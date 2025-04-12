from base_bot import BaseBot
from rules import Rules

class Player(BaseBot):

    # This is intentionally left simple for competition participants to implement their strategy.
        # They have access to self.hand and the top_card.
        # Example:
        #   top_card = "R5"
        #   self.hand = ["B2", "RS", "WC", "Y4", ...]

        # Participants should return a valid card from self.hand or None if no playable card.

    def choose_card(self, top_card):
        def parse_card(card):
            if card[0] in {'W', 'P'}:
                return card[1], card[0]
            return card[0], card[1:]

        top_color, top_value = parse_card(top_card)

        # Count color frequency to choose optimal color for Wild/Draw4
        color_count = {'R': 0, 'G': 0, 'B': 0, 'Y': 0}
        for card in self.hand:
            color, _ = parse_card(card)
            if color in color_count:
                color_count[color] += 1

        most_common_color = max(color_count, key=color_count.get)

        # 1. Try to play a number or action card that matches color or value
        for card in self.hand:
            color, value = parse_card(card)
            if color == top_color or value == top_value:
                if card[0] not in {'W', 'P'}:  # Prefer non-wilds
                    return card

        # 2. Use Wild or +4 if no match
        for card in self.hand:
            if card.startswith('W'):
                return 'W' + most_common_color
            if card.startswith('P'):
                return 'P' + most_common_color

        # 3. No playable card, must draw
        return None



# For local testing only
if __name__ == "__main__":
    bot = Player(player_id=0)

    # Example input
    bot.hand = input("Enter your hand as space-separated cards: ").strip().split()
    top_card = input("Enter the top card: ").strip()

    move = bot.choose_card(top_card)
    print(f"Chosen card: {move}")
