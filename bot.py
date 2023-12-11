import telebot
import ToDoistApi
from ToDoistApi import MyApi
import DataManager
from DataManager import User
import shutil
import os
from random import randint

import re
import requests
from bs4 import BeautifulSoup


# Для создания кнопок
from telebot import types



bot = telebot.TeleBot('6782562513:AAEzhFxFmumCg9x06o1n0seZ6wRdHe_xAvY')



@bot.message_handler(commands=["start"])
def start(message, res=False):
    User(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    more_info_button = types.KeyboardButton('Что я умею?')
    auth_button = types.KeyboardButton('Авторизоваться')
    markup.add(more_info_button, auth_button)
    User(message.chat.id).SetFlagVal("PrevMessage", message.text)
    bot.send_message(message.chat.id, 'Я - Organaizer Bot. С моей помощью вы сможете создавать и редактировать карточки в Notion. Вы можете узнать больше информации, нажав на кнопку "Что я умею?", или авторизоваться в боте для начала работы', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def start_command(message):
    if message.text == 'Что я умею?'or message.text == 'информация' or message.text == 'Инофрмация' or message.text == 'Инфо' or message.text == 'инфо':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        User(message.chat.id)
        add_project = types.KeyboardButton('Добавить проект')
        delete_project = types.KeyboardButton('Удалить проект')
        rename_project = types.KeyboardButton('Переименовать проект')
        add_task = types.KeyboardButton('Добавить в задачу проект')
        close_task = types.KeyboardButton('Удалить задачу из проекта')
        markup.add(add_project, delete_project, rename_project, add_task, close_task)
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        bot.send_message(message.chat.id, 'С моей помощью Вы можете создавать, редактировать проекты, а также добавлять и закрывать задачи в текущих проектах. Чтобы начать работу просто нажми на одну из кнопок', reply_markup=markup)

    elif message.text == 'Авторизоваться':
        User(message.chat.id).SetFlagVal("DialogStatusFlag", "GettingApiKey")
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        bot.send_message(message.chat.id, 'Введите своей API-ключь от todoist : ')

    elif User(message.chat.id).GetFlagVal("DialogStatusFlag") == "GettingApiKey":
        User(message.chat.id).SetFlagVal("DialogStatusFlag", "Default")
        User(message.chat.id).SetFlagVal("IsAuthorizedFlag", "True")
        User(message.chat.id).SetFlagVal("ApiKey", str(message.text))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        add_project = types.KeyboardButton('Добавить проект')
        delete_project = types.KeyboardButton('Удалить проект')
        rename_project = types.KeyboardButton('Переименовать проект')
        add_task = types.KeyboardButton('Добавить в задачу проект')
        close_task = types.KeyboardButton('Удалить задачу из проекта')
        markup.add(add_project, delete_project, rename_project, add_task, close_task)
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        bot.send_message(message.chat.id,
                         'Авторизация прошла успешно! С моей помощью Вы можете создавать, редактировать проекты, а также добавлять и закрывать задачи в текущих проектах. Чтобы начать работу просто нажми на одну из кнопок',
                         reply_markup=markup)
    elif User(message.chat.id).GetFlagVal("IsAuthorizedFlag") == "False":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        more_info_button = types.KeyboardButton('Что я умею?')
        auth_button = types.KeyboardButton('Авторизоваться')
        markup.add(more_info_button, auth_button)
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        bot.send_message(message.chat.id,
                         'Вы еще не авторизовались. Пожалуйста, нажмите на кнопку "Авторизоваться" для начала работы',
                         reply_markup=markup)


    elif message.text == 'Добавить проект':
        User(message.chat.id).SetFlagVal("DialogStatusFlag", "AddingNewProject")
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        bot.send_message(message.chat.id, 'Введите название для проекта : ')
    elif User(message.chat.id).GetFlagVal("DialogStatusFlag") == "AddingNewProject":
        User(message.chat.id).SetFlagVal("DialogStatusFlag", "Default")

        # calling Api
        MyApi(User(message.chat.id).GetFlagVal("ApiKey")).AddProject(message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        add_project = types.KeyboardButton('Добавить проект')
        delete_project = types.KeyboardButton('Удалить проект')
        rename_project = types.KeyboardButton('Переименовать проект')
        add_task = types.KeyboardButton('Добавить в задачу проект')
        close_task = types.KeyboardButton('Удалить задачу из проекта')
        markup.add(add_project, delete_project, rename_project, add_task, close_task)
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        bot.send_message(message.chat.id,
                         'Проект ' + str(message.text) + ' создан! Доступные действия можете увидеть с помощью кнопок',
                         reply_markup=markup)
    elif message.text == 'Удалить проект':
        User(message.chat.id).SetFlagVal("DialogStatusFlag", "DeletingProject")
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        bot.send_message(message.chat.id, 'Введите название удаляемого проекта : ')
    elif User(message.chat.id).GetFlagVal("DialogStatusFlag") == "DeletingProject":
        User(message.chat.id).SetFlagVal("DialogStatusFlag", "Default")
        # calling Api
        MyApi(User(message.chat.id).GetFlagVal("ApiKey")).DeleteProject(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        add_project = types.KeyboardButton('Добавить проект')
        delete_project = types.KeyboardButton('Удалить проект')
        rename_project = types.KeyboardButton('Переименовать проект')
        add_task = types.KeyboardButton('Добавить в задачу проект')
        close_task = types.KeyboardButton('Удалить задачу из проекта')
        markup.add(add_project, delete_project, rename_project, add_task, close_task)
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        bot.send_message(message.chat.id,
                         'Проект ' + str(message.text) + ' удален! Доступные действия можете увидеть с помощью кнопок',
                         reply_markup=markup)
    elif message.text == 'Переименовать проект':
        User(message.chat.id).SetFlagVal("DialogStatusFlag", "RenamingProjectSt1")
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        bot.send_message(message.chat.id, 'Введите старое название проекта : ')
    elif User(message.chat.id).GetFlagVal("DialogStatusFlag") == "RenamingProjectSt1":
        User(message.chat.id).SetFlagVal("DialogStatusFlag", "RenamingProjectSt2")
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        bot.send_message(message.chat.id, 'Введите новое название проекта : ')
    elif User(message.chat.id).GetFlagVal("DialogStatusFlag") == "RenamingProjectSt2":
        User(message.chat.id).SetFlagVal("DialogStatusFlag", "Default")

        # calling Api
        MyApi(User(message.chat.id).GetFlagVal("ApiKey")).RenameProject(User(message.chat.id).GetFlagVal("PrevMessage"), message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        add_project = types.KeyboardButton('Добавить проект')
        delete_project = types.KeyboardButton('Удалить проект')
        rename_project = types.KeyboardButton('Переименовать проект')
        add_task = types.KeyboardButton('Добавить в задачу проект')
        close_task = types.KeyboardButton('Удалить задачу из проекта')
        markup.add(add_project, delete_project, rename_project, add_task, close_task)
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        bot.send_message(message.chat.id,
                         'Проект ' + str(message.text) + ' успешно переименован! Доступные действия можете увидеть с помощью кнопок',
                         reply_markup=markup)
    elif message.text == 'Добавить в задачу проект':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        add_project = types.KeyboardButton('Добавить проект')
        delete_project = types.KeyboardButton('Удалить проект')
        rename_project = types.KeyboardButton('Переименовать проект')
        add_task = types.KeyboardButton('Добавить в задачу проект')
        close_task = types.KeyboardButton('Удалить задачу из проекта')
        markup.add(add_project, delete_project, rename_project, add_task, close_task)
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        bot.send_message(message.chat.id, 'Извините, я пока не умею такое :D\n Доступные действия можете увидеть с помощью кнопок',
                         reply_markup=markup)
    elif message.text == 'Удалить задачу из проекта':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        add_project = types.KeyboardButton('Добавить проект')
        delete_project = types.KeyboardButton('Удалить проект')
        rename_project = types.KeyboardButton('Переименовать проект')
        add_task = types.KeyboardButton('Добавить в задачу проект')
        close_task = types.KeyboardButton('Удалить задачу из проекта')
        markup.add(add_project, delete_project, rename_project, add_task, close_task)
        User(message.chat.id).SetFlagVal("PrevMessage", message.text)
        bot.send_message(message.chat.id,
                         'Извините, я пока не умею такое :D\n Доступные действия можете увидеть с помощью кнопок',
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Не знаю, что Вам ответить. Напишите "Инфо" чтобы увидеть спиок доступных действий')


bot.polling(none_stop=True)