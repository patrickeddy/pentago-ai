# Board module

class GameBoard():
    def __init__(self):
        self.board1 = self.get_empty_board()
        self.board2 = self.get_empty_board()
        self.board3 = self.get_empty_board()
        self.board4 = self.get_empty_board()
        self.turn = "b"

    def complete_turn(self):
        self.turn = "w" if self.turn == "b" else "b"

    def get_empty_board(self):
        return [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]

    def print_full_board(self):
        for i in range(6):
            print("") # add a new line for the board here
            if (i == 3):
                print "+------+------+"
            for j in range(6):
                if j==0 or j == 3:
                    print "|",
                if (j < 3):
                    if (i < 3):
                        # first board
                        print " " + str(self.board1[i][j]),
                    else:
                        # third board
                        print " " + str(self.board3[i%3][j]),
                else:
                    if (i < 3):
                        # second board
                        print " " + str(self.board2[i][j%3]),
                    else:
                        # fourth board
                        print " " + str(self.board4[i%3][j%3]),
                if j==5:
                    print "|",
        print("")

    def play_move(self, color, move):
        """Completes a move for a player."""
        parts = move.split(" ")

        pos = parts[0]
        rot = parts[1]

        pp_success = self.__place_piece(color, pos)
        rb_success = self.__rotate_board(rot)

        print("Placing piece status: " + str(pp_success))
        print("Rotating board status: " + str(rb_success))

        return pp_success and rb_success

    def __place_piece(self, color, pos):
        parts = pos.split("/")

        subboard = parts[0]
        subpos = int(parts[1])

        # print("subboard is " + str(subboard))
        # print("subpos is " + str(subpos))

        succeeded = False

        if subboard == "1":
            succeeded = self.__place_piece_on_subboard(self.board1, subpos)
        elif subboard == "2":
            succeeded =  self.__place_piece_on_subboard(self.board2, subpos)
        elif subboard == "3":
            succeeded = self.__place_piece_on_subboard(self.board3, subpos)
        elif subboard == "4":
            succeeded = self.__place_piece_on_subboard(self.board4, subpos)

        return succeeded

    def __place_piece_on_subboard(self, subboard, subpos):
        """Returns True if succeeded, and False if not."""
        succeeded = False

        if (subpos <= 3): # first row
            if self.__is_empty_spot(subboard[0][subpos-1]):
                subboard[0][subpos-1] = self.turn
                succeeded = True
        elif (subpos >= 3) and (subpos <= 5): # second row
            if self.__is_empty_spot(subboard[1][subpos%3-1]):
                subboard[1][subpos%3-1] = self.turn
                succeeded = True
        elif (subpos >= 6) and (subpos <= 9): # third row
            if self.__is_empty_spot(subboard[2][subpos%3-1]):
                subboard[2][subpos%3-1] = self.turn
                succeeded = True

        return succeeded

    def __is_empty_spot(self, val):
        """Returns if spot is empty in board."""
        if val == "0":
            return True
        else:
            return False

    def __rotate_board(self, rot):
        return True

    def __check_game_complete(self):
        """Checks if the game is over."""

        """
        Ideas:
        - Iterate through pieces horizontally, vertically, and diagonally, checking to see how many are in one line
        - ...
        """
        return
