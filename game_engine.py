import random
from deck import Deck
from rules import Rules


class Game:
    def __init__(self):
        self.deck = Deck()
        self.players = {}
        self.direction = 1
        self.turn_order = []
        self.current_player_idx = 0
        self.current_player = 0
        self.played_cards = []

    def next_turn(self):
        self.current_player_idx = (self.current_player_idx + self.direction) % len(self.turn_order)
        self.current_player = self.turn_order[self.current_player_idx]

    def skip_turn(self):
        self.next_turn()

    def reverse_turn_order(self):
        self.direction *= -1

    def next_player_draw(self, num_cards):
        next_index = (self.current_player_idx + self.direction) % len(self.turn_order)
        next_player = self.turn_order[next_index]

        for _ in range(num_cards):
            if not self.deck.cards:
                self.reshuffle_deck()

            card = self.deck.draw_card()
            if card:
                self.players[next_player].receive_cards([card])
            else:
                print(f"⚠️ Could not draw a card for Player {next_player} — deck still empty after reshuffle.")

    def check_winner(self):
        for pid, bot in self.players.items():
            if not bot.hand:
                print(f"🏆 Player {pid} wins!")
                return pid
        return None

    def reshuffle_deck(self):
        if len(self.played_cards) > 1:
            print("♻️ Deck empty — reshuffling played cards...")
            self.deck.reset_deck(self.played_cards)
        else:
            print("⚠️ Not enough cards to reshuffle.")

    def play_turn(self, player_id, player_move=None):
        if player_id != self.current_player:
            print("Not your turn!")
            return None

        bot = self.players[player_id]
        top_card = self.played_cards[-1]

        if player_move:
            if Rules.is_valid_move(player_move, top_card):
                if player_move[0] in {'W', 'P'}:
                    bot.remove_card(player_move[0]+'C')
                else:
                    bot.remove_card(player_move)
                self.played_cards.append(player_move)
                if len(bot.hand) == 1:
                    print(f"⚠ Player {player_id} has UNO!")
                Rules.apply_card_effect(player_move, self, player_id)

                winner = self.check_winner()
                if winner is not None:
                    return winner  # 🔁 Exit early if win

                self.next_turn()
            else:
                print("Invalid move. Turn forfeited.")
                self.next_turn()

        else:
            if not self.deck.cards:
                self.reshuffle_deck()
            drawn_card = self.deck.draw_card()
            if drawn_card:
                bot.receive_cards([drawn_card])
                print(f"Player {player_id} draws {drawn_card}")

                if Rules.is_valid_move(drawn_card, top_card):
                    print(f"Player {player_id} plays drawn card: {drawn_card}")
                    bot.remove_card(drawn_card)
                    self.played_cards.append(drawn_card)
                    if len(bot.hand) == 1:
                        print(f"⚠ Player {player_id} has UNO!")
                    Rules.apply_card_effect(drawn_card, self, player_id)

                    winner = self.check_winner()
                    if winner is not None:
                        return winner

            self.next_turn()

        return None  # Default
