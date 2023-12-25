from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src import kb

router = Router()


@router.callback_query(kb.TaskInfo.filter())
async def get_task_info(query: CallbackQuery, callback_data: kb.TaskInfo):
    description = callback_data.description
    if description is not None and description != "":
        await query.message.answer("Описание: " + description)
    else:
        await query.answer("Нет описания")


@router.callback_query(F.data == "info")
async def info_handler(query: CallbackQuery):
    await query.answer("Информация")


@router.message()
async def incorrect(msg: Message):
    await msg.reply("Некорректная команда")
