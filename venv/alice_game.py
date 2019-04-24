from flask import Flask, request
import logging
import json
import random
from answers import answers, situations
from get_bonuse import bonuse


app = Flask(__name__)

logging.basicConfig(filename='.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

sessionStorage = {}
move = 0
sit = 0
life = 100
bon = [0, 0]
begin = True
child = False
junior = False
yoth = False


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
    # res['response']['end_session'] = True

    user_id = req['session']['user_id']
    mis = ['Ты уверен? Давай все-таки сыграем!', 'Ну давай сыграем!', 'Давай играть!']
    answers = answers[move]

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = 'Привет! Давай сыграем в игру?'
        res['response']['buttons'] = get_suggests(user_id)
        return

    question = req['request']['original_utterance'].lower()



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