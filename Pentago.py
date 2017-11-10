"""
Patrick Eddy
TCSS 435

PA 2 - Pentago
"""

"""
HOW TO RUN:
Play Pentago by running in terminal:
`python Pentago.py`
"""

import board
import ai

# Setup the game
game_ended = False
player_color = ""

# Get which color the player wants to be
player_color = str(raw_input("Welcome to Pentago\nPlease choose a color (b, w) : "))
if player_color != "b" and player_color != "w":
    print("Error: Please choose w or b for your color.")
    exit()
move_order = int(raw_input("Would you like to move first (1) or second (2)? : "))
if move_order != 1 and move_order != 2:
    print("Error: Please choose first or second move.")
    exit()

print("\nHere we go...\n")

# Create the gameboard
gb = board.GameBoard()
if move_order == 1:
    gb.turn = player_color
else:
    gb.turn = "b" if player_color != "b" else "w"

# Create the AI
ai_color = "b" if player_color == "w" else "w"
ai = ai.AI(ai_color)

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
        ai_move()
    print("- - - - - - - - - - - - - - - - - - - ")
