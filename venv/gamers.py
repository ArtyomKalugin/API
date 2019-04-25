import random


class Gamer():

    def __init__(self, gamers):
        my_cards = []
        second_gamer_cards = []
        player_cards = []

        for i in range(36 / gamers):
            second_gamer_cards.append('? ?')
            player_cards.append('? ?')

    def add_card(self, card):
        my_cards.append(card)


