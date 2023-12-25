# notionBot

ТГ-бот, который будет создавать задачи/карточки в трекере

# Описание

* Бот поддерживает 10 различных команд для взаимодействия с Todoist
* С помощью них можно управлять проектами и задачам.
  Также посмотреть общие списки, задания на сегодня и получить описание
* Во время ввода данных при необходимости показывается список доступных вариантов
* Есть функция автоматической обработки сообщения с запросом с помощью ИИ и других методов
* Асинхронная реализация
* Обработаны возможные исключения и некорректные запросы

# Установка

* В переменные среды нужно поместить BOT_TOKEN
* Необходимые зависимости в [requirements](/requirements.txt)
* Зарегистрироваться на [Todoist](https://todoist.com/)

# Команды

* /info — получить информацию
* /start — начать взаимодействие
* /logout — выйти, чтобы сменить API-токен

# Поддерживаемые запросы

1. Добавить проект
2. Удалить проект
3. Переименовать проект
4. Создать задачу
5. Удалить задачу
6. Обновить задачу
7. Список задач на сегодня
8. Список всех проектов
9. Список всех задач
10. Удалить пропущенные задачи
