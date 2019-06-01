import pygame, time
from config import Config
from objects import Deck, Player


def draw_text(surf, text, size, x, y, font_name):
    _font_name = pygame.font.match_font(font_name)
    font = pygame.font.Font(_font_name, size)
    text_surface = font.render(text, True, Game.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Game:

    # Font global def
    font_name = pygame.font.match_font('freesansbold')

    # Game global colors
    WHITE = (255, 255, 255)

    def __init__(self, display):
        self.clock = pygame.time.Clock()
        self.last = pygame.time.get_ticks()
        self.cd = 800
        self.hit_btn_rect = pygame.Rect(Config["deck"]["x"], Config["deck"]["y"]+150, 140, 25)
        self.pygame = pygame.init()
        pygame.font.init()
        self.font_small = pygame.font.SysFont('Arial Black', 12)
        self.font_large = pygame.font.SysFont('Arial', 32)
        self.display = display
        self.deck = Deck(self.display)
        self.player = Player("Player", self.deck)
        self.dealer = Player("Dealer", self.deck)
        self.w, self.h = self.display.get_size()
        self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.player_card_x_offset = 0
        self.player_card_y_offset = 0
        self.dealer_card_x_offset = 0
        self.dealer_card_y_offset = 33.75
        self.player_hand_txt = None
        self.players = []
        self.players.append(self.player)
        self.players.append(self.dealer)
        self.run = True
        self.game_over = False
        self.reason = ""

    def loop(self):
        _x = 0

        # Filling bg with green gradient
        self.gradient_bg(self.display, self.rect, (34, 139, 34), (0, 100, 0), True, True)

        # Putting deck image on the screen
        self.deck.draw()

        # Dealing first hard of cards
        self.first_hand(self.players)

        # Drawing the hit and stay button
        self.stand_btn()
        self.hit_btn()

        # Show Player Hand Total text
        self.display_player_hand()

        # Show Dealer Hand Total text
        self.display_dealer_hand()
        # self.display_dealer_cards()

        # Main loop
        while self.run:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    _deck_img_size = self.deck.deck_img.get_size()
                    _deck_img = pygame.Rect((Config["deck"]["x"], Config["deck"]["y"]), _deck_img_size)
                    _hit_btn_w = self.deck.deck_img.get_size()[0]
                    _hit_btn = pygame.Rect(Config["deck"]["x"], Config["deck"]["y"] + 150, _hit_btn_w, 25)
                    _stand_btn = pygame.Rect(Config["deck"]["x"], Config["deck"]["y"] + 185, _hit_btn_w, 25)
                    if _deck_img.collidepoint(x, y):
                        # It works... need to implement [Hit] and [Stay] buttons
                        pass
                    if _hit_btn.collidepoint(x, y):
                        print("_hit btn COLLIDE")
                        self.player.hit()
                        self.player_card_x_offset += 25
                        self.player.draw_card(self.display, self.player, self.player.show_hand()[-1],
                                              self.player_card_x_offset, self.player_card_y_offset)
                        # print("Player Hand: ", self.player.str_hand(), "Values: ", self.player.get_values())
                        self.update_player_value_txt()
                    if _stand_btn.collidepoint(x, y):
                        print("_stand btn COLLIDE")
                        self.restart_game(True)

                        # Check if we reveal the first card or not and add a timer to flip the card
                        self.last = pygame.time.get_ticks() + 200
                        while self.dealer.hand[0].is_hidden():
                            now = pygame.time.get_ticks()
                            if now - self.last >= self.cd:
                                self.dealer.hand[0].reveal_card()
                                self.display_dealer_cards()
                                self.dealer.draw_card(self.display, self.dealer, self.dealer.show_hand()[-1],
                                                      self.dealer_card_x_offset, self.dealer_card_y_offset)
                                self.update_dealer_value_txt(True)
                                self.last = pygame.time.get_ticks()
                                break

                        if self.dealer.get_values() >= 17 and self.dealer.get_values() > self.player.get_values():
                            self.reason = "Dealer win (" + str(self.dealer.get_values()) + ")."
                            self.game_over = True
                            self.show_game_over_screen(self.reason)
                            break
                        elif self.dealer.get_values() >= 17 and self.player.get_values() > self.dealer.get_values():
                            self.reason = "You win (" + str(self.player.get_values()) + ")."
                            self.game_over = True
                            self.show_game_over_screen(self.reason)
                            break

                        self.last = pygame.time.get_ticks() + 500
                        while True:
                            if self.dealer.get_values() >= 17:
                                break
                            while self.dealer.get_values() < 17:
                                now = pygame.time.get_ticks()
                                if now - self.last >= self.cd:
                                    self.dealer.hit()
                                    self.dealer_card_x_offset += 25

                                    self.display_dealer_cards()
                                    self.dealer.draw_card(self.display, self.dealer, self.dealer.show_hand()[-1],
                                                          self.dealer_card_x_offset, self.dealer_card_y_offset)
                                    self.update_dealer_value_txt(True)
                                    self.last = pygame.time.get_ticks() + 500

            if self.player.get_values() == 21:
                self.reason = "Blackjack!"
                self.game_over = True
                self.show_game_over_screen(self.reason)

            if self.player.get_values() > 21:
                self.reason = "Busted (" + str(self.player.get_values()) + "). Dealer win."
                self.game_over = True
                self.show_game_over_screen(self.reason)

            if self.dealer.get_values() > 21:
                self.reason = "Dealer busted (" + str(self.dealer.get_values()) + "). You win."
                self.game_over = True
                self.show_game_over_screen(self.reason)

            if self.dealer.get_values() >= 17 and self.dealer.get_values() > self.player.get_values():
                self.reason = "Dealer win (" + str(self.dealer.get_values()) + ")."
                self.game_over = True
                self.show_game_over_screen(self.reason)

            if self.dealer.get_values() == 21:
                self.reason = "Dealer got a Blackjack! You lose."
                self.game_over = True
                self.show_game_over_screen(self.reason)

            if self.dealer.get_values() >= 17 and self.player.get_values() > self.dealer.get_values():
                self.reason = "You win."
                self.game_over = True
                self.show_game_over_screen(self.reason)

            if self.dealer.get_values() >= 17 and self.player.get_values() == self.dealer.get_values():
                self.reason = "It is a Tie."
                self.game_over = True
                self.show_game_over_screen(self.reason)

            pygame.display.update()
            self.clock.tick(Config["game"]["fps"])

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

    def show_game_over_screen(self, reason):
        # Clear Player Hand
        self.player = Player("Player", self.deck)
        # Filling bg with green gradient
        # self.gradient_bg(self.display, self.rect, (34, 139, 34), (0, 100, 0), True, True)
        _w = Config["game"]["width"]
        _h = Config["game"]["height"]
        # Draw text msg
        draw_text(self.display, reason, 26, _w/2-60, _h/2-20, "freesansbold")
        draw_text(self.display, "Press ESC to exit or any other key to play again", 22, _w/2-60, _h/2+4, "freesansbold")
        pygame.display.flip()
        # Check player key input to quit or restart the game
        waiting = True
        while waiting:

            self.clock.tick(Config["game"]["fps"])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    else:
                        waiting = False
                        self.restart_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    self.restart_game()

    def restart_game(self, hide_btns=False):
        self.game_over = False
        # Create a new Deck and new Player/Dealer
        self.deck = Deck(self.display)
        self.player = Player("Player", self.deck)
        self.dealer = Player("Dealer", self.deck)
        self.players = []
        self.players.append(self.player)
        self.players.append(self.dealer)

        # Filling bg with green gradient
        self.gradient_bg(self.display, self.rect, (34, 139, 34), (0, 100, 0), True, True)

        # Putting deck image on the screen
        self.deck.draw()

        # Dealing first hard of cards
        self.first_hand(self.players)

        if not hide_btns:
            # Drawing the hit and stay button
            self.stand_btn()
            self.hit_btn()

        # Show Player Hand Total text
        self.display_player_hand()

        # Show Dealer Hand Total text
        self.display_dealer_hand()

        self.display_dealer_cards()

        pygame.display.flip()

    def game_loop(self):
        pass

    def first_hand(self, players):
        for i in range(2):
            for player in players:
                player.add_card(self.deck.deal())

        for player in players:
            _x = 0
            dealer_hidden = True
            for i in player.show_hand():
                if player.name == "Dealer" and dealer_hidden:
                    # print("Hide card", i)
                    i.hide_card()
                    dealer_hidden = False
                img_w, img_h = i.card_img.get_size()
                _card_x = (self.w/2.5) - (img_w*2) + _x
                _card_y = (self.h/2) + (img_h/2)
                player.draw_card(self.display, player.name, i, _card_x, _card_y)
                _x += 25
                self.player_card_x_offset = _card_x
                self.dealer_card_x_offset = _card_x
                self.player_card_y_offset = _card_y
                pygame.display.update()

    def hit_btn(self):
        btn_txt = self.font_small.render("HIT", False, (255, 255, 255))
        btn_w = self.deck.deck_img.get_size()[0]
        btn = pygame.Rect(Config["deck"]["x"], Config["deck"]["y"]+150, btn_w, 25)
        btn_rect = btn_txt.get_rect(center=btn.center)
        self.display.fill((20, 35, 0), btn, 1)
        self.display.blit(btn_txt, btn_rect)
        pygame.display.flip()
        return btn

    def stand_btn(self):
        btn_txt = self.font_small.render("STAND", False, (255, 255, 255))
        btn_w = self.deck.deck_img.get_size()[0]
        btn = pygame.Rect(Config["deck"]["x"], Config["deck"]["y"]+185, btn_w, 25)
        btn_rect = btn_txt.get_rect(center=btn.center)
        self.display.fill((20, 35, 0), btn, 1)
        self.display.blit(btn_txt, btn_rect)
        pygame.display.flip()

    def display_dealer_hand(self):
        txt_x = self.player_card_x_offset - ((len(self.player.hand) - 1) * 25)
        txt_y = self.player_card_y_offset - 120
        rect_w = (self.deck.deck_img.get_size()[0] + 75)
        txt_str = "Dealer Total: " + str(self.dealer.get_values())
        txt = self.font_small.render(txt_str, False, (255, 255, 255))
        rect = pygame.Rect(txt_x, txt_y, rect_w, 25)
        self.display.blit(txt, rect)

    def display_player_hand(self):
        txt_x = self.player_card_x_offset - ((len(self.player.hand) - 1) * 25)
        txt_y = self.player_card_y_offset - 35
        rect_w = (self.deck.deck_img.get_size()[0] + 75)
        txt_str = "Player Total: " + str(self.player.get_values())
        txt = self.font_small.render(txt_str, False, (255, 255, 255))
        rect = pygame.Rect(txt_x, txt_y, rect_w, 25)
        self.display.blit(txt, rect)

    def update_dealer_value_txt(self, hide_btns=False):
        txt_x = self.player_card_x_offset - ((len(self.player.hand) - 1) * 25)
        txt_y = self.player_card_y_offset - 120
        rect_w = (self.deck.deck_img.get_size()[0] + 75)
        txt_str = "Dealer Total: " + str(self.dealer.get_values())
        txt = self.font_small.render(txt_str, False, (255, 255, 255))
        rect = pygame.Rect(txt_x, txt_y, rect_w, 25)
        # Re-Cover the screen with the background gradient
        self.gradient_bg(self.display, self.rect, (34, 139, 34), (0, 100, 0), True, True)

        self.display.blit(txt, rect)

        # Update player score
        self.display_player_hand()

        # Redraw Player, Dealer, Deck and buttons
        self.display_player_cards()
        self.display_dealer_cards()
        self.deck.draw()

        if not hide_btns:
            self.hit_btn()
            self.stand_btn()

        pygame.display.flip()

    def update_player_value_txt(self, hide_btns=False):
        txt_x = self.player_card_x_offset - ((len(self.player.hand) - 1) * 25)
        txt_y = self.player_card_y_offset - 35
        rect_w = (self.deck.deck_img.get_size()[0] + 75)
        txt_str = "Player Total: " + str(self.player.get_values())
        txt = self.font_small.render(txt_str, False, (255, 255, 255))
        rect = pygame.Rect(txt_x, txt_y, rect_w, 25)
        # Re-Cover the screen with the background gradient
        self.gradient_bg(self.display, self.rect, (34, 139, 34), (0, 100, 0), True, True)

        self.display.blit(txt, rect)

        # Update dealer score
        self.display_dealer_hand()

        # Redraw Player, Dealer, Deck and buttons
        self.display_player_cards()
        self.display_dealer_cards()
        self.deck.draw()

        if not hide_btns:
            self.hit_btn()
            self.stand_btn()

        pygame.display.flip()

    def display_dealer_cards(self):
        _x = 0
        for card in self.dealer.hand:
            img_w, img_h = card.card_img.get_size()
            _card_x = (self.w / 2.5) - (img_w * 2) + _x
            _card_y = (self.h / 2) + (img_h / 2)
            self.dealer.draw_card(self.display, self.dealer.name, card, _card_x, _card_y)
            _x += 25

    def display_player_cards(self):
        _x = 0
        for card in self.player.hand:
            img_w, img_h = card.card_img.get_size()
            _card_x = (self.w / 2.5) - (img_w * 2) + _x
            _card_y = (self.h / 2) + (img_h / 2)
            self.player.draw_card(self.display, self.player.name, card, _card_x, _card_y)
            _x += 25
