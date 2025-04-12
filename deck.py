import random


def _initialize_deck():
    colors = ['R', 'G', 'B', 'Y']
    numbers = list(range(10))
    actions = ['S', 'R', 'P']

    deck = []
    for color in colors:
        deck.append(f"{color}0")  # One 0 per color
        for num in range(1, 10):
            deck.extend([f"{color}{num}"] * 2)
        for action in actions:
            deck.extend([f"{color}{action}"] * 2)

    wild_cards = ['WC']*4
    plus_four_cards = ['PC']*4
    deck.extend(wild_cards+plus_four_cards)

    return deck


class Deck:
    def __init__(self):
        self.cards = _initialize_deck()
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None

    def reset_deck(self, played_cards):
        """Shuffle played cards back into the deck, keeping the last card in play."""
        last_card = played_cards.pop()

        def normalize(card):
            if card.startswith("W") and len(card) == 2:
                return "WC"
            if card.startswith("P") and len(card) == 2:
                return "PC"
            return card

        normalized = [normalize(card) for card in played_cards]
        self.cards = normalized.copy()
        random.shuffle(self.cards)
        self.cards.insert(0, last_card)


# Example Usage
if __name__ == "__main__":
    deck = Deck()
    print("Initial Deck:", deck.cards[:10])
    print("Drawn Card:", deck.draw_card())
