from typing import List, Tuple, Optional

import datetime

from aiogram.filters.callback_data import CallbackData
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from todoist_api_python.models import Task

import api

queries = []
for query in api.types:
    queries.append([KeyboardButton(text=query)])
queries = ReplyKeyboardMarkup(keyboard=queries, resize_keyboard=True)

cancel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отмена")]], resize_keyboard=True)

skip = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пропустить"), KeyboardButton(text="Отмена")]],
    resize_keyboard=True
)


class TaskInfo(CallbackData, prefix="task_info"):
    content: str
    description: str


def get_list(texts: List[str]) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=text)] for text in texts]
    keyboard.append([KeyboardButton(text="Отмена")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def set_info(keyboard: List[List[InlineKeyboardButton]]) -> List[List[InlineKeyboardButton]]:
    for i in range(len(keyboard)):
        for j in range(len(keyboard[i])):
            keyboard[i][j].callback_data = "info"
    return keyboard


def get_today_tasks(tasks: List[Tuple[str, Optional[datetime.datetime], Task]]) -> InlineKeyboardMarkup:
    keyboard = []
    now = datetime.datetime.now()
    for task in tasks:
        if task[1] is not None and task[1].date() == now.date():
            text = f"\"{task[0]}\" до {task[1].time()}    "
            if task[1] < now:
                text += "❌"
            else:
                text += "✅"
            keyboard.append([
                InlineKeyboardButton(
                    text=text, callback_data=TaskInfo(content=task[0], description=task[2].description).pack()
                )
            ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_all_projects(projects: List[Tuple[str, int]]) -> InlineKeyboardMarkup:
    keyboard = []
    for project in projects:
        keyboard.append([InlineKeyboardButton(text=f"\"{project[0]}\" ({project[1]})")])
    return InlineKeyboardMarkup(inline_keyboard=set_info(keyboard))


def get_all_tasks(tasks: List[Tuple[str, Optional[datetime.datetime], Task]]) -> InlineKeyboardMarkup:
    keyboard = []
    now = datetime.datetime.now()
    for task in tasks:
        text = f"\"{task[0]}\""
        if task[1] is not None:
            text += f" до {task[1]}   "
            if task[1] < now:
                text += "❌"
            else:
                text += "✅"
        keyboard.append([
            InlineKeyboardButton(
                text=text, callback_data=TaskInfo(content=task[0], description=task[2].description).pack()
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def choose_attrs(data: dict) -> ReplyKeyboardMarkup:
    keyboard = []
    if "type_idx" in data:
        keyboard.append([KeyboardButton(text=f"Тип запроса: {api.types[data['type_idx']]}")])
    if "name" in data:
        keyboard.append([KeyboardButton(text=f"Имя проекта: {data['name']}")])
    if "content" in data:
        keyboard.append([KeyboardButton(text=f"Имя задачи: {data['content']}")])
    if "due_string" in data:
        keyboard.append([KeyboardButton(text=f"Дедлайн: {data['due_string']}")])
    keyboard.append([KeyboardButton(text="Сохранить")])
    keyboard.append([KeyboardButton(text="Отмена")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
