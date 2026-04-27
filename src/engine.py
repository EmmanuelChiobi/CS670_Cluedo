import random
from .models import Card, Player
from .logic_ai import CluedoAI

class CluedoEngine:
    def __init__(self, player_names):
        # 1. Initialize Cards
        self.suspects = [Card(n, 'Suspect') for n in ["Col. Mustard", "Miss Scarlett", "Prof. Plum"]]
        self.weapons = [Card(n, 'Weapon') for n in ["Dagger", "Revolver", "Rope"]]
        self.rooms = [Card(n, 'Room') for n in ["Kitchen", "Ballroom", "Library"]]
        
        self.all_cards = self.suspects + self.weapons + self.rooms
        self.players = [Player(name, is_ai=True) for name in player_names]
        self.case_file = []
        
        # 2. Setup Game
        self.setup_game()
        
        # 3. Initialize AI Brains
        for p in self.players:
            if p.is_ai:
                p.logic = CluedoAI(p.name, self.all_cards)
                # AI knows its own cards immediately
                for card in p.hand:
                    p.logic.mark_seen(card.name, status='Owned')

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

    def play_turn(self, player):
        print(f"\n--- {player.name}'s Turn ---")
        
        # STEP 1: Deduction Check
        # The AI checks if it has enough info to win
        accusation = player.logic.make_deduction()
        if accusation:
            print(f"!!! {player.name} is making an ACCUSATION: {accusation}")
            return self.check_accusation(accusation)

        # STEP 2: Movement (BFS)
        # AI finds the shortest path to a room it hasn't investigated
        current_room = getattr(player, 'location', 'Hall') 
        path = player.logic.find_nearest_unseen_room(current_room)
        
        if path:
            new_room = path[-1]
            player.location = new_room
            print(f"{player.name} moved to the {new_room} via path: {path}")
            
            # STEP 3: Suggestion
            # AI suggests the current room and two other unknown items
            suspect = random.choice([c.name for c in self.all_cards if c.card_type == 'Suspect'])
            weapon = random.choice([c.name for c in self.all_cards if c.card_type == 'Weapon'])
            
            print(f"{player.name} suggests: {suspect} in the {new_room} with the {weapon}")
            self.process_suggestion(player, suspect, weapon, new_room)

    def process_suggestion(self, suggester, suspect, weapon, room):
        suggestion_names = [suspect, weapon, room]
        idx = self.players.index(suggester)
        
        for i in range(1, len(self.players)):
            responder = self.players[(idx + i) % len(self.players)]
            revealed = responder.show_card(suggestion_names)
            
            if revealed:
                print(f"{responder.name} showed a card to {suggester.name}.")
                # UPDATE LOGIC: The suggester learns a new piece of info
                if suggester.is_ai:
                    suggester.logic.mark_seen(revealed.name, status='Seen')
                return
        
        print("No one could disprove the suggestion.")

    def check_accusation(self, accusation):
        solution_names = [c.name for c in self.case_file]
        if set(accusation) == set(solution_names):
            print("CORRECT! The mystery is solved.")
            return True
        else:
            print("WRONG! That player is eliminated.")
            return False