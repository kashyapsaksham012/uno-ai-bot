import random


class Rules:
    VALID_COLORS = {'R', 'G', 'B', 'Y', 'W', 'P'}
    ACTION_CARDS = {'S': 'Skip', 'R': 'Reverse', 'P': 'Draw4', 'W': 'Wild'}

    @staticmethod
    def is_valid_move(card, top_card):
        if not card or not top_card:
            return False
        if card in {"WC", "PC"}:
            return False  # Uncolored wilds not allowed directly

        def parse(c):
            if c[0] in ('W', 'P'):  # Wild or +4
                return c[1:], 10
            return c[0], c[1:]

        card_color, card_val = parse(card)
        top_color, top_val = parse(top_card)

        return (
                card_color == top_color or
                card_val == top_val or
                card[0] in {'W', 'P'}  # wilds & +4s
        )

    @staticmethod
    def apply_card_effect(card, game_state, agent):
        """
        Apply the effect of action or wild cards to the game state.
        Supports Skip (S), Reverse (R), Draw 2 (P), Wild (W), and Wild Draw 4 (PR, PB, etc.)
        """
        if not card or not game_state:
            return

        color = card[0]
        value = card[1:]

        # 🃏 Wild Color (e.g., 'WR', 'WB', etc.)
        if color == "W":
            print("🎨 Wild played.")
            return

        # 🃏 Wild Draw Four (e.g., 'PR', 'PG', etc.)
        if color == "P":
            game_state.next_player_draw(4)
            game_state.skip_turn()
            print("🎯 Wild Draw 4 played — next player draws 4 cards and is skipped.")
            return

        # 🎨 Colored action cards (e.g., 'RS', 'RP', 'RR')
        if value == "S":
            game_state.skip_turn()
            print("⏭️ Skip played — next player is skipped.")
        elif value == "R":
            game_state.reverse_turn_order()
            print("🔁 Reverse played — turn direction reversed.")
        elif value == "P":
            game_state.next_player_draw(2)
            game_state.skip_turn()
            print("🎯 Draw 2 played — next player draws 2 cards and is skipped.")

    @staticmethod
    def is_special_card(card):
        if not card:
            return False
        return any(symbol in card for symbol in Rules.ACTION_CARDS.keys())

    @staticmethod
    def get_card_color(card):
        if not card:
            return None
        if card.startswith("W"):
            return "W"
        if card.endswith("P"):
            return "2"
        return card[0] if card[0] in Rules.VALID_COLORS else None

    @staticmethod
    def is_next_uno(game_state, current_player, next_player):
        return len(game_state.get_player_hand(next_player)) == 1

    @staticmethod
    def is_any_uno(game_state, players):
        return any(len(game_state.get_player_hand(player)) == 1 for player in players)

    @staticmethod
    def deck_draw(deck, discard_pile, player_hand):
        if not deck and discard_pile:
            top_card = discard_pile[-1]
            deck.extend(discard_pile[:-1])
            random.shuffle(deck)
            discard_pile.clear()
            discard_pile.append(top_card)

        if deck:
            card = deck.pop()
            player_hand.append(card)
            return card
        return None

    @staticmethod
    def pass_turn(game_state):
        game_state.skip_turn()

    @staticmethod
    def challenge_plus_four(challenger, challenged, game_state):
        last_card = game_state.get_last_played_card()
        if not last_card or not last_card.startswith("P"):
            return False

        challenged_hand = game_state.get_player_hand(challenged)
        top_card_before = game_state.get_top_card_before_last()
        has_playable = any(
            Rules.is_valid_move(card, top_card_before) and
            Rules.get_card_color(card) == Rules.get_card_color(top_card_before)
            for card in challenged_hand
        )

        if has_playable:
            game_state.next_player_draw(4, challenged)
            return True
        else:
            game_state.next_player_draw(6, challenger)
            return False

    @staticmethod
    def can_stack(card1, card2):
        return (
                (card1.startswith("P") and card2.startswith("P")) or
                (card1.endswith("P") and card2.endswith("P"))
        )

    @staticmethod
    def enforce_auto_penalty(card, game_state, player_hand):
        top_card = game_state.get_top_card()
        if not Rules.is_valid_move(card, top_card):
            game_state.next_player_draw(2)
            print("Invalid move! Drawing 2 cards as penalty.")
