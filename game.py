import pygame
from config import Config
from objects import Deck, Player


class Game:

    def __init__(self, display):
        pygame.init()
        pygame.font.init()
        self.font_small = pygame.font.SysFont('Arial Black', 12)
        self.font_large = pygame.font.SysFont('Arial', 32)
        self.display = display
        self.deck = Deck(self.display)
        self.player = Player("Player", self.deck)
        self.dealer = Player("Dealer", self.deck)
        self.w, self.h = self.display.get_size()
        self.rect = pygame.Rect(0, 0, self.w, self.h)

    def loop(self):
        clock = pygame.time.Clock()
        players = []
        players.append(self.player)
        players.append(self.dealer)
        first_hand = True
        hit = False
        _x = 0

        # Filling bg with green gradient
        self.gradient_bg(self.display, self.rect, (34, 139, 34), (0, 100, 0), True, True)

        # Putting deck image on the screen
        self.deck.draw()

        # Dealing first hard of cards
        self.first_hand(players)

        # Drawing the hit and stay button
        self.hit_btn()
        self.stay_btn()

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    _deck_img_size = self.deck.deck_img.get_size()
                    _deck_img = pygame.Rect((Config["deck"]["x"], Config["deck"]["y"]), _deck_img_size)
                    if _deck_img.collidepoint(x, y):
                        # It works... need to implement [Hit] and [Stay] buttons
                        pass

            pygame.display.update()
            clock.tick(Config["game"]["fps"])

    def gradient_bg(self, display, rect, start_color, end_color, vertical=True, forward=True):
        """fill a surface with a gradient pattern
        Parameters:
        color -> starting color
        gradient -> final color
        rect -> area to fill; default is surface's rect
        vertical -> True=vertical; False=horizontal
        forward -> True=forward; False=reverse

        Pygame recipe: http://www.pygame.org/wiki/GradientCode
        """
        if rect is None:
            rect = display.get_rect()
        x1, x2 = rect.left, rect.right
        y1, y2 = rect.top, rect.bottom
        if vertical:
            h = y2-y1
        else:
            h = x2-x1
        if forward:
            a, b = start_color, end_color
        else:
            b, a = start_color, end_color
        rate = (
            float(b[0]-a[0])/h,
            float(b[1]-a[1])/h,
            float(b[2]-a[2])/h
        )
        fn_line = pygame.draw.line
        if vertical:
            for line in range(y1, y2):
                color = (
                    min(max(a[0]+(rate[0]*(line-y1)), 0), 255),
                    min(max(a[1]+(rate[1]*(line-y1)), 0), 255),
                    min(max(a[2]+(rate[2]*(line-y1)), 0), 255)
                )
                fn_line(display, color, (x1, line), (x2, line))
        else:
            for col in range(x1, x2):
                color = (
                    min(max(a[0]+(rate[0]*(col-x1)), 0), 255),
                    min(max(a[1]+(rate[1]*(col-x1)), 0), 255),
                    min(max(a[2]+(rate[2]*(col-x1)), 0), 255)
                )
                fn_line(display, color, (col, y1), (col, y2))

    def first_hand(self, players):
        for i in range(2):
            for player in players:
                player.add_card(self.deck.deal())

        for player in players:
            _x = 0
            dealer_hidden = True
            for i in player.show_hand():
                if player.name == "Dealer" and dealer_hidden == True:
                    print("Hide card", i)
                    i.hide_card()
                    dealer_hidden = False
                print(player.name, "i", i.is_hidden())
                img_w, img_h = i.card_img.get_size()
                _card_x = (self.w/2.5) - (img_w*2) + _x
                _card_y = (self.h/2) + (img_h/2)
                player.draw_card(self.display, player.name, i, _card_x, _card_y)
                _x += 25
                pygame.display.update()

    def hit_btn(self):
        btn_txt = self.font_small.render("HIT", False, (255, 255, 255))
        btn_w = self.deck.deck_img.get_size()[0]
        btn = pygame.Rect(Config["deck"]["x"], Config["deck"]["y"]+150, btn_w, 25)
        btn_rect = btn_txt.get_rect(center=btn.center)
        self.display.fill((20, 35, 0), btn, 1)
        self.display.blit(btn_txt, btn_rect)
        pygame.display.flip()

    def stay_btn(self):
        btn_txt = self.font_small.render("STAY", False, (255, 255, 255))
        btn_w = self.deck.deck_img.get_size()[0]
        btn = pygame.Rect(Config["deck"]["x"], Config["deck"]["y"]+185, btn_w, 25)
        btn_rect = btn_txt.get_rect(center=btn.center)
        self.display.fill((20, 35, 0), btn, 1)
        self.display.blit(btn_txt, btn_rect)
        pygame.display.flip()


