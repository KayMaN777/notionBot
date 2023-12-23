from typing import List, Tuple, Optional

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

import api


def set_info(keyboard: List[List[InlineKeyboardButton]]) -> List[List[InlineKeyboardButton]]:
    for i in range(len(keyboard)):
        for j in range(len(keyboard[i])):
            keyboard[i][j].callback_data = "info"
    return keyboard


queries = []
for query in api.types:
    queries.append([KeyboardButton(text=query)])
queries = ReplyKeyboardMarkup(keyboard=queries, resize_keyboard=True)

cancel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отмена")]], resize_keyboard=True)

skip = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пропустить"), KeyboardButton(text="Отмена")]],
    resize_keyboard=True
)


def get_today_tasks(projects: List[Tuple[str, Optional[str]]]) -> InlineKeyboardMarkup:
    return get_all_tasks(projects)


def get_all_projects(projects: List[Tuple[str, int]]) -> InlineKeyboardMarkup:
    keyboard = []
    for project in projects:
        keyboard.append([InlineKeyboardButton(text=f"{project[0]} ({project[1]})")])
    return InlineKeyboardMarkup(inline_keyboard=set_info(keyboard))


def get_all_tasks(projects: List[Tuple[str, Optional[str]]]) -> InlineKeyboardMarkup:
    keyboard = []
    for project in projects:
        if project[1] is not None:
            keyboard.append([InlineKeyboardButton(text=f"{project[0]} до {project[1]}")])
        else:
            keyboard.append([InlineKeyboardButton(text=f"{project[0]}")])
    return InlineKeyboardMarkup(inline_keyboard=set_info(keyboard))
