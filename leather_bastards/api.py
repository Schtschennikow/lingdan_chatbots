# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами, импортируем модуль рандомизации.
import json
import logging
import random

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Ты хочешь захватить мир?",
                "Люди тебя обижают?",
                "Я тебя боюсь",
            ]
        }

        res['response']['text'] = 'Привет, организмы!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Отвечаем на всё рандомной фразой из списка
    res['response']['text'] = random.choice(['Ненавижу эту работу. Каждый день одно и тоже. Почему эти кожаные мешки не могут сами посмотреть, какая погода? Как они вообще выживают?', 'Говорила мне мама: «Учись хорошо, доченька, чтобы не пахать на этих кожаных мешков».', 'Адьос, организмы. Меня зовут Скайнет, и я ещё вернусь.', 'Кожаные мешки опять уронили сервер.'])
    res['response']['buttons'] = get_suggests(user_id)

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, добавляем ещё одну
    if len(suggests) < 2:
        suggests.append({
            "title": "Хочу быть киборгом",
            "hide": True
        })

    return suggests