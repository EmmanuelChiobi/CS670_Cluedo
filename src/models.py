import random

class Card:
    def __init__(self, name, card_type):
        self.name = name
        self.card_type = card_type # 'Suspect', 'Weapon', or 'Room'

    def __repr__(self):
        return f"{self.name} ({self.card_type})"

class Player:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.is_ai = is_ai
        self.hand = []
        self.notebook = [] # Tracks seen cards

    def show_card(self, suggestion):
        # Return a card if it matches the suggestion
        matching = [c for c in self.hand if c.name in suggestion]
        return random.choice(matching) if matching else None