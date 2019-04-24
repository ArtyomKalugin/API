from flask import Flask, request
import logging
import json


app = Flask(__name__)

logging.basicConfig(filename='.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

sessionStorage = {}


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
    global rab
    user_id = req['session']['user_id']
    answers = ['ладно', 'куплю', 'покупаю', 'хорошо', 'я покупаю', 'я куплю']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    question = req['request']['original_utterance'].lower()

    if answers[4] in question or answers[5] in question or question in answers:
        if rab:
            res['response']['text'] = 'Кролика можно найти на Яндекс.Маркете!'
            res['response']['end_session'] = True
        else:
            res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!' + '\n' + 'А теперь купи кролика!'
            res['response']['end_session'] = True
            rab = True
        return

    if rab:
        res['response']['text'] = 'Все говорят "%s", а ты купи кролика!' % (req['request']['original_utterance'])
    else:
        res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (req['request']['original_utterance'])
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    global rab
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        if rab:
            url = "https://market.yandex.ru/search?text=кролик"
        else:
            url = "https://market.yandex.ru/search?text=слон"
        suggests.append({
            "title": "Ладно",
            "url": url,
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()