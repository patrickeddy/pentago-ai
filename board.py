# Board module

empty_piece = "."

class GameBoard():
    def __init__(self):
        self.board1 = self.get_empty_board()
        self.board2 = self.get_empty_board()
        self.board3 = self.get_empty_board()
        self.board4 = self.get_empty_board()
        self.turn = "b"

    def end_game(self, winner):
        self.print_full_board()
        print("Game over! Winner is: " + str(winner))
        exit()

    def complete_turn(self):
        self.turn = "w" if self.turn == "b" else "b"

    def get_empty_board(self):
        return [[empty_piece, empty_piece, empty_piece], [empty_piece, empty_piece, empty_piece], [empty_piece, empty_piece, empty_piece]]

    def print_full_board(self):
        for i in range(6):
            print("") # add a new line for the board here
            if (i==0 or i == 3):
                print "+-------+-------+"
            for j in range(6):
                if j==0 or j == 3:
                    print "|",
                if (j < 3):
                    if (i < 3):
                        # first board
                        print str(self.board1[i][j]),
                    else:
                        # third board
                        print str(self.board3[i%3][j]),
                else:
                    if (i < 3):
                        # second board
                        print str(self.board2[i][j%3]),
                    else:
                        # fourth board
                        print str(self.board4[i%3][j%3]),
                if j==5:
                    print "|",
            if i==5:
                print "\n+-------+-------+"
        print("")

    # ===================
    # PLAY MOVE
    # ===================

    def play_move(self, color, move):
        """Completes a move for a player."""
        parts = move.split(" ")

        pos = parts[0]
        rot = parts[1]

        pp_success = self.__place_piece(color, pos)
        rb_success = self.__rotate_board(rot)

        # print("Placing piece status: " + str(pp_success))
        # print("Rotating board status: " + str(rb_success))

        boards = {
            "board1": self.board1,
            "board2": self.board2,
            "board3": self.board3,
            "board4": self.board4
        }
        winner = self.__check_game_complete(boards) # check for winner with the current boards

        if winner: # Won the game!
            self.end_game(winner)

        return pp_success and rb_success

    def place_piece(self, color, pos):
        """Helper method to access private method."""
        self.__place_piece(color, pos)

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
        elif (subpos >= 4) and (subpos <= 6): # second row
            if self.__is_empty_spot(subboard[1][subpos%3-1]):
                subboard[1][subpos%3-1] = self.turn
                succeeded = True
        elif (subpos >= 7) and (subpos <= 9): # third row
            if self.__is_empty_spot(subboard[2][subpos%3-1]):
                subboard[2][subpos%3-1] = self.turn
                succeeded = True

        return succeeded

    def __is_empty_spot(self, val):
        """Returns if spot is empty in board."""
        if val == empty_piece:
            return True
        else:
            return False

    def do_rotation(self, rot):
        """Helper function for hook into private method."""
        self.__rotate_board(rot)

    def __rotate_board(self, rot):
        """Translates rotation command."""
        b = rot[0] # board
        d = rot[1] # direction

        if b == "1":
            return self.__do_rotation(self.board1, d)
        elif b == "2":
            return self.__do_rotation(self.board2, d)
        elif b == "3":
            return self.__do_rotation(self.board3, d)
        elif b == "4":
            return self.__do_rotation(self.board4, d)

    def __do_rotation(self, board, direction):
        """Rotates pieces on a board."""
        success = False
        new_board = self.get_empty_board()
        if direction == "L":
            new_board[0][0] = board[0][2]
            new_board[0][1] = board[1][2]
            new_board[0][2] = board[2][2]
            new_board[1][0] = board[0][1]
            new_board[1][1] = board[1][1]
            new_board[1][2] = board[2][1]
            new_board[2][0] = board[0][0]
            new_board[2][1] = board[1][0]
            new_board[2][2] = board[2][0]
            for i in range(3):
                for j in range(3):
                    board[i][j] = new_board[i][j]
            success = True

        elif direction == "R":
            new_board[0][0] = board[2][0]
            new_board[0][1] = board[1][0]
            new_board[0][2] = board[0][0]
            new_board[1][0] = board[2][1]
            new_board[1][1] = board[1][1]
            new_board[1][2] = board[0][1]
            new_board[2][0] = board[2][2]
            new_board[2][1] = board[1][2]
            new_board[2][2] = board[0][2]
            for i in range(3):
                for j in range(3):
                    board[i][j] = new_board[i][j]
            success = True

        return success

    # ===================
    # CHECK GAME COMPLETE
    # ===================
    def __check_game_complete(self, boards):
        """Checks if the game is over and returns the winner."""
        b_win = self.__check_color_win_diag("b", boards) # check diagonal win first
        w_win = self.__check_color_win_diag("w", boards)

        if not (b_win or w_win): # no diagonal win...
            for x in range(6): # now check the vertical and horizontal wins
                b_win = self.__check_color_win_vert(x, "b", boards) or self.__check_color_win_horiz(x, "b", boards)
                w_win = self.__check_color_win_vert(x, "w", boards) or self.__check_color_win_horiz(x, "w", boards)

                if b_win or w_win:
                    break # break this loop if we found the winner

        winner = None
        if b_win:
            winner = "b"
        elif w_win:
            winner = "w"

        return winner

    def __check_color_win_vert(self, it, color, boards):
        if it <= 2:
            # left half
            if ((boards["board1"][0][it] == color
                    and boards["board1"][1][it] == color
                    and boards["board1"][2][it] == color
                    and boards["board3"][0][it] == color
                    and boards["board3"][1][it] == color) # first case for win
                or (boards["board1"][1][it] == color
                    and boards["board1"][2][it] == color
                    and boards["board3"][0][it] == color
                    and boards["board3"][1][it] == color
                    and boards["board3"][2][it] == color)): # second case for win (shifted by 1)
                return True
        else:
            # right half
            if ((boards["board2"][0][it%3] == color
                    and boards["board2"][1][it%3] == color
                    and boards["board2"][2][it%3] == color
                    and boards["board4"][0][it%3] == color
                    and boards["board4"][1][it%3] == color) # first case for win
                or (boards["board2"][1][it%3] == color
                    and boards["board2"][2][it%3] == color
                    and boards["board4"][0][it%3] == color
                    and boards["board4"][1][it%3] == color
                    and boards["board4"][2][it%3] == color)): # second case for win (shifted by 1)
                return True


    def __check_color_win_horiz(self, it, color, boards):
        if it <= 2:
            # top half
            if ((boards["board1"][it][0] == color
                    and boards["board1"][it][1] == color
                    and boards["board1"][it][2] == color
                    and boards["board2"][it][0] == color
                    and boards["board2"][it][1] == color) # first case for win
                or (boards["board1"][it][1] == color
                    and boards["board1"][it][2] == color
                    and boards["board2"][it][0] == color
                    and boards["board2"][it][1] == color
                    and boards["board2"][it][2] == color)): # second case for win (shifted by 1)
                return True
        else:
            # bottom half
            if ((boards["board3"][it%3][0] == color
                    and boards["board3"][it%3][1] == color
                    and boards["board3"][it%3][2] == color
                    and boards["board4"][it%3][0] == color
                    and boards["board4"][it%3][1] == color) # first case for win
                or (boards["board3"][it%3][1] == color
                    and boards["board3"][it%3][2] == color
                    and boards["board4"][it%3][0] == color
                    and boards["board4"][it%3][1] == color
                    and boards["board4"][it%3][2] == color)): # second case for win (shifted by 1)
                return True


    def __check_color_win_diag(self, color, boards):
        # There are only four ways you can win diagonally
        if ((boards["board1"][0][0] == color
              and boards["board1"][1][1] == color
              and boards["board1"][2][2] == color
              and boards["board4"][0][0] == color
              and boards["board4"][1][1] == color)
            or (boards["board1"][1][1] == color
              and boards["board1"][2][2] == color
              and boards["board4"][0][0] == color
              and boards["board4"][1][1] == color
              and boards["board4"][2][2] == color)
            or (boards["board2"][0][2] == color
              and boards["board2"][1][1] == color
              and boards["board2"][2][0] == color
              and boards["board3"][0][2] == color
              and boards["board3"][1][1] == color)
            or (boards["board2"][1][1] == color
              and boards["board2"][2][0] == color
              and boards["board3"][0][2] == color
              and boards["board3"][1][1] == color
              and boards["board3"][2][0] == color)):
            return True
        else:
            return False
