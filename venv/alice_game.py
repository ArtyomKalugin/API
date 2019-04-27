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
names = ['Вы', 'Алиса', 'Андрей']
message = ''
begin = True
rules = False
game = False
turn_value = False
turn_num = False
turn_suit = False
turn_name = None
turn_bot = False
turn_turn = True
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

    user_id = req['session']['user_id']
    mis = ['Ты уверен? Давай все-таки сыграем!', 'Ну давай сыграем!', 'Давай играть!']
    answers = ['хорошо', 'давай', 'я согласен', 'начинай', 'хочу', 'окей', 'да']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Давай сыграем в "сундучки"?'
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

            alice = Gamer(3)
            bot = Gamer(3)
            user = Gamer(3)
            spread()
            now = random.choice(range(1, 4))

            rules = False
            game = True
            return

    if game:
        if len(user.show_cards()) == 1:
            res['response']['text'] = 'Вы вышли из игры'
            res['response']['end_session'] = True


        sessionStorage[user_id] = {
            'suggests': user.show_cards()
        }
        res['response']['buttons'] = get_suggests(user_id)

        if now > 3:
            now = 1

        if now == 1:
            if turn_value:
                name, value = question.split()[0], question.split()[1]

                if name.lower() == 'алиса':
                    if alice.check_exit():
                        message = 'Алиса вышла из игры! Выберите другого игрока!'
                    else:
                        response = alice.get_answer(value=value)
                        if response == 'Нету':
                            message = 'Алиса: Нету' + '\n' + 'Ваш ход окончен'
                            now += 1
                            turn_value = False
                            bot.change_enemy_cards(2, value=(value, False))
                            alice.change_enemy_cards()
                        else:
                            message = 'Алиса: Есть'
                            turn_value = False
                            turn_num = True
                            bot.change_enemy_cards(2, value=(value, True))
                            turn_name = 'алиса'

                if name.lower() == 'андрей':
                    if bot.check_exit():
                        message = 'Андрей вышел из игры! Выберите другого игрока!'
                    else:
                        response = bot.get_answer(value=value)
                        if response == 'Нету':
                            message = 'Андрей: Нету' + '\n' + 'Ваш ход окончен'
                            now += 1
                            turn_value = False
                            alice.change_enemy_cards(2, value=(value, False))
                        else:
                            message = 'Андрей: Есть'
                            turn_value = False
                            turn_num = True
                            alice.change_enemy_cards(2, value=(value, True))
                            turn_name = 'андрей'

            else:
                message = 'Ваш ход'
                turn_value = True

            if turn_num:
                num = question

                if turn_name == 'алиса':
                        response = alice.get_answer(num=num)
                        if response == 'Нет':
                            message = 'Алиса: Нет' + '\n' + 'Ваш ход окончен'
                            now += 1
                            turn_num = False
                            bot.change_enemy_cards(2, num=(num, False))
                        else:
                            message = 'Алиса: Да'
                            turn_num = False
                            turn_suit = True
                            bot.change_enemy_cards(2, num=(num, True))

                if turn_name == 'андрей':
                        response = bot.get_answer(nun=num)
                        if response == 'Нет':
                            message = 'Андрей: Нет' + '\n' + 'Ваш ход окончен'
                            now += 1
                            turn_num = False
                            alice.change_enemy_cards(2, num=(num, False))
                        else:
                            message = 'Андрей: Да'
                            turn_num = False
                            turn_suit = True
                            alice.change_enemy_cards(2, num=(num, True))

            if turn_suit:
                suit = question

                if turn_name == 'алиса':
                        response = alice.get_answer(suit=suit)
                        if response == 'Нет':
                            message = 'Алиса: Нет' + '\n' + 'Ваш ход окончен'
                            now += 1
                            turn_suit = False
                            bot.change_enemy_cards(2, suit=(suit, False))
                        else:
                            message = 'Алиса: Да' + '\n' + 'Передаю карты вам'
                            turn_suit = False
                            bot.change_enemy_cards(2, suit=(suit, True))

                            if len(response.strip()) > 3:
                                user.add_card(response.strip(), many=True)
                            else:
                                user.add_card(response.strip())
                            user.check_chest()

                if turn_name == 'андрей':
                        response = bot.get_answer(suit=suit)
                        if response == 'Нет':
                            message = 'Андрей: Нет' + '\n' + 'Ваш ход окончен'
                            now += 1
                            turn_suit = False
                            alice.change_enemy_cards(2, suit=(suit, False))
                        else:
                            message = 'Андрей: Да' + '\n' + 'Передаю карты вам'
                            turn_suit = False
                            alice.change_enemy_cards(2, suit=(suit, True))

                            if len(response.strip()) > 3:
                                user.add_card(response, many=True)
                            else:
                                user.add_card(response)
                            user.check_chest()

        if now == 2:
            if turn_value:
                turn_name, value = alice.make_choice(value=True)

                if turn_name == 2:
                    if bot.check_exit():
                        turn_name = 1
                        turn_bot = False
                    else:
                        turn_bot = True
                        message += '- Андрей, у тебя есть ' + value + '?' + '\n'
                        response = bot.get_answer(value=value)
                        if response == 'Нету':
                            message += '- Нету' + '\n' + 'Ход Алисы закончен'
                            now += 1
                            alice.change_enemy_cards(turn_name, value=(value, False))
                        else:
                            message += '- Есть' + '\n'
                            alice.change_enemy_cards(turn_name, value=(value, True))

                if turn_name == 1:
                    turn_bot = False

                    if turn_turn:
                        message = 'Алиса: Пользователь, у вас есть ' + value + '?'
                        turn_turn = False
                    else:
                        if question == 'да':
                            bot.change_enemy_cards(1, value=(value, True))
                            alice.change_enemy_cards(1, value=(value, True))
                            turn_value = False
                            turn_num = True

                        else:
                            bot.change_enemy_cards(1, value=(value, False))
                            alice.change_enemy_cards(1, value=(value, True))
                            now += 1
                            turn_value = False
                            message = 'Ход Алисы окончен'
                        turn_turn = True
            else:
                message = 'Ходит Алиса'
                turn_value = True

            if turn_num:
                num = alice.make_choice(num=True)

                if turn_name == 2:
                    turn_bot = True
                    message += '- И их ' + num + 'шт?' + '\n'
                    response = bot.get_answer(num=num)
                    if response == 'Нет':
                        message += '- Нет' + '\n' + 'Ход Алисы закончен'
                        now += 1
                        alice.change_enemy_cards(turn_name, num=(num, False))
                    else:
                        message += '- Да' + '\n'
                        alice.change_enemy_cards(turn_name, num=(num, True))

                if turn_name == 1:
                    turn_bot = False

                    if turn_turn:
                        message = 'Алиса: И их ' + value + 'шт?'
                        turn_turn = False
                    else:
                        if question == 'да':
                            bot.change_enemy_cards(1, num=(num, True))
                            alice.change_enemy_cards(1, num=(num, True))
                            turn_num = False
                            turn_suit = True

                        else:
                            bot.change_enemy_cards(1, num=(num, False))
                            alice.change_enemy_cards(1, num=(num, True))
                            now += 1
                            turn_num = False
                            message = 'Ход Алисы окончен'
                        turn_turn = True

            if turn_suit:
                suit = alice.make_choice(suit=True)

                if turn_name == 2:
                    turn_bot = True
                    message += '- Это' + suit + '?' + '\n'
                    response = bot.get_answer(suit=suit)
                    if response == 'Нет':
                        message += '- Нет' + '\n' + 'Ход Алисы закончен'
                        now += 1
                        alice.change_enemy_cards(turn_name, suit=(suit, False))
                    else:
                        message += '- Да' + '\n' + 'Ход Алисы закончен'
                        alice.change_enemy_cards(turn_name, suit=(suit, True))
                        now += 1
                        turn_bot = False

                if turn_name == 1:
                    turn_bot = False

                    if turn_turn:
                        message = 'Алиса: Это ' + suit + '?'
                        turn_turn = False
                    else:
                        if question == 'да':
                            bot.change_enemy_cards(1, suit=(suit, True))
                            alice.change_enemy_cards(1, suit=(suit, True))
                            alice.check_chest()
                        else:
                            bot.change_enemy_cards(1, suit=(suit, False))
                            alice.change_enemy_cards(1, suit=(suit, True))
                        now += 1
                        turn_num = False
                        message = 'Ход Алисы окончен'
                        turn_turn = True
        if now == 3:
            if turn_value:
                turn_name, value = bot.make_choice(value=True)

                if turn_name == 2:
                    if alice.check_exit():
                        turn_name = 1
                        turn_bot = False
                    else:
                        turn_bot = True
                        message += '- Алиса, у тебя есть ' + value + '?' + '\n'
                        response = alice.get_answer(value=value)
                        if response == 'Нету':
                            message += '- Нету' + '\n' + 'Ход Андрея закончен'
                            now += 1
                            bot.change_enemy_cards(turn_name, value=(value, False))
                        else:
                            message += '- Есть' + '\n'
                            bot.change_enemy_cards(turn_name, value=(value, True))

                if turn_name == 1:
                    turn_bot = False

                    if turn_turn:
                        message = 'Андрей: Пользователь, у вас есть ' + value + '?'
                        turn_turn = False
                    else:
                        if question == 'да':
                            bot.change_enemy_cards(1, value=(value, True))
                            alice.change_enemy_cards(1, value=(value, True))
                            turn_value = False
                            turn_num = True

                        else:
                            bot.change_enemy_cards(1, value=(value, False))
                            alice.change_enemy_cards(1, value=(value, True))
                            now += 1
                            turn_value = False
                            message = 'Ход Андрей окончен'
                        turn_turn = True
            else:
                message = 'Ходит Андрей'
                turn_value = True

            if turn_num:
                num = bot.make_choice(num=True)

                if turn_name == 2:
                    turn_bot = True
                    message += '- И их ' + num + 'шт?' + '\n'
                    response = alice.get_answer(num=num)
                    if response == 'Нет':
                        message += '- Нет' + '\n' + 'Ход Андрея закончен'
                        now += 1
                        bot.change_enemy_cards(turn_name, num=(num, False))
                    else:
                        message += '- Да' + '\n'
                        bot.change_enemy_cards(turn_name, num=(num, True))

                if turn_name == 1:
                    turn_bot = False

                    if turn_turn:
                        message = 'Андрей: И их ' + value + 'шт?'
                        turn_turn = False
                    else:
                        if question == 'да':
                            bot.change_enemy_cards(1, num=(num, True))
                            alice.change_enemy_cards(1, num=(num, True))
                            turn_num = False
                            turn_suit = True

                        else:
                            bot.change_enemy_cards(1, num=(num, False))
                            alice.change_enemy_cards(1, num=(num, True))
                            now += 1
                            turn_num = False
                            message = 'Ход Андрея окончен'
                        turn_turn = True

            if turn_suit:
                suit = bot.make_choice(suit=True)

                if turn_name == 2:
                    turn_bot = True
                    message += '- Это' + suit + '?' + '\n'
                    response = alice.get_answer(suit=suit)
                    if response == 'Нет':
                        message += '- Нет' + '\n' + 'Ход Андрея закончен'
                        now += 1
                        bot.change_enemy_cards(turn_name, suit=(suit, False))
                    else:
                        message += '- Да' + '\n' + 'Ход Андрея закончен'
                        bot.change_enemy_cards(turn_name, suit=(suit, True))
                        now += 1
                        turn_bot = False

                if turn_name == 1:
                    turn_bot = False

                    if turn_turn:
                        message = 'Андрей: Это ' + suit + '?'
                        turn_turn = False
                    else:
                        if question == 'да':
                            bot.change_enemy_cards(1, suit=(suit, True))
                            alice.change_enemy_cards(1, suit=(suit, True))
                            bot.check_chest()
                        else:
                            bot.change_enemy_cards(1, suit=(suit, False))
                            alice.change_enemy_cards(1, suit=(suit, True))
                        now += 1
                        turn_num = False
                        message = 'Ход Андрея окончен'
                        turn_turn = True

        if turn_bot is False:
            res['response']['text'] = message
            message = ''
            return

    if begin:
        res['response']['text'] = random.choice(mis)
        return
    elif rules:
        alice = Gamer(3)
        bot = Gamer(3)
        user = Gamer(3)
        spread()
        now = random.choice(range(1, 4))

        res['response']['text'] = 'Приступаем!'

        rules = False
        game = True
    else:
        res['response']['text'] = 'Я не совсем тебя поняла. Попробуй еще один раз.'
        return


if __name__ == '__main__':
    app.run()