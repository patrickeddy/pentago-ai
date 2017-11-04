"""
Patrick Eddy
TCSS 435

PA 2 - Pentago
"""

def get_empty_board():
    return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# get empty boards for the sub-boards
board1 = get_empty_board()
board2 = get_empty_board()
board3 = get_empty_board()
board4 = get_empty_board()

def print_full_board():
    for i in range(6):
        print("") # add a new line for the board here
        if (i == 3):
            print "- - - - - - - "
        for j in range(6):
            if j == 3:
                print "|",
            if (j < 3):
                if (i < 3):
                    # first board
                    print str(board1[i][j]),
                else:
                    # second board
                    print str(board2[i%3][j]),
            else:
                if (i < 3):
                    # second board
                    print str(board3[i][j%3]),
                else:
                    # third board
                    print str(board4[i%3][j%3]),
    print("")

def play_move(player, play):
    parts = play.split(" ")

    pos = parts[0]
    rot = parts[1]

    print("Player is " + str(player))
    print("Pos is: " + str(pos))
    print("Rot is: " + str(rot))

    return

print_full_board()
play_move("b", "4/2 4L")
