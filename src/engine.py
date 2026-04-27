import random
from .models import Card, Player

class CluedoEngine:
    def __init__(self, player_names):
        self.suspects = [Card(n, 'Suspect') for n in ["Col. Mustard", "Miss Scarlett", "Prof. Plum"]]
        self.weapons = [Card(n, 'Weapon') for n in ["Dagger", "Revolver", "Rope"]]
        self.rooms = [Card(n, 'Room') for n in ["Kitchen", "Ballroom", "Library"]]
        
        self.players = [Player(name) for name in player_names]
        self.case_file = []
        self.setup_game()

    def setup_game(self):
        # Pick the secret solution
        self.case_file = [
            self.suspects.pop(random.randrange(len(self.suspects))),
            self.weapons.pop(random.randrange(len(self.weapons))),
            self.rooms.pop(random.randrange(len(self.rooms)))
        ]
        
        # Distribute remaining cards
        all_remaining = self.suspects + self.weapons + self.rooms
        random.shuffle(all_remaining)
        
        while all_remaining:
            for p in self.players:
                if all_remaining:
                    p.hand.append(all_remaining.pop())

    def process_suggestion(self, suggester, suspect, weapon, room):
        suggestion_names = [suspect, weapon, room]
        # Ask other players in order
        idx = self.players.index(suggester)
        for i in range(1, len(self.players)):
            responder = self.players[(idx + i) % len(self.players)]
            revealed = responder.show_card(suggestion_names)
            if revealed:
                return responder, revealed
        return None, None