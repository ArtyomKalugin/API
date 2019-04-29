import random


class Gamer():

    def __init__(self, gamers):
        self.my_cards = []
        self.my_enemy = None
        self.my_card_now = None
        self.my_cards_now = []
        self.first_time = False
        self.num_now = 0
        self.exit = False
        self.one_card = False

        self.second_gamer_cards = {}
        self.player_cards = {}
        self.values_no = None

        self.chest = 0

        self.lear_answer = []
        self.suit_answer = []
        self.next_answer = False

    def add_card(self, card, many=False):
        if many:
            for elem in card.split(', '):
                self.my_cards.append(elem.strip())
        else:
            self.my_cards.append(card)

        print(self.my_cards, 'LOl')
        self.my_cards = sorted(self.my_cards, key=lambda x: x.split()[1])
        self.check_chest()

    def check_chest(self):
        run = 0
        check = None
        card_start = 0
        minus_i = 0
        for i in range(len(self.my_cards)):
            if i == 0:
                check = self.my_cards[i - minus_i * 4].split()[1]
                run = 1
                card_start = i
            else:
                if check == self.my_cards[i - minus_i * 4].split()[1]:
                    run += 1
                else:
                    check = self.my_cards[i - minus_i * 4].split()[1]
                    run = 1
                    card_start = i

            if run == 4:
                self.chest += 1
                del self.my_cards[card_start: i + 1]
                minus_i += 1
                self.one_card = False

        if len(self.my_cards) == 0:
            self.exit = True

    def show_chest(self):
        return self.chest

    def show_cards(self):
        chests = 'Сундучки:' + str(self.chest)
        return self.my_cards + chests.split()

    def get_answer(self, value=False, suit=False, num=False):
        answer = ''
        if value:
            answer = 'Нету'
            for elem in self.my_cards:
                if value == elem.split()[1]:
                    answer = 'Есть'
                    self.suit_answer.append(elem)
                    self.lear_answer.append(elem.split()[0])

        if num:
            answer = 'Нет'
            if int(num) == len(self.suit_answer):
                answer = 'Да'
                self.next_answer = True
            else:
                self.suit_answer = []

        if suit:
            quantity = 0
            answer = 'Нет'

            if type(suit) is list:
                for elem in suit:
                    if elem in self.lear_answer:
                        quantity += 1
            else:
                for elem in suit.split():
                    if elem in self.lear_answer:
                        quantity += 1

            if quantity == len(self.suit_answer):
                return self.hand_cards()
            else:
                self.suit_answer = []
                self.lear_answer = []

        return answer

    def hand_cards(self):
        answer = []
        for elem in self.suit_answer:
            answer.append(self.my_cards.pop(self.my_cards.index(elem)))

        answer = ', '.join(answer)

        self.suit_answer = []
        self.lear_answer = []
        self.next_answer = False

        return answer

    def change_enemy_cards(self, whom, value=None, num=None):
        if whom == 1:
            if value:
                self.values_no = value[0]
                if value[1]:
                    if value[0] not in self.player_cards.keys():
                        self.player_cards[value[0]] = {'suit': None, 'num': None}
                else:
                    if value[0] not in self.player_cards.keys():
                        self.player_cards[value[0]] = 0

                if value[0] not in self.second_gamer_cards.keys():
                    self.second_gamer_cards[value[0]] = {'suit': None, 'num': None}

            if num:
                if num[1]:
                    if self.player_cards[self.values_no] != 0:
                        self.player_cards[self.values_no]['num'] = num[0]
                else:
                    if self.player_cards[self.values_no] != 0:
                        self.player_cards[self.values_no]['num'] = 'not ' + num[0]

        if whom == 2:
            if value:
                self.values_no = value[0]
                if value[1]:
                    if value[0] not in self.second_gamer_cards.keys():
                        self.second_gamer_cards[value[0]] = {'suit': None, 'num': None}
                else:
                    if value[0] not in self.second_gamer_cards.keys():
                        self.second_gamer_cards[value[0]] = 0

                if value[0] not in self.player_cards.keys():
                    self.player_cards[value[0]] = {'suit': None, 'num': None}

            if num:
                if num[1]:
                    if self.second_gamer_cards[self.values_no] != 0:
                        self.second_gamer_cards[self.values_no]['num'] = num[0]
                else:
                    if self.second_gamer_cards[self.values_no] != 0:
                        self.second_gamer_cards[self.values_no]['num'] = 'not ' + num[0]

    def show_player_cards(self):
        return self.player_cards

    def show_second_cards(self):
        return self.second_gamer_cards

    def make_choice(self, value=None, suit=None, num=None):
        if value:
            if self.my_card_now in self.my_cards:
                self.one_card = True
            else:
                self.one_cards = False

            if self.one_card is False:
                self.my_card_now = random.choice(self.my_cards)
                self.one_card = True
            self.count_cards(self.my_card_now)

            if self.my_card_now.split()[1] in self.player_cards.keys():
                self.my_enemy = 1

                return self.my_enemy, self.my_card_now.split()[1]

            elif self.my_card_now.split()[1] in self.second_gamer_cards.keys():
                self.my_enemy = 2

                return self.my_enemy, self.my_card_now.split()[1]

            else:
                self.first_time = True
                self.count_cards(self.my_card_now)

                self.my_enemy = random.choice(range(1, 3))

                return self.my_enemy, self.my_card_now.split()[1]

        if num:
            numer = None
            if self.first_time:
                self.change_enemy_cards(self.my_enemy, value=(self.my_card_now.split()[1], True))

                numer = len(self.my_cards_now)
                if numer == 1:
                    self.num_now = random.choice(range(1, 4))
                if numer == 2:
                    self.num_now = random.choice(range(1, 3))
                if numer == 3:
                    self.num_now = 1
            else:
                if self.my_enemy == 1:
                    if self.player_cards[self.my_card_now.split()[1]] != 0:
                        numer = self.player_cards[self.my_card_now.split()[1]]['num']
                if self.my_enemy == 2:
                    if self.second_gamer_cards[self.my_card_now.split()[1]] != 0:
                        numer = self.second_gamer_cards[self.my_card_now.split()[1]]['num']
                if numer:
                    cards = [1, 2, 3, 4]
                    del cards[:len(self.my_cards_now)]
                    if str(numer).split()[0] == 'not':
                        number = random.choice(range(1, 5 - len(self.my_cards_now)))
                        if str(number) == numer.split()[1]:
                            while str(number) == numer.split()[1]:
                                number = random.choice(range(1, 5 - len(self.my_cards_now)))
                        self.num_now = number
                    else:
                        self.num_now = numer
                else:
                    numer = len(self.my_cards_now)
                    if numer == 1:
                        self.num_now = random.choice(range(1, 4))
                    if numer == 2:
                        self.num_now = random.choice(range(1, 3))
                    if numer == 3:
                        self.num_now = 1

            return str(self.num_now)

        if suit:
            lear = ['к', 'ч', 'п', 'б']
            choice = []
            self.change_enemy_cards(self.my_enemy, num=(self.num_now, True))
            num = len(self.my_cards_now)
            if num == 1:
                color = self.my_card_now.split()[0]
                del lear[lear.index(color)]
            if num == 2 or num == 3:
                for elem in self.my_cards_now:
                    del lear[lear.index(elem.split()[0])]

            for i in range(int(self.num_now)):
                guess = random.choice(lear)
                if guess not in choice:
                    choice.append(guess)
                else:
                    while guess in choice:
                        guess = random.choice(lear)
                    choice.append(guess)

            self.first_time = False

            return choice

    def count_cards(self, card):
        self.my_cards_now = []
        for elem in self.my_cards:
            if card.split()[1] == elem.split()[1]:
                self.my_cards_now.append(elem)

    def check_exit(self):
        return self.exit
