from typing import List, Optional, Tuple

import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from nltk import RegexpTokenizer

from src import api, kb, states

from src.finder import Finder, clear_text
from src.handlers.base import funcs, choose_query

router = Router()

name_tokenizer = RegexpTokenizer(r"\"[^\"]+\"")
date_tokenizer = RegexpTokenizer(r"\d{2}\.\d{2}\.\d{4}|\d{2}\.\d{2}\.\d{2}")
time_tokenizer = RegexpTokenizer(r"\d{1,2}:\d{2}")
finder = Finder(api.types)


def add_name(query: str, data: dict) -> None:
    name = None
    if data["type_idx"] == 0 or data["type_idx"] == 3:
        res = name_tokenizer.tokenize(query)
        if len(res) == 1:
            name = res[0][1: -1].strip()
    if data["type_idx"] == 0 and name is not None:
        data["name"] = name
    if 3 <= data["type_idx"] <= 5 and "name" not in data:
        data["name"] = "Inbox"
    if data["type_idx"] == 3 and name is not None:
        data["content"] = name
        if data["name"] == name:
            data["name"] = "Inbox"


def add_due_string(query: str, data: dict) -> None:
    query = query.lower()
    date = date_tokenizer.tokenize(query)
    date = date[0] if len(date) == 1 else ""
    if date == "":
        for v in ("сегодня", "today", "завтра", "tomorrow", "вчера", "yesterday"):
            if v in query:
                date = v
                break
    time = time_tokenizer.tokenize(query)
    time = time[0] if len(time) == 1 else ""
    due_string = date + " " + time
    due_string = due_string.strip()
    if due_string != "":
        data["due_string"] = due_string


@router.message(states.Menu.choose_query)
async def get_custom_query(msg: Message, state: FSMContext):
    data = await state.get_data()

    res_all = await api.get_all(data["token"])
    names = []
    contents = []
    for project, tasks in res_all:
        names.append(project.name)
        contents.extend([task.content for task in tasks])

    query = msg.text.strip()
    res = await asyncio.gather(asyncio.to_thread(finder.get, query, [names, contents]))
    type_idx: int = res[0][0]
    nearest: List[Optional[Tuple[int, int]]] = res[0][1]

    data["type_idx"] = type_idx

    if nearest[0] is not None and nearest[0][1] >= 50:
        data["name"] = names[nearest[0][0]]
    if nearest[1] is not None and nearest[1][1] >= 50:
        data["content"] = contents[nearest[1][0]]

    query = clear_text(query)

    await asyncio.gather(asyncio.to_thread(add_name, query, data))
    await asyncio.gather(asyncio.to_thread(add_due_string, query, data))

    await state.set_data(data)
    await state.set_state(states.CustomQuery.state)
    await msg.answer(
        "Запрос обработан. Выберите что *неверно*", parse_mode='Markdown', reply_markup=kb.choose_attrs(data)
    )


@router.message(F.text == "Сохранить", states.CustomQuery.state)
async def save_attrs(msg: Message, state: FSMContext):
    data = await state.get_data()
    if "type_idx" in data:
        await funcs[data["type_idx"]](msg, state)
    else:
        await choose_query(msg, state, reset=False)


@router.message(states.CustomQuery.state)
async def drop_attrs(msg: Message, state: FSMContext):
    data = await state.get_data()

    choice = msg.text.strip()
    choice = choice.split(':')[0].strip().lower()

    match choice:
        case "тип запроса":
            data.pop("type_idx")
        case "имя проекта":
            data.pop("name")
        case "имя задачи":
            data.pop("content")
        case "дедлайн":
            data.pop("due_string")
        case _:
            await incorrect(msg)
            return

    await state.set_data(data)
    await state.set_state(states.CustomQuery.state)
    await msg.answer("Выберите что *неверно*", parse_mode='Markdown', reply_markup=kb.choose_attrs(data))


@router.callback_query(F.data == "info")
async def info_handler(query: CallbackQuery):
    await query.answer("Информация")


@router.message()
async def incorrect(msg: Message):
    await msg.reply("Некорректная команда")
