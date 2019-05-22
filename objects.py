import pygame
import random
from config import Config
import os


class Deck():
    _suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    _ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]

    def __init__(self, display):
        self.cards = [Card(s, r) for s in self._suits for r in self._ranks]
        self.shuffle()
        self.display = display
        _deck = os.path.abspath(Config["deck"]["img"])
        _image = pygame.image.load(_deck)
        _image_size = _image.get_size()
        _sizes = (int(_image_size[0]/1.4), int(_image_size[1]/1.4))
        _resize_img = pygame.transform.scale(_image, _sizes)
        self.deck_img = _resize_img

    def draw(self):
        self.display.blit(self.deck_img, (Config["deck"]["x"], Config["deck"]["y"]))

    def deal(self):
        return self.cards.pop()

    def shuffle(self):
        random.shuffle(self.cards)


class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        _pre = Config["card"]["pre"]
        _dir = Config["card"]["dir"]
        _image = pygame.image.load(_dir+_pre+self.suit+str(self.rank)+".png")
        _image_size = _image.get_size()
        _sizes = (int(_image_size[0]/1.4), int(_image_size[1]/1.4))
        _resize_img = pygame.transform.scale(_image, _sizes)
        self.card_img = _resize_img
        self.hidden = False

        if self.rank in ["J", "Q", "K"]:
            self.val = 10
        elif self.rank == "A":
            self.val = 11
        else:
            self.val = int(self.rank)

    def __str__(self):
        if self.hidden:
            return "[X]"
        else:
            return "[{} of {}]".format(self.rank, self.suit)

    def show(self):
        return "{} of {}".format(self.rank, self.suit)

    def is_ace(self):
        return self.val == 1

    def hide_card(self):
        self.hidden = True

    def reveal_card(self):
        self.hidden = False

    def is_hidden(self):
        return self.hidden == True


class Hand(object):
    def __init__(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)
        return self.hand

    def get_values(self):
        aces = 0
        value = 0
        for card in self.hand:
            if card.is_ace():
                aces += 1
            value += card.val
        while (value > 21) and aces:
            value -= 10
            aces -= 1
        return value


class Player(Hand):
    def __init__(self, name, deck):
        Hand.__init__(self)
        self.name = name
        self.deck = deck
        self.bust = False
        self.card_span = 25
        _deck = os.path.abspath(Config["deck"]["img"])
        _image = pygame.image.load(_deck)
        _image_size = _image.get_size()
        _sizes = (int(_image_size[0]/1.4), int(_image_size[1]/1.4))
        _resize_img = pygame.transform.scale(_image, _sizes)
        self.deck_img = _resize_img

    def __str__(self):
        return str(self.name).capitalize()

    def show_hand(self):
        _hand = []
        _imgs = []
        for c in self.hand:
            _hand.append(c.__str__())
            # print(c, c.suit, c.rank, c.card_img)
            _imgs.append(c)
        # print(", ".join(_hand))
        return _imgs

    def hit(self):
        self.add_card(self.deck.deal())
        return self.hand

    def check_bust(self):
        if self.get_values > 21:
            self.bust = True
            print("{} busted!".format(self.__str__()))

    def draw_card(self, display, player, card, x, y):
        if player == "Dealer":
            _y = (card.card_img.get_size()[1]/2)/2
            print(player, card.is_hidden(), x, _y)
            _img = card.card_img
            if card.is_hidden():
                _img = self.deck_img

            display.blit(_img, (x, _y))
        else:
            # print(player, card.card_img, x, y)
            display.blit(card.card_img, (x, y))
