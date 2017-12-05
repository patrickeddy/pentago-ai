# Patrick Eddy
# Bad-ass Pentago Playing AI
# TCSS 435, University of Washington

import board
import ai

from random import randint

# Setup the game
game_ended = False
player_color = ""

# Get which color the player wants to be
player_color = str(raw_input("Welcome to Pentago\n\nPlease choose a color (b, w) : "))
if player_color != "b" and player_color != "w":
    print("Error: Please choose w or b for your color.")
    exit()
move_order = randint(1,2)

# Create the gameboard
gb = board.GameBoard()
if move_order == 1:
    # Player turn
    gb.turn = player_color
else:
    # AI turn
    gb.turn = "b" if player_color != "b" else "w"

# Create the AI
ai_color = "b" if player_color == "w" else "w"
ai = ai.AI(ai_color)

print("=> You are " + str(player_color) + "\n=> AI is " + str(ai_color))

# GAME INTERFACE METHODS
def ai_move():
    """Method that moves the AI based on Minimax."""
    print("\nAI moving...\n")
    ai.move(gb)
    gb.complete_turn()

def prompt_player_move():
    """Prompts and initiates action by player."""
    move = str(raw_input("\nYour turn to move.\n\n: ")).upper()
    if (move != "Q"):
        success = gb.play_move(player_color, move)
        if not success:
            print("Invalid position. Please choose another position. ")
            prompt_player_move()

    gb.complete_turn()


# GAME LOOP
print("- - - - - - - - - - - - - - - - - - - ")
while True:
    if gb.turn == player_color: # player first
        gb.print_full_board()
        prompt_player_move()
    else: # let ai go first
        gb.print_full_board()
        ai_move()
    print("- - - - - - - - - - - - - - - - - - - ")
