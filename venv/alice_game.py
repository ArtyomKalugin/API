from flask import Flask, request
import logging
import json
import random
from cards import cards
from gamers import Gamer


app = Flask(__name__)

logging.basicConfig(filename='alice_game.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

sessionStorage = {}
names = ['Вы', 'Алиса', 'Бот Андрей']
begin = True
rules = False
game = False
now = None


def spread():
    for i in range(12):
        me.add_card(cards.pop(random.choce(range(len(cards)))))
        sec.add_card(cards.pop(random.choce(range(len(cards)))))
        user.add_card(cards.pop(random.choce(range(len(cards)))))


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', request.json)

    return json.dumps(response)


def handle_dialog(req, res):
    global begin, game, rules
    #res['response']['end_session'] = True

    user_id = req['session']['user_id']
    mis = ['Ты уверен? Давай все-таки сыграем!', 'Ну давай сыграем!', 'Давай играть!']
    answers = ['хорошо', 'давай', 'я согласен', 'начинай', 'хочу', 'окей', 'да']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = 'Привет! Давай сыграем в "сундучки"?'
        res['response']['buttons'] = get_suggests(user_id)
        return

    question = req['request']['original_utterance'].lower()

    if question in answers:
        if begin:
            res['response']['text'] = 'Начинаем! Хотите ознакомиться с правилами?'
            begin = False
            rules = True
            return

        if rules:
            res['response']['text'] = 'Вот тут правила!'
            res['response']['card'] = {"type": "BigImage",
                                        "image_id": "965417/a734b446e4c419cf014d",
                                        "title": "Правила игры",
                                        "description": "Правилы игры в сундучки",
                                        "button": {"text": "Правила",
                                                    "url": "http://127.0.0.1:8080/rules",
                                                    "payload": {}}}

            me = Gamer(3)
            sec = Gamer(3)
            user = Gamer(3)
            spread()
            now = random.choice(range(1, 4))

            rules = False
            game = True
            return

    if game:
        message = 'Ходит: ' + names[now - 1]
        if now == 1:
            pass
        #res['response']['text'] = 'Ходит: ' + names[now - 1]

    if begin:
        res['response']['text'] = random.choice(mis)
        return
    elif rules:
        me = Gamer(3)
        sec = Gamer(3)
        user = Gamer(3)
        spread()
        now = random.choice(range(1, 4))

        res['response']['text'] = 'Приступаем!'

        rules = False
        game = True
    else:
        res['response']['text'] = 'Я не совсем тебя поняла. Попробуй еще один раз.'
        return
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        url = "https://market.yandex.ru/search?text=слон"
        suggests.append({
            "title": "Ладно",
            "url": url,
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()