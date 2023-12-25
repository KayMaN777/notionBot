import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src import api, kb, states

from src.finder import Attrs, Finder
from src.handlers.base import funcs, choose_query

router = Router()

finder = Finder(api.types)


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
    res = await asyncio.gather(asyncio.to_thread(finder.get_attrs, query, [names, contents]))
    attrs: Attrs = res[0]
    print(query, api.types[attrs.type_idx], attrs)  # TODO

    data["type_idx"] = attrs.type_idx
    # if attrs.due_string is not None:
    #     data["due_string"] = attrs.due_string

    if attrs.nearest[0] is not None and attrs.nearest[0][1] >= 50:
        data["name"] = names[attrs.nearest[0][0]]
    if attrs.nearest[1] is not None and attrs.nearest[1][1] >= 50:
        data["content"] = contents[attrs.nearest[1][0]]

    # if attrs.name is not None:
    #     if "задач" in api.types[attrs.type_idx].lower():
    #         data["name"] = "Inbox"
    #         data["content"] = attrs.name
    #     else:
    #         data["name"] = attrs.name

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
        case "дедлайн":
            data.pop("due_string")
        case _:
            await incorrect(msg, state)
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
