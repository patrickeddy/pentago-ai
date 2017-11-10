# AI Module

import GameBoard from board

class AI():
    def __init__(self, color, board):
        self.color = color

    def move(self, board):
        """Finds best move via Minimax alpha-beta pruning, and makes the move."""
        start_node = Node(board) # creates the start node for alphabeta
        winner = self.alphabeta(start_node, )

    def alphabeta(self, node, depth, alpha, beta, maxPlayer):
        return


class Node():
    def __init__(self, board):
        self.gb = board
        self.move = ""
        self.children = self.__get_move_options()

    def __get_move_options(self):
        """Gets the permutations."""
        empties = self.__get_empty_spots()
        moves = []
        for (subboard, pos) in empties:
            # for each empty spot, create 4 nodes that use it (rotate 1,2,3,4 left/right)
            m1 = self.__get_move_for_rotation("1L", subboard, pos)
            m2 = self.__get_move_for_rotation("1R", subboard, pos)
            m3 = self.__get_move_for_rotation("2L", subboard, pos)
            m4 = self.__get_move_for_rotation("2R", subboard, pos)
            m5 = self.__get_move_for_rotation("3L", subboard, pos)
            m6 = self.__get_move_for_rotation("3R", subboard, pos)
            m7 = self.__get_move_for_rotation("4L", subboard, pos)
            m8 = self.__get_move_for_rotation("4R", subboard, pos)

            moves.append(m1, m2, m3, m4, m5, m6, m7, m8)

        return moves

    def __get_move_for_rotation(self, rot, subboard, pos):
        ngb = self.gb.clone() #FIXME: Change so that board1, 2, 3, 4 are being copied
        ngb.place_piece(self.color, str(subboard) + "/" + str(pos)) # place piece
        ngb.do_rotation(rot) # do rotation
        return Node(ngb)


    def __get_empty_spots(self):
        """Gets the open spots for placement."""
        spots = []
        marker = "."
        for (i in range(6)):
            for (j in range(6)):
                if (j < 3):
                    if (i < 3):
                        # first board
                        if self.gb.board1[i][j] == marker:
                            spots.append(("1", (i*3)+(j+1)) ) # get the command
                    else:
                        # third board
                        if self.gb.board3[i%3][j] == marker:
                            spots.append(("3", (i*3)+(j+1)) ) # get the command
                else:
                    if (i < 3):
                        # second board
                        if self.gb.board2[i][j%3] == marker:
                            spots.append(("2", (i*3)+(j+1)) ) # get the command
                    else:
                        # fourth board
                        if self.board4[i%3][j%3] == marker:
                            spots.append(("4", (i*3)+(j+1)) ) # get the command
        return spots
