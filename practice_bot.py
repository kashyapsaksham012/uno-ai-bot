from base_bot import BaseBot


class PracticeBot(BaseBot):
    def choose_card(self, top_card):
        def parse_card(temp_card):
            """Returns (color, value) from card."""
            if temp_card[0] in {'W', 'P'} and len(temp_card) == 2:
                return temp_card[1], temp_card[0]  # e.g., WR => (R, W)
            return temp_card[0], temp_card[1:]  # e.g., R4 => (R, 4)

        top_color, top_value = parse_card(top_card)

        # Count color frequencies in hand
        color_count = {'R': 0, 'G': 0, 'B': 0, 'Y': 0}
        for card in self.hand:
            c, _ = parse_card(card)
            if c in color_count:
                color_count[c] += 1

        # Decide best color
        best = max(color_count.items(), key=lambda x: x[1])[0]

        for card in self.hand:
            card_color, card_value = parse_card(card)

            # Standard match
            if card_color == top_color or card_value == top_value:
                return card

        for card in self.hand:
            if card.startswith('W'):
                return 'W' + best
            if card.startswith('P'):
                return 'P' + best

        return None  # No playable card
