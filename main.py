from src.engine import CluedoEngine

def main():
    print("========================================")
    print("   WELCOME TO THE CLUEDO AI SIMULATOR   ")
    print("========================================\n")
    
    # Initialize the engine with AI players
    player_names = ["AI_Watson", "AI_Holmes", "AI_Adler"]
    game = CluedoEngine(player_names)
    
    print(f"The mystery has been set. {len(game.players)} players are ready.")
    print("Distribution of cards complete. Let the investigation begin!\n")

    game_active = True
    round_count = 1

    while game_active:
        print(f"--- ROUND {round_count} ---")
        
        for player in game.players:
            # The engine handles the AI turn logic
            result = game.play_turn(player)
            
            # If play_turn returns True, an accusation was successful
            if result is True:
                print(f"\nGAME OVER: {player.name} has won the game!")
                game_active = False
                break
        
        round_count += 1
        # Safety break for demo purposes
        if round_count > 50:
            print("The mystery remains unsolved after 50 rounds.")
            break

if __name__ == "__main__":
    main()