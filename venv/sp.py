import logging
import json
import random
from cards import cards
from gamers import Gamer


def spread(arrow):
    for i in range(4):
        for elem in arrow:
            card = cards.pop(random.choice(range(len(cards))))
            elem.add_card(card)

sessionStorage = {}

alice = Gamer(3)
bot = Gamer(3)
user = Gamer(3)

spread([alice, bot, user])

alice.check_chest()
bot.check_chest()
user.check_chest()
now = random.choice(range(1, 4))


names = ['Вы', 'Алиса', 'Андрей']
message = ''
begin = True
rules = False
game = False
turn_value = False
turn_num = False
turn_suit = False
turn_name = None
turn_turn = True
who_turned = True


def handle_dialog(req):
    global begin, game, rules, turn_value, turn_num, turn_suit, turn_name, turn_turn, now, message, names, alice, bot, user, sessionStorage, who_turned

    mis = ['Ты уверен? Давай все-таки сыграем!', 'Ну давай сыграем!', 'Давай играть!']
    answers = ['хорошо', 'давай', 'я согласен', 'начинай', 'хочу', 'окей', 'да', 'ок', 'го', 'поехали', 'погнали']

    question = req.lower()

    if question in answers:
        if begin:
            print('Играем на 12 карт и сразу раздаем всю колоду! Отвечать на вопросы ботов следует "да" или "нет". В начале хода писать сначала имя, потом номинал карты первой буквой номинала, например: ' \
                                      'Алиса т (Означает: Алиса, есть ли у тебя тузы?)' + '\n' + 'Дальше пишем количество, например: 5' + '\n' + 'После ' \
                                      'количества пишем масти, также первой буквой и через пробел, например: к п (Это крести и пики?)' + '\n' + 'Имя, на ' \
                                      'Кого вы ходите пишется только в начале хода, дальще его указывать не нужно. После любого хода следует писать "ок".' + '\n' + 'Хотите ' \
                                      'ли вы ознакомиться с правилами игры в "сундучки"?')

            begin = False
            rules = True
            return

        if rules:
            print('Вот тут правила!')
            rules = False
            game = True
            turn_value = True
            return

    if game:
        print(user.show_cards())
        if len(user.show_cards()) == 1:
            print('Вы вышли из игры')
            return

        if now > 3:
            now = 1

        if who_turned:
            if now == 1:
                print('Ваш ход')
            elif now == 2:
                print('Ход Алисы')
            elif now == 3:
                print('Ход Андрея')

            turn_value = True
            who_turned = False
            return

        if now == 1:
            if turn_value:
                name, value = question.split()[0], question.split()[1]
                if name.lower() == 'алиса':
                    if alice.check_exit():
                        print('Алиса вышла из игры! Выберите другого игрока!')
                        return
                    else:
                        response = alice.get_answer(value=value)
                        alice.change_enemy_cards(1, value=(value, True))
                        if response == 'Нету':
                            print('Алиса: Нету' + '\n' + 'Ваш ход окончен')
                            now += 1
                            turn_value = False
                            bot.change_enemy_cards(2, value=(value, False))
                            who_turned = True
                        else:
                            print('Алиса: Есть')
                            turn_value = False
                            turn_num = True
                            bot.change_enemy_cards(2, value=(value, True))
                            turn_name = 'алиса'
                            return

                if name.lower() == 'андрей':
                    if bot.check_exit():
                        print('Андрей вышел из игры! Выберите другого игрока!')
                    else:
                        response = bot.get_answer(value=value)
                        bot.change_enemy_cards(2, value=(value, True))
                        if response == 'Нету':
                            print('Андрей: Нету' + '\n' + 'Ваш ход окончен')
                            now += 1
                            turn_value = False
                            alice.change_enemy_cards(2, value=(value, False))
                            who_turned = True
                        else:
                            print('Андрей: Есть')
                            turn_value = False
                            turn_num = True
                            alice.change_enemy_cards(2, value=(value, True))
                            turn_name = 'андрей'
                            return

            if turn_num:
                num = question

                if turn_name == 'алиса':
                        response = alice.get_answer(num=num)
                        if response == 'Нет':
                            print('Алиса: Нет' + '\n' + 'Ваш ход окончен')
                            now += 1
                            turn_num = False
                            bot.change_enemy_cards(2, num=(num, False))
                            who_turned = True
                        else:
                            print('Алиса: Да')
                            turn_num = False
                            turn_suit = True
                            bot.change_enemy_cards(2, num=(num, True))
                            return

                if turn_name == 'андрей':
                        response = bot.get_answer(num=num)
                        if response == 'Нет':
                            print('Андрей: Нет' + '\n' + 'Ваш ход окончен')
                            now += 1
                            turn_num = False
                            alice.change_enemy_cards(2, num=(num, False))
                            who_turned = True
                        else:
                            print('Андрей: Да')
                            turn_num = False
                            turn_suit = True
                            alice.change_enemy_cards(2, num=(num, True))
                            return

            if turn_suit:
                suit = question

                if turn_name == 'алиса':
                        response = alice.get_answer(suit=suit)
                        if response == 'Нет':
                            print('Алиса: Нет' + '\n' + 'Ваш ход окончен')
                            now += 1
                            turn_suit = False
                            who_turned = True
                        else:
                            print('Алиса: Да' + '\n' + 'Передаю карты вам')
                            turn_suit = False

                            if len(response.strip()) > 2:
                                user.add_card(response.strip(), many=True)
                            else:
                                user.add_card(response.strip())
                            user.check_chest()
                            turn_turn = True
                            who_turned = True
                            return

                if turn_name == 'андрей':
                        response = bot.get_answer(suit=suit)
                        if response == 'Нет':
                            print('Андрей: Нет' + '\n' + 'Ваш ход окончен')
                            now += 1
                            turn_suit = False
                            who_turned = True
                        else:
                            print('Андрей: Да' + '\n' + 'Передаю карты вам')
                            turn_suit = False

                            if len(response.strip()) > 2:
                                user.add_card(response, many=True)
                            else:
                                user.add_card(response)
                            user.check_chest()
                            turn_turn = True
                            who_turned = True
                            return

        if now == 2:
            if turn_value:
                turn_name, value = alice.make_choice(value=True)
                if turn_name == 2:
                    if bot.check_exit():
                        turn_name = 1
                    else:
                        print('- Андрей, у тебя есть ' + value + '?')
                        response = bot.get_answer(value=value)
                        if response == 'Нету':
                            print('- Нету' + '\n' + 'Ход Алисы закончен')
                            now += 1
                            turn_value = False
                            alice.change_enemy_cards(turn_name, value=(value, False))
                            who_turned = True
                        else:
                            print('- Есть')
                            alice.change_enemy_cards(turn_name, value=(value, True))
                            turn_value = False
                            turn_num = True
                        bot.change_enemy_cards(2, value=(value, True))

                if turn_name == 1:
                    response = user.get_answer(value=value)

                    if turn_turn:
                        print('Алиса: Пользователь, у вас есть ' + value + '?')
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
                            print('Ход Алисы окончен')
                            who_turned = True
                        turn_turn = True

            if turn_num:
                num = alice.make_choice(num=True)
                if turn_name == 2:
                    print('- И их ' + num + 'шт?')
                    response = bot.get_answer(num=num)
                    if response == 'Нет':
                        print('- Нет' + '\n' + 'Ход Алисы закончен')
                        now += 1
                        alice.change_enemy_cards(turn_name, num=(num, False))
                        turn_num = False
                        who_turned = True
                    else:
                        print('- Да')
                        alice.change_enemy_cards(turn_name, num=(num, True))
                        turn_num = False
                        turn_suit = True

                if turn_name == 1:
                    response = user.get_answer(num=num)
                    if turn_turn:
                        print('Алиса: И их ' + num + 'шт?')
                        turn_turn = False
                    else:
                        if question == 'да':
                            bot.change_enemy_cards(1, num=(num, True))
                            alice.change_enemy_cards(1, num=(num, True))
                            turn_num = False
                            turn_suit = True

                        else:
                            bot.change_enemy_cards(1, num=(num, False))
                            alice.change_enemy_cards(1, num=(num, False))
                            now += 1
                            turn_num = False
                            print('Ход Алисы окончен')
                            who_turned = True
                        turn_turn = True

            if turn_suit:
                suit = alice.make_choice(suit=True)

                if turn_name == 2:
                    print('- Это' + ' ' + ' '.join(suit) + '?')
                    response = bot.get_answer(suit=suit)
                    if response == 'Нет':
                        print('- Нет' + '\n' + 'Ход Алисы закончен')
                        now += 1
                        who_turned = True
                    else:
                        print('- Да')
                        who_turned = True
                        if len(response.split()) > 2:
                            alice.add_card(response, many=True)
                        else:
                            alice.add_card(response)
                        alice.check_chest()


                if turn_name == 1:
                    response = esponse = user.get_answer(suit=suit)
                    if turn_turn:
                        print('Алиса: Это ' + ' '.join(suit) + '?')
                        turn_turn = False
                    else:
                        if question == 'да':
                            if len(response.split()) > 2:
                                alice.add_card(response.strip(), many=True)
                            else:
                                alice.add_card(response.strip())
                            alice.check_chest()
                            who_turned = True
                            turn_suit = False
                        else:
                            now += 1
                            print('Ход Алисы окончен')
                            who_turned = True
                            turn_suit = False
                        turn_turn = True

        if now == 3:
            if turn_value:
                turn_name, value = bot.make_choice(value=True)
                if turn_name == 2:
                    if alice.check_exit():
                        turn_name = 1
                    else:
                        print('- Алиса, у тебя есть ' + value + '?')
                        response = alice.get_answer(value=value)
                        if response == 'Нету':
                            print('- Нету' + '\n' + 'Ход Андрея закончен')
                            now += 1
                            turn_value = False
                            bot.change_enemy_cards(turn_name, value=(value, False))
                            who_turned = True
                        else:
                            message += '- Есть' + '\n'
                            bot.change_enemy_cards(turn_name, value=(value, True))
                            turn_value = False
                            turn_num = True
                        alice.change_enemy_cards(2, value=(value, True))

                if turn_name == 1:
                    response = user.get_answer(value=value)
                    if turn_turn:
                        print('Андрей: Пользователь, у вас есть ' + value + '?')
                        turn_turn = False
                    else:
                        if question == 'да':
                            bot.change_enemy_cards(1, value=(value, True))
                            alice.change_enemy_cards(1, value=(value, True))
                            turn_value = False
                            turn_num = True

                        else:
                            bot.change_enemy_cards(1, value=(value, False))
                            alice.change_enemy_cards(1, value=(value, False))
                            now += 1
                            turn_value = False
                            print('Ход Андрея окончен')
                            who_turned = True
                        turn_turn = True

            if turn_num:
                num = bot.make_choice(num=True)
                if turn_name == 2:
                    print('- И их ' + num + 'шт?')
                    response = alice.get_answer(num=num)
                    if response == 'Нет':
                        print('- Нет' + '\n' + 'Ход Андрея закончен')
                        now += 1
                        bot.change_enemy_cards(turn_name, num=(num, False))
                        turn_num = False
                        who_turned = True
                    else:
                        print('- Да')
                        bot.change_enemy_cards(turn_name, num=(num, True))
                        turn_num = False
                        turn_suit = True

                if turn_name == 1:
                    response = user.get_answer(num=num)
                    if turn_turn:
                        print('Андрей: И их ' + num + 'шт?')
                        turn_turn = False
                    else:
                        if question == 'да':
                            bot.change_enemy_cards(1, num=(num, True))
                            alice.change_enemy_cards(1, num=(num, True))
                            turn_num = False
                            turn_suit = True

                        else:
                            bot.change_enemy_cards(1, num=(num, False))
                            alice.change_enemy_cards(1, num=(num, False))
                            now += 1
                            turn_num = False
                            print('Ход Андрея окончен')
                            who_turned = True
                        turn_turn = True

            if turn_suit:
                suit = bot.make_choice(suit=True)
                if turn_name == 2:
                    print('- Это' + ' '.join(suit) + '?')
                    response = alice.get_answer(suit=suit)
                    if response == 'Нет':
                        print('- Нет' + '\n' + 'Ход Андрея закончен')
                        now += 1
                        who_turned = True
                    else:
                        print('- Да')

                        if len(response.split()) > 2:
                            bot.add_card(response, many=True)
                        else:
                            bot.add_card(response)
                        bot.check_chest()
                        who_turned = True

                if turn_name == 1:
                    response = user.get_answer(suit=suit)
                    if turn_turn:
                        print('Андрей: Это ' + ' ' + ' '.join(suit) + '?')
                        turn_turn = False
                    else:
                        if question == 'да':
                            if len(response.split()) > 2:
                                bot.add_card(response, many=True)
                            else:
                                bot.add_card(response)
                            bot.check_chest()
                            who_turned = True
                            turn_suit = False
                        else:
                            now += 1
                            turn_turn = True
                            who_turned = True
                            print('Ход Андрея окончен')
                            turn_suit = False
                        turn_turn = True

        return

    if begin:
        print(random.choice(mis))
        return
    if rules:
        print('Приступаем!')
        rules = False
        game = True
        turn_value = True
        return
    else:
        print('Я не совсем тебя поняла. Попробуй еще один раз.')
        return

while True:
    handle_dialog(input())
