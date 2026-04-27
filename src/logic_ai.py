from collections import deque

class CluedoAI:
    def __init__(self, player_name, all_cards):
        self.name = player_name
        # The 'Notebook' tracks what we know: {card_name: 'Owned' | 'Seen' | 'Unknown'}
        self.notebook = {card.name: 'Unknown' for card in all_cards}
        self.map_data = {
            'Hall': ['Study', 'Library', 'Lounge'],
            'Library': ['Hall', 'Billiard Room', 'Conservatory'],
            'Kitchen': ['Ballroom', 'Dining Room'],
            # ... other room connections ...
        }

    def mark_seen(self, card_name, status='Seen'):
        """Update the notebook when a card is revealed."""
        self.notebook[card_name] = status

    def find_nearest_unseen_room(self, current_room):
        queue = deque([(current_room, [current_room])])
        visited = {current_room}
        
        all_rooms = list(self.map_data.keys())
        fallback_room = None

        while queue:
            node, path = queue.popleft()

            # Goal: A room I haven't ruled out yet
            if self.notebook.get(node) == 'Unknown':
                return path
            
            # Save the first room we find as a fallback if everything is 'Seen'
            if not fallback_room and node != current_room:
                fallback_room = path

            for neighbor in self.map_data.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        # If no 'Unknown' rooms exist, just move to a random adjacent room
        return fallback_room

    def make_deduction(self):
        """
        Propositional Logic: If only one card in a category is 'Unknown',
        that must be the card in the Case File.
        """
        unknowns = [name for name, status in self.notebook.items() if status == 'Unknown']
        # If the AI has narrowed it down to 3 cards (1 of each type), it can accuse.
        return unknowns if len(unknowns) == 3 else None