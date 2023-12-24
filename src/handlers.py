from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command

import api
import kb
import states

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    data = await state.get_data()
    if "token" in data:
        await msg.answer(f"С возвращением, {msg.from_user.full_name}!", reply_markup=ReplyKeyboardRemove())
        await choose_query(msg, state)
    else:
        await msg.answer(f"Добро пожаловать, {msg.from_user.full_name}!", reply_markup=ReplyKeyboardRemove())
        await login(msg, state)


async def login(msg: Message, state: FSMContext):
    await state.set_state(states.Menu.get_token)
    await msg.answer("Введите Ваш API-токен от Todoist")


@router.message(states.Menu.get_token)
async def get_token(msg: Message, state: FSMContext):
    token = msg.text.strip()
    if await api.check_token(token):
        await state.update_data(token=token)
        await msg.answer("Успешная авторизация")
        await choose_query(msg, state)
    else:
        await msg.answer("Не удалось авторизоваться. Попробуйте снова")


@router.message(F.text == "Отмена")
async def choose_query(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_data({"token": data["token"]})
    await state.set_state(states.Menu.choose_query)
    await msg.answer("Введите запрос", reply_markup=kb.queries)


@router.message(F.text == "Добавить проект", states.Menu.choose_query)
async def add_project(msg: Message, state: FSMContext):
    data = await state.get_data()
    if "name" not in data:
        await state.set_state(states.AddProject.name)
        await msg.answer("Введите имя проекта", reply_markup=kb.cancel)
    else:
        flag = await api.add_project(data["token"], data["name"])
        if flag:
            await msg.answer("Проект успешно добавлен")
        else:
            await msg.answer("Ошибка")
        await choose_query(msg, state)


@router.message(F.text == "Удалить проект", states.Menu.choose_query)
async def delete_project(msg: Message, state: FSMContext):
    data = await state.get_data()
    if "name" not in data:
        names = await api.get_names(data["token"])
        if names == ["Inbox"]:
            await msg.answer("Нет проектов для удаления")
            await choose_query(msg, state)
        else:
            await state.set_state(states.DeleteProject.name)
            await msg.answer("Введите имя проекта", reply_markup=kb.get_list(names))
    else:
        flag = await api.delete_project(data["token"], data["name"])
        if flag:
            await msg.answer("Проект успешно удален")
        else:
            await msg.answer("Ошибка")
        await choose_query(msg, state)


@router.message(F.text == "Переименовать проект", states.Menu.choose_query)
async def rename_project(msg: Message, state: FSMContext):
    data = await state.get_data()
    if "name" not in data:
        names = await api.get_names(data["token"])
        if names == ["Inbox"]:
            await msg.answer("Нет проектов для переименования")
            await choose_query(msg, state)
        else:
            await state.set_state(states.RenameProject.name)
            await msg.answer("Введите имя проекта", reply_markup=kb.get_list(names))
    elif "new_name" not in data:
        await state.set_state(states.RenameProject.new_name)
        await msg.answer("Введите новое имя проекта", reply_markup=kb.cancel)
    else:
        flag = await api.rename_project(data["token"], data["name"], data["new_name"])
        if flag:
            await msg.answer("Проект успешно переименован")
        else:
            await msg.answer("Ошибка")
        await choose_query(msg, state)


@router.message(F.text == "Создать задачу", states.Menu.choose_query)
async def create_task(msg: Message, state: FSMContext):
    data = await state.get_data()
    if "name" not in data:
        names = await api.get_names(data["token"])
        await state.set_state(states.CreateTask.name)
        await msg.answer("Введите имя проекта", reply_markup=kb.get_list(names))
    elif "content" not in data:
        await state.set_state(states.CreateTask.content)
        await msg.answer("Введите имя задачи", reply_markup=kb.cancel)
    elif "description" not in data:
        await state.set_state(states.CreateTask.description)
        await msg.answer("Введите описание", reply_markup=kb.skip)
    elif "due_string" not in data:
        await state.set_state(states.CreateTask.due_string)
        await msg.answer("Введите дедлайн", reply_markup=kb.skip)
    else:
        flag = await api.create_task(
            data["token"], data["name"], data["content"], data["description"], data["due_string"]
        )
        if flag:
            await msg.answer("Задача успешно добавлена")
        else:
            await msg.answer("Ошибка")
        await choose_query(msg, state)


@router.message(F.text == "Удалить задачу", states.Menu.choose_query)
async def delete_task(msg: Message, state: FSMContext):
    data = await state.get_data()
    if "name" not in data:
        names = await api.get_names(data["token"])
        await state.set_state(states.DeleteTask.name)
        await msg.answer("Введите имя проекта", reply_markup=kb.get_list(names))
    elif "content" not in data:
        contents = await api.get_contents(data["token"], data["name"])
        if len(contents) == 0:
            await msg.answer("Нет задач в этом проекте")
            await choose_query(msg, state)
        else:
            await state.set_state(states.DeleteTask.content)
            await msg.answer("Введите имя задачи", reply_markup=kb.get_list(contents))
    else:
        flag = await api.delete_task(data["token"], data["name"], data["content"])
        if flag:
            await msg.answer("Задача успешно удалена")
        else:
            await msg.answer("Ошибка")
        await choose_query(msg, state)


@router.message(F.text == "Обновить задачу", states.Menu.choose_query)
async def update_task(msg: Message, state: FSMContext):
    data = await state.get_data()
    if "name" not in data:
        names = await api.get_names(data["token"])
        await state.set_state(states.UpdateTask.name)
        await msg.answer("Введите имя проекта", reply_markup=kb.get_list(names))
    elif "content" not in data:
        contents = await api.get_contents(data["token"], data["name"])
        if len(contents) == 0:
            await msg.answer("В этом проекте нет задач")
            await choose_query(msg, state)
        else:
            await state.set_state(states.UpdateTask.content)
            await msg.answer("Введите имя задачи", reply_markup=kb.get_list(contents))
    elif "new_content" not in data:
        await state.set_state(states.UpdateTask.new_content)
        await msg.answer("Введите новое имя задачи", reply_markup=kb.skip)
    elif "new_description" not in data:
        await state.set_state(states.UpdateTask.new_description)
        await msg.answer("Введите новое описание", reply_markup=kb.skip)
    elif "new_due_string" not in data:
        await state.set_state(states.UpdateTask.new_due_string)
        await msg.answer("Введите новый дедлайн", reply_markup=kb.skip)
    else:
        flag = await api.update_task(
            data["token"], data["name"], data["content"],
            data["new_content"], data["new_description"], data["new_due_string"]
        )
        if flag:
            await msg.answer("Задача успешно обновлена")
        else:
            await msg.answer("Ошибка")
        await choose_query(msg, state)


@router.message(states.AddProject.name)
@router.message(states.RenameProject.new_name)
async def get_new_name(msg: Message, state: FSMContext):
    data = await state.get_data()
    name = msg.text.strip()
    flag = await api.find_project_name(data["token"], name)
    if flag == 0:
        await set_arg(name, msg, state)
    elif flag == 1:
        await msg.answer("Имя проекта уже занято")
    else:
        await msg.answer("Ошибка")


@router.message(states.DeleteProject.name)
@router.message(states.RenameProject.name)
@router.message(states.CreateTask.name)
@router.message(states.DeleteTask.name)
@router.message(states.UpdateTask.name)
async def get_exist_name(msg: Message, state: FSMContext):
    data = await state.get_data()
    name = msg.text.strip()
    flag = await api.find_project_name(data["token"], name)
    if flag == 1:
        await set_arg(name, msg, state)
    elif flag == 0:
        await msg.answer("Нет проекта с таким именем")
    else:
        await msg.answer("Ошибка")


@router.message(states.CreateTask.content)
@router.message(F.text != "Пропустить", states.UpdateTask.new_content)
async def get_new_content(msg: Message, state: FSMContext):
    data = await state.get_data()
    content = msg.text.strip()
    flag = await api.find_task_content(data["token"], data["name"], content)
    if flag == 0:
        await set_arg(content, msg, state)
    elif flag == 1:
        await msg.answer("Имя задачи уже занято")
    else:
        await msg.answer("Ошибка")


@router.message(states.DeleteTask.content)
@router.message(states.UpdateTask.content)
async def get_exists_content(msg: Message, state: FSMContext):
    data = await state.get_data()
    content = msg.text.strip()
    flag = await api.find_task_content(data["token"], data["name"], content)
    if flag == 1:
        await set_arg(content, msg, state)
    elif flag == 0:
        await msg.answer("Нет задачи с таким именем")
    else:
        await msg.answer("Ошибка")


@router.message(states.CreateTask.description)
@router.message(states.CreateTask.due_string)
@router.message(states.UpdateTask.new_content)
@router.message(states.UpdateTask.new_description)
@router.message(states.UpdateTask.new_due_string)
async def get_add_args(msg: Message, state: FSMContext):
    text = msg.text.strip()
    if text == "Пропустить":
        text = None
    await set_arg(text, msg, state)


async def set_arg(value: str, msg: Message, state: FSMContext):
    state_name = await state.get_state()
    state_name = state_name.split(":")
    await state.update_data({state_name[1]: value})
    await mapper[state_name[0]](msg, state)


@router.message(F.text == "Список задач на сегодня", states.Menu.choose_query)
async def get_today_tasks(msg: Message, state: FSMContext):
    data = await state.get_data()
    tasks = await api.get_today_tasks(data["token"])
    if len(tasks) == 0:
        await msg.answer("Нет задач на сегодня")
    else:
        await msg.answer("Список задач на сегодня:", reply_markup=kb.get_today_tasks(tasks))


@router.message(F.text == "Список всех проектов", states.Menu.choose_query)
async def get_all_projects(msg: Message, state: FSMContext):
    data = await state.get_data()
    projects = await api.get_all_projects(data["token"])
    await msg.answer("Список всех проектов:", reply_markup=kb.get_all_projects(projects))


@router.message(F.text == "Список всех задач", states.Menu.choose_query)
async def get_all_tasks(msg: Message, state: FSMContext):
    data = await state.get_data()
    tasks = await api.get_all_tasks(data["token"])
    if len(tasks) == 0:
        await msg.answer("Нет задач")
    else:
        await msg.answer("Список всех задач:", reply_markup=kb.get_all_tasks(tasks))


@router.callback_query(F.data == "info")
async def info_handler(query: CallbackQuery):
    await query.answer("Информация")


@router.message()
async def incorrect(msg: Message):
    await msg.reply("Некорректная команда")


mapper = {
    "AddProject": add_project,
    "DeleteProject": delete_project,
    "RenameProject": rename_project,
    "CreateTask": create_task,
    "DeleteTask": delete_task,
    "UpdateTask": update_task,
}
