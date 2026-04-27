from src.engine import CluedoEngine

def main():
    print("Welcome to Cluedo!")
    game = CluedoEngine(["Alice", "Bob", "Charlie"])
    
    # Simple demo loop
    current_turn = 0
    game_over = False
    
    while not game_over:
        player = game.players[current_turn]
        print(f"\nIt's {player.name}'s turn.")
        
        # In a real app, you'd take user input here
        # For demo: Alice suggests Scarlett in the Kitchen with the Dagger
        sug, card = game.process_suggestion(player, "Miss Scarlett", "Dagger", "Kitchen")
        
        if card:
            print(f"{sug.name} showed you the {card.name} card.")
        else:
            print("No one could disprove your suggestion.")
        
        # Increment turn
        current_turn = (current_turn + 1) % len(game.players)
        if current_turn == 0: game_over = True # End demo after 1 round

if __name__ == "__main__":
    main()