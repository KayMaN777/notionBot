from todoist_api_python.api import TodoistAPI
from datetime import date

class MyApi:
    '''Класс, создаваемый для взаимодействия с органайзером пользователя
       по его токену.
    '''
    def __init__(self, TOKEN):
        self.api = TodoistAPI(TOKEN)
    
    # Получаем id проекта
    def GetProjectId(self, name):
        try:
            projects = self.api.get_projects()
            res = None
            for project in projects:
                if (project.name == name):
                    res = project.id
            return res
        except Exception as e:
            raise e
    
    # Добавление нового проекта
    def AddProject(self, name, parent = None, style = "list", color = "charcoal"):
        try:
            parent_id = self.GetProjectId(parent)
            project = self.api.add_project(name = name, parent_id = parent_id, view_style = style, color = color)
            return project.id
        except Exception as e:
            raise e
    
    # Удаление проекта
    def DeleteProject(self, name):
        try:
            project_id = self.GetProjectId(name)
            self.api.delete_project(project_id=project_id)
        except Exception as e:
            raise e
    
    # Переименование проекта
    def RenameProject(self, name, new_name):
        try:
            project_id = self.GetProjectId(name)
            project = self.api.update_project(project_id = project_id, name = new_name)
            return project.id
        except Exception as e:
            raise e

    # Получение id задачи
    def GetTaskId(self, content, project):
        project_id = self.GetProjectId(project)
        tasks = self.api.get_tasks(project_id = project_id)
        res = None
        for task in tasks:
            if (task.content == content):
                res = task.id
        return res

    # Добавление новой задачи, по умолчанию если не указан проект, добавляется в inbox
    def AddTask(self, content, project = "Inbox", description = None, date = None, priority = 1):
        try:
            project_id = self.GetProjectId(project)
            task = self.api.add_task(content=content, project_id = project_id, description = description, due_date = date, priority = priority)
            return task
        except Exception as e:
            raise e

    # Закрытие задачи
    def CloseTask(self, content, project = "Inbox"):
        try:
            task_id = self.GetTaskId(content, project)
            self.api.close_task(task_id = task_id)
        except Exception as e:
            raise e
    
    # Просмотреть задачи на сегодня
    def TodayTasks(self, project = "Inbox"):
        try:
            project_id = self.GetProjectId(project)
            today = str(date.today())
            tasks = self.api.get_tasks(project_id = project_id)
            res = []
            for task in tasks:
                if (task.due != None and task.due.date == today):
                    res.append(task)
            return res
        except Exception as e:
            raise e
