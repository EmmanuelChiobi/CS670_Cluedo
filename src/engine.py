import random
from .models import Card, Player
from .logic_ai import CluedoAI

class CluedoEngine:
    def __init__(self, player_names):
        # 1. DOMAIN INITIALIZATION: Define the suspects, weapons, and rooms.
        self.suspects = [Card(n, 'Suspect') for n in ["Col. Mustard", "Miss Scarlett", "Prof. Plum"]]
        self.weapons = [Card(n, 'Weapon') for n in ["Dagger", "Revolver", "Rope"]]
        self.rooms = [Card(n, 'Room') for n in ["Kitchen", "Ballroom", "Library"]]
        
        self.all_cards = self.suspects + self.weapons + self.rooms
        self.players = [Player(name, is_ai=True) for name in player_names]
        self.case_file = []
        
        # 2. GAME SETUP: Conceal the solution and distribute the rest of the cards.
        self.setup_game()
        
        # 3. AI BOOTSTRAP: Initialize the 'Brain' for each player and give them their starting cards.
        for p in self.players:
            if p.is_ai:
                p.logic = CluedoAI(p.name, self.all_cards)
                # INTERNAL KNOWLEDGE: The AI marks its own hand as 'Owned' immediately.
                for card in p.hand:
                    p.logic.mark_seen(card.name, status='Owned')

    def setup_game(self):
        """Creates the 'Case File' (The secret solution)."""
        self.case_file = [
            self.suspects.pop(random.randrange(len(self.suspects))),
            self.weapons.pop(random.randrange(len(self.weapons))),
            self.rooms.pop(random.randrange(len(self.rooms)))
        ]
        
        # SHUFFLE & DEAL: Distribute remaining evidence among players.
        all_remaining = self.suspects + self.weapons + self.rooms
        random.shuffle(all_remaining)
        
        while all_remaining:
            for p in self.players:
                if all_remaining:
                    p.hand.append(all_remaining.pop())

    def play_turn(self, player):
        """The atomic turn structure: 1. Accuse? -> 2. Move -> 3. Suggest."""
        print(f"\n--- {player.name}'s Turn ---")
        
        # STAGE 1: DEDUCTION CHECK
        # Before moving, the AI checks if the mystery is already solved.
        accusation = player.logic.make_deduction()
        if accusation:
            print(f"!!! {player.name} ACCUSES: {accusation}")
            return self.check_accusation(accusation)

        # STAGE 2: NAVIGATION (BFS)
        current_loc = getattr(player, 'location', 'Hall')
        path = player.logic.find_nearest_unseen_room(current_loc)
        
        if path:
            player.location = path[-1]
            print(f"{player.name} moved to the {player.location}")
            
            # STAGE 3: INTELLIGENT SUGGESTION
            # The AI only suggests cards that are still 'Unknown' to maximize new info.
            unknown_suspects = [c.name for c in self.all_cards 
                                if c.card_type == 'Suspect' and player.logic.notebook[c.name] == 'Unknown']
            unknown_weapons = [c.name for c in self.all_cards 
                                if c.card_type == 'Weapon' and player.logic.notebook[c.name] == 'Unknown']
            
            s_guess = random.choice(unknown_suspects) if unknown_suspects else "Miss Scarlett"
            w_guess = random.choice(unknown_weapons) if unknown_weapons else "Dagger"
            
            print(f"{player.name} suggests: {s_guess} in {player.location} with {w_guess}")
            self.process_suggestion(player, s_guess, w_guess, player.location)

    def process_suggestion(self, suggester, suspect, weapon, room):
        """Simulates the table talk where players disprove suggestions."""
        suggestion_names = [suspect, weapon, room]
        idx = self.players.index(suggester)
        
        # CIRCULAR PASSING: Check each opponent in order for a matching card.
        for i in range(1, len(self.players)):
            responder = self.players[(idx + i) % len(self.players)]
            revealed = responder.show_card(suggestion_names)
            
            if revealed:
                print(f"{responder.name} showed a card to {suggester.name}.")
                # INFORMATION FEEDBACK: The suggester updates their knowledge base.
                if suggester.is_ai:
                    suggester.logic.mark_seen(revealed.name, status='Seen')
                return
        
        print("No one could disprove the suggestion.")

    def check_accusation(self, accusation):
        """Verifies if the player's deduction matches the hidden Case File."""
        solution_names = [c.name for c in self.case_file]
        if set(accusation) == set(solution_names):
            print("CORRECT! The mystery is solved.")
            return True
        else:
            print("WRONG! That player is eliminated.")
            return False