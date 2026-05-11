from collections import deque

class CluedoAI:
    def __init__(self, player_name, all_cards):
        self.name = player_name
        
        # STATE REPRESENTATION: The 'Notebook' is the agent's Knowledge Base.
        # It maps every card to a state: 'Owned' (in hand), 'Seen' (ruled out), or 'Unknown'.
        self.notebook = {card.name: 'Unknown' for card in all_cards}
        
        # GRAPH DATA: The mansion represented as an adjacency list for pathfinding.
        self.map_data = {
            'Hall': ['Study', 'Library', 'Lounge'],
            'Library': ['Hall', 'Billiard Room', 'Conservatory'],
            'Kitchen': ['Ballroom', 'Dining Room'],
            # ... additional room connectivity ...
        }

    def mark_seen(self, card_name, status='Seen'):
        """
        KNOWLEDGE UPDATE: When a card is revealed, update the internal notebook.
        This effectively reduces the search space for the final solution.
        """
        self.notebook[card_name] = status

    def find_nearest_unseen_room(self, current_room):
        """
        PATHFINDING (BFS): Finds the shortest path to a room still marked as 'Unknown'.
        Ensures the AI is always moving toward new information.
        """
        queue = deque([(current_room, [current_room])])
        visited = {current_room}
        
        fallback_room = None

        while queue:
            node, path = queue.popleft()

            # GOAL TEST: Return the path if this node is an 'Unknown' room
            if self.notebook.get(node) == 'Unknown':
                return path
            
            # HEURISTIC FALLBACK: If all rooms are known, we still need to move.
            # Store the first adjacent room found to avoid an empty return.
            if not fallback_room and node != current_room:
                fallback_room = path

            # EXPLORATION: Standard BFS neighbor traversal
            for neighbor in self.map_data.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return fallback_room

    def make_deduction(self):
        """
        PROPOSITIONAL LOGIC: Implements the process of elimination.
        If the agent has ruled out all but 3 cards (1 Suspect, 1 Weapon, 1 Room),
        it makes a formal accusation.
        """
        unknowns = [name for name, status in self.notebook.items() if status == 'Unknown']
        
        # ACCUSATION TRIGGER: In this simplified engine, 3 unknowns = The Case File.
        return unknowns if len(unknowns) == 3 else None