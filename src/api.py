from typing import Optional, List, Tuple

import datetime

from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import Project, Task


async def check_token(token: str) -> bool:
    api = TodoistAPIAsync(token)
    try:
        await api.get_projects()
        return True
    except Exception as error:
        print(error)
        return False


async def find_project_name(token: str, name: str) -> Optional[bool]:
    api = TodoistAPIAsync(token)
    try:
        projects = await api.get_projects()
        for project in projects:
            if project.name == name:
                return True
        return False
    except Exception as error:
        print(error)
        return None


async def get_project_id(token: str, name: str) -> Optional[str]:
    api = TodoistAPIAsync(token)
    try:
        projects = await api.get_projects()
        for project in projects:
            if project.name == name:
                return project.id
        return None
    except Exception as error:
        print(error)
        return None


async def get_names(token: str) -> List[str]:
    api = TodoistAPIAsync(token)
    try:
        projects = await api.get_projects()
        return [project.name for project in projects]
    except Exception as error:
        print(error)
        return []


async def add_project(token: str, name: str) -> bool:
    api = TodoistAPIAsync(token)
    try:
        await api.add_project(name=name)
        return True
    except Exception as error:
        print(error)
        return False


async def delete_project(token: str, name: str) -> bool:
    api = TodoistAPIAsync(token)
    project_id = await get_project_id(token, name)
    try:
        is_success = await api.delete_project(project_id=project_id)
        return is_success
    except Exception as error:
        print(error)
        return False


async def rename_project(token: str, name: str, new_name: str) -> bool:
    api = TodoistAPIAsync(token)
    project_id = await get_project_id(token, name)
    try:
        is_success = await api.update_project(project_id=project_id, name=new_name)
        return is_success
    except Exception as error:
        print(error)
        return False


async def find_task_content(token: str, name: str, content: str) -> Optional[bool]:
    api = TodoistAPIAsync(token)
    project_id = await get_project_id(token, name)
    try:
        tasks = await api.get_tasks(project_id=project_id)
        for task in tasks:
            if task.content == content:
                return True
        return False
    except Exception as error:
        print(error)
        return None


async def get_task_id(token: str, name: str, content: str) -> Optional[str]:
    api = TodoistAPIAsync(token)
    project_id = await get_project_id(token, name)
    try:
        tasks = await api.get_tasks(project_id=project_id)
        for task in tasks:
            if task.content == content:
                return task.id
        return None
    except Exception as error:
        print(error)
        return None


async def get_contents(token: str, name: str) -> List[str]:
    api = TodoistAPIAsync(token)
    project_id = await get_project_id(token, name)
    try:
        tasks = await api.get_tasks(project_id=project_id)
        return [task.content for task in tasks]
    except Exception as error:
        print(error)
        return []


async def create_task(token: str, name: str, content: str, description: str, due_string: str) -> bool:
    api = TodoistAPIAsync(token)
    project_id = await get_project_id(token, name)
    try:
        await api.add_task(
            project_id=project_id, content=content, description=description, due_string=due_string, due_lang="ru"
        )
        return True
    except Exception as error:
        print(error)
        return False


async def delete_task(token: str, name: str, content: str) -> bool:
    api = TodoistAPIAsync(token)
    task_id = await get_task_id(token, name, content)
    try:
        is_success = await api.delete_task(task_id=task_id)
        return is_success
    except Exception as error:
        print(error)
        return False


async def update_task(
        token: str, name: str, content: str,
        new_content: Optional[str], new_description: Optional[str], new_due_string: Optional[str]
) -> bool:
    api = TodoistAPIAsync(token)
    task_id = await get_task_id(token, name, content)
    try:
        is_success = True
        if new_content is not None:
            is_success &= await api.update_task(task_id=task_id, content=new_content)
        if new_description is not None:
            is_success &= await api.update_task(task_id=task_id, description=new_description)
        if new_due_string is not None:
            is_success &= await api.update_task(task_id=task_id, due_string=new_due_string)
        return is_success
    except Exception as error:
        print(error)
        return False


async def get_all(token: str) -> List[Tuple[Project, List[Task]]]:
    api = TodoistAPIAsync(token)
    res = []
    try:
        projects = await api.get_projects()
        for project in projects:
            tasks = await api.get_tasks(project_id=project.id)
            res.append((project, tasks))
        return res
    except Exception as error:
        print(error)
        return []


async def get_today_tasks(token: str) -> List[Tuple[str, str]]:
    res_all = await get_all(token)
    res = []
    today = str(datetime.date.today())
    for _, tasks in res_all:
        for task in tasks:
            if task.due is not None and task.due.date == today:
                if task.due.datetime is not None:
                    res.append((task.content, task.due.datetime.split('T')[1]))
                else:
                    res.append((task.content, None))
    return res


async def get_all_projects(token: str) -> List[Tuple[str, int]]:
    res_all = await get_all(token)
    res = []
    for project, tasks in res_all:
        res.append((project.name, len(tasks)))
    return res


async def get_all_tasks(token: str) -> List[Tuple[str, Optional[str]]]:
    res_all = await get_all(token)
    res = []
    for project, tasks in res_all:
        for task in tasks:
            if task.due is not None:
                if task.due.datetime is not None:
                    res.append((task.content, task.due.datetime.replace('T', '')))
                else:
                    res.append((task.content, task.due.date))
            else:
                res.append((task.content, None))
    return res


types = [
    "Добавить проект",
    "Удалить проект",
    "Переименовать проект",
    "Создать задачу",
    "Удалить задачу",
    "Обновить задачу",
    "Список задач на сегодня",
    "Список всех проектов",
    "Список всех задач",
]
