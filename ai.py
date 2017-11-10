# AI Module

from board import GameBoard

class AI():
    def __init__(self, color):
        self.color = color

    def move(self, board):
        """Finds best move via Minimax alpha-beta pruning, and makes the move."""
        start_node = Node(self.color, [board.board1, board.board2, board.board3, board.board4]) # creates the start node for alphabeta
        # winner = self.alphabeta(start_node, 2, 9999, -9999, self.color)

    def alphabeta(self, node, depth, alpha, beta, maxPlayer):
        return


class Node():
    def __init__(self, color, boards):
        self.color = "b" if color == "w" else "w" # alternate color as Node is created from parent
        # Found this array deepcopy solution from Ryan Ye at stackoverflow.com/a/6533065
        self.board1 = [row[:] for row in boards[0]] # copy all of the boards into this one
        self.board2 = [row[:] for row in boards[1]]
        self.board3 = [row[:] for row in boards[2]]
        self.board4 = [row[:] for row in boards[3]]

        # Node utilities
        self.move = ""
        self.v = 0
        self.children = []

    def __get_move_options(self):
        """Gets the permutations."""
        empties = self.__get_empty_spots()
        moves = []
        for (subboard, pos) in empties:
            # for each empty spot (max 36), create 8 nodes that use it (rotate 1,2,3,4 left/right)
            m1 = self.__get_move_for_rotation(subboard, pos, "1L")
            m2 = self.__get_move_for_rotation(subboard, pos, "1R")

            m3 = self.__get_move_for_rotation(subboard, pos, "2L")
            m4 = self.__get_move_for_rotation(subboard, pos, "2R")

            m5 = self.__get_move_for_rotation(subboard, pos, "3L")
            m6 = self.__get_move_for_rotation(subboard, pos, "3R")

            m7 = self.__get_move_for_rotation(subboard, pos, "4L")
            m8 = self.__get_move_for_rotation(subboard, pos, "4R")

            moves.append(m1, m2, m3, m4, m5, m6, m7, m8)

        self.children = moves

    def __get_move_for_rotation(self, subboard, pos, rot):
        """Gets the permutation based on the piece placement and rotation."""
        move = Node(self.__get_boards()) # creates a new node with these boards
        move.move = str(subboard) + "/" + str(pos) + str(rot) # assign the move to this node
        move.place_piece(self.color, str(subboard) + "/" + str(pos)) # place piece
        move.do_rotation(rot) # do rotation
        move.update_utility() # update the utility value of the node
        return move

    def __update_utility(self):
        """Updates the utility value of this node based on a heuristic."""
        # Winner +1000
        # 3 in a row +200
        # 2 in a row +50
        

        return


    def __get_boards(self):
        return [self.board1, self.board2, self.board3, self.board4]

    def __get_empty_spots(self):
        """Gets the open spots for placement."""
        spots = []
        marker = "."
        for i in range(6):
            for j in range(6):
                if (j < 3):
                    if (i < 3):
                        # first board
                        if self.board1[i][j] == marker:
                            spots.append(("1", (i*3)+(j+1)) ) # get the subboard and pos
                    else:
                        # third board
                        if self.board3[i%3][j] == marker:
                            spots.append(("3", (i*3)+(j+1)) )
                else:
                    if (i < 3):
                        # second board
                        if self.board2[i][j%3] == marker:
                            spots.append(("2", (i*3)+(j+1)) )
                    else:
                        # fourth board
                        if self.board4[i%3][j%3] == marker:
                            spots.append(("4", (i*3)+(j+1)) )
        return spots
