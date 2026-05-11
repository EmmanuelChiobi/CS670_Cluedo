from src.engine import CluedoEngine

def main():
    """
    Orchestrates the Cluedo AI simulation. 
    Handles game setup, the round-based loop, and victory conditions.
    """
    print("========================================")
    print("   WELCOME TO THE CLUEDO AI SIMULATOR   ")
    print("========================================\n")
    
    # SYSTEM INIT: Instantiate the game engine with three AI participants
    player_names = ["AI_Watson", "AI_Holmes", "AI_Adler"]
    game = CluedoEngine(player_names)
    
    print(f"The mystery has been set. {len(game.players)} players are ready.")
    print("Distribution of cards complete. Let the investigation begin!\n")

    game_active = True
    round_count = 1

    # GAME LOOP: Continues until a player wins or the round limit is reached
    while game_active:
        print(f"--- ROUND {round_count} ---")
        
        for player in game.players:
            # ENGINE CALLBACK: Each player executes their logic (Move -> Suggest -> Accuse)
            result = game.play_turn(player)
            
            # GOAL TEST: If play_turn returns True, the player's propositional logic was correct
            if result is True:
                print(f"\nGAME OVER: {player.name} has won the game!")
                game_active = False
                break
        
        round_count += 1
        
        # SAFETY CONSTRAINTS: Prevent infinite loops in edge cases
        if round_count > 50:
            print("The mystery remains unsolved after 50 rounds.")
            break

if __name__ == "__main__":
    main()