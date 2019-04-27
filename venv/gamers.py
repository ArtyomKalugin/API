import random


class Gamer():

    def __init__(self, gamers):
        self.my_cards = []
        self.my_enemy = None
        self.my_card_now = None
        self.my_cards_now = []
        self.first_time = False
        self.num_now = False
        self.exit = False

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

        self.my_cards = sorted(self.my_cards, key=lambda x: int(x.split()[1]))
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

        if len(self.my_cards) == 0:
            self.exit = True

    def show_chest(self):
        return self.chest

    def show_cards(self):
        chests = 'Сундучки:' + str(self.chest)
        return self.my_cards + chests.split()

    def get_answer(self, value=False, suit=False, num=False):
        if value:
            answer = 'Нету'
            for elem in self.my_cards:
                if value == elem.split()[1]:
                    answer = 'Есть'
                    self.suit_answer.append(elem)
                    self.lear_answer.append(elem.split()[0])
                    self.next_answer = True

        if num and self.next_answer:
            answer = 'Нет'
            if int(num) == len(self.suit_answer):
                answer = 'Да'
                self.next_answer = True
            else:
                self.suit_answer = []
                self.next_answer = False

        if suit and self.next_answer:
            quantity = 0
            answer = 'Нет'
            for elem in suit.split():
                if elem in self.lear_answer:
                    quantity += 1

            if quantity == len(self.suit_answer):
                return self.hand_cards()
            else:
                self.suit_answer = []
                self.lear_answer = []
                self.next_answer = False

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

    def change_enemy_cards(self, whom, value=None, suit=None, num=None):
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
                    self.player_cards[self.values_no]['num'] = num[0]
                else:
                    self.player_cards[self.values_no]['num'] = 'not ' + num[0]

            if suit:
                if suit[1]:
                    self.player_cards[self.values_no] = 0
                    self.second_gamer_cards[self.values_no]['suit'] = suit[0]
                    self.second_gamer_cards[self.values_no]['num'] = str(len(suit[0].split())) + '+'
                else:
                    self.player_cards[self.values_no]['suit'] = 'not ' + suit[0]
                    self.second_gamer_cards[self.values_no]['suit'] = 'notonly ' + suit[0]

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
                    self.second_gamer_cards[self.values_no]['num'] = num[0]
                else:
                    self.second_gamer_cards[self.values_no]['num'] = 'not ' + num[0]

            if suit:
                if suit[1]:
                    self.second_gamer_cards[self.values_no] = 0
                    self.player_cards[self.values_no]['suit'] = suit[0]
                    self.player_cards[self.values_no]['num'] = str(len(suit[0].split())) + '+'
                else:
                    self.second_gamer_cards[self.values_no]['suit'] = 'not ' + suit[0]
                    self.player_cards[self.values_no]['suit'] = 'notonly ' + suit[0]

    def show_player_cards(self):
        return self.player_cards

    def show_second_cards(self):
        return self.second_gamer_cards

    def make_choice(self, value=None, suit=None, num=None):
        if value:
            self.my_card_now = random.choice(self.my_cards)
            self.count_cards(self.my_card_now)

            if self.my_card.split()[1] in self.player_cards.keys():
                self.my_enemy = 1

                return self.my_enemy, self.my_card_now.split()[1]

            elif self.my_card.split()[1] in self.second_gamer_cards.keys():
                self.my_enemy = 2

                return self.my_enemy, self.my_card_now.split()[1]

            else:
                self.first_time = True
                self.count_cards(self.my_card_now)

                self.my_enemy = random.choice(range(1, 3))

                return self.my_enemy, self.my_card_now.split()[1]

        if num:
            if self.first_time:
                self.change_enemy_cards(self.my_enemy, value=(self.my_card_now.split()[1], True))

                num = len(self.my_cards_now)
                if num == 1:
                    self.num_now = random.choice(range(1, 4))
                if num == 2:
                    self.num_now = random.choice(range(1, 3))
                if num == 3:
                    self.num_now = 1

                return self.num_now

            elif self.my_enemy == 1:
                num = self.player_cards[self.my_card_now.split()[1]]['num']
                if num:
                    cards = [1, 2, 3, 4]
                    del cards[:len(self.my_cards_now)]
                    if num.split()[0] == 'not':
                        number = random.choice(range(5 - len(self.my_cards_now)))
                        if str(number) == num.split()[1]:
                            while str(number) == num.split()[1]:
                                number = random.choice(range(5 - len(self.my_cards_now)))
                        self.num_now = number
                    else:
                        self.num_now = num
                else:
                    num = len(self.my_cards_now)
                    if num == 1:
                        self.num_now = random.choice(range(1, 4))
                    if num == 2:
                        self.num_now = random.choice(range(1, 3))
                    if num == 3:
                        self.num_now = 1

                return str(self.num_now)

        if suit:
            lear = ['к', 'ч', 'п', 'б']
            choice = []
            if self.first_time:
                self.change_enemy_cards(self.my_enemy, num=(self.num_now, True))

                num = len(self.my_cards_now)
                if num == 1:
                    color = self.my_card_now.split()[0]
                    del lear[lear.index(color)]
                if num == 2 or num == 3:
                    for elem in self.my_cards_now:
                        del lear[lear.index(elem.split()[0])]

                for i in range(self.num_now):
                    choice.append(random.choice(lear))

                return choice

    def count_cards(self, card):
        for elem in self.my_cards:
            if card.split()[1] == elem.split()[1]:
                self.my_cards_now.append(elem)

    def check_exit(self):
        return self.exit


a = Gamer(3)
a.add_card('п 6')
a.add_card('п 7')
a.add_card('ч 7')
a.add_card('к 7')
a.add_card('к 6')
a.add_card('б 7')
a.add_card('ч 10')
a.add_card('б 10')
a.check_chest()
print(a.show_cards())
print()
print(a.get_answer(value='6'))
print(a.get_answer(num='2'))
print(a.get_answer(suit='к п'))
print()
print(a.show_cards())




