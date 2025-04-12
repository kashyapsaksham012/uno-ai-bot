from abc import ABC, abstractmethod


class BaseBot(ABC):
    def __init__(self, player_id):
        self.player_id = player_id
        self.hand = []

    @abstractmethod
    def choose_card(self, top_card):
        """Return a card to play or None to draw."""
        pass

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def remove_card(self, card):
        if card in self.hand:
            self.hand.remove(card)

    def __str__(self):
        return f"Player {self.player_id}: {self.hand}"
