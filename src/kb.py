from typing import List, Tuple, Optional

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

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


def get_list(texts: List[str]) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=text)] for text in texts]
    keyboard.append([KeyboardButton(text="Отмена")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def set_info(keyboard: List[List[InlineKeyboardButton]]) -> List[List[InlineKeyboardButton]]:
    for i in range(len(keyboard)):
        for j in range(len(keyboard[i])):
            keyboard[i][j].callback_data = "info"
    return keyboard


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


def choose_attrs(data: dict) -> ReplyKeyboardMarkup:
    keyboard = []
    if "type_idx" in data:
        keyboard.append([KeyboardButton(text=f"Тип запроса: {api.types[data['type_idx']]}")])
    if "name" in data:
        keyboard.append([KeyboardButton(text=f"Имя проекта: {data['name']}")])
    keyboard.append([KeyboardButton(text="Сохранить")])
    keyboard.append([KeyboardButton(text="Отмена")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
