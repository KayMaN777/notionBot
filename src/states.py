from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    get_token = State()
    choose_query = State()


class AddProject(StatesGroup):
    name = State()


class DeleteProject(StatesGroup):
    name = State()


class RenameProject(StatesGroup):
    name = State()
    new_name = State()


class CreateTask(StatesGroup):
    name = State()
    content = State()
    description = State()
    due_string = State()


class DeleteTask(StatesGroup):
    name = State()
    content = State()


class UpdateTask(StatesGroup):
    name = State()
    content = State()
    new_content = State()
    new_description = State()
    new_due_string = State()


class CustomQuery(StatesGroup):
    state = State()
