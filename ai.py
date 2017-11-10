# AI Module

from board import GameBoard
from random import randint
from copy import deepcopy

class AI():
    def __init__(self, color):
        self.color = color

    def move(self, board):
        """Finds best move via Minimax alpha-beta pruning, and makes the move."""
        boards = {
            "board1": board.board1,
            "board2": board.board2,
            "board3": board.board3,
            "board4": board.board4
        }
        # creates the start node for alphabeta
        start_node = Node(board, self.color, boards)
        # get the heuristic and best move
        h = self.alphabeta(start_node, 500, 99999, -99999, True)
        print("h is: " + str(h))
        best_move = self.__get_best_move_from_h(start_node, h)

        print("Winning move is: " + str(best_move))

        # ai makes the move
        board.play_move(self.color, best_move)

    def __get_best_move_from_h(self, node, h):
        """Fetches the actual move from the children based on the heuristic."""
        if h == 0:
            # if the best heuristic is 0, pick a random place
            subboard = randint(1,4)
            pos = randint(1,9)
            rotb = randint(1,4)
            rotd = randint(1,2)
            direction = "L" if rotd == 1 else "R"
            return str(subboard) + "/" + str(pos) + " " + str(rotb) + str(direction)
        else:
            for child in node.children:
                # print("child move: " + str(child.move))
                # print("child v: " + str(child.v))
                if child.v == h:
                    # found the child, get the move
                    return child.move

    def alphabeta(self, node, depth, alpha, beta, maxPlayer):
        # print("node move: " + str(node.move))
        # print("node v: " + str(node.v))

        if depth == 0:
            # print("utility is: " + str(node.get_utility()))
            return node.get_utility()

        node.get_move_options() # gets and sets the children for the node

        if maxPlayer:
            node.v = -99999
            for child in node.children:
                node.v = max(node.v, self.alphabeta(child, depth-1, alpha, beta, False)) # going to the min player
                alpha = max(alpha, node.v) # get the max of the nodes utility or alpha
                if beta <= alpha:
                    break # cut off this node subtree
            return node.v
        else:
            node.v = 99999
            for child in node.children:
                node.v = min(node.v, self.alphabeta(child, depth-1, alpha, beta, True))
                beta = min(beta, node.v)
                if beta <= alpha:
                    break # cut off this node subtree

            return node.v

class Node():
    def __init__(self, game_board, color, boards):
        self.gb = game_board                        # primary GameBoard that manages the game
        self.color = color
        self.board1 = deepcopy(boards["board1"]) # copy all of the boards into this one
        self.board2 = deepcopy(boards["board2"])
        self.board3 = deepcopy(boards["board3"])
        self.board4 = deepcopy(boards["board4"])

        # Node utilities
        self.move = ""
        self.v = 0
        self.children = []

    def get_move_options(self):
        """Gets the permutations."""
        empties = self.__get_empty_spots()
        moves = []
        for (subboard, pos) in empties:
            # for each empty spot (max 36), create 8 nodes that use it (rotate 1,2,3,4 left/right)
            m1 = self.__get_move_for(subboard, pos, "1L")
            m2 = self.__get_move_for(subboard, pos, "1R")

            m3 = self.__get_move_for(subboard, pos, "2L")
            m4 = self.__get_move_for(subboard, pos, "2R")

            m5 = self.__get_move_for(subboard, pos, "3L")
            m6 = self.__get_move_for(subboard, pos, "3R")

            m7 = self.__get_move_for(subboard, pos, "4L")
            m8 = self.__get_move_for(subboard, pos, "4R")

            moves.extend([m1, m2, m3, m4, m5, m6, m7, m8])

        self.children.extend(moves)

    def __get_board_dict(self):
        return {
            "board1": self.board1,
            "board2": self.board2,
            "board3": self.board3,
            "board4": self.board4
        }

    def __get_move_for(self, subboard, pos, rot):
        """Gets the permutation based on the piece placement and rotation."""
        color = "b" if self.color == "w" else "w" # alternate colors
        actual_pos = pos

        move = Node(self.gb, color, self.__get_board_dict()) # creates a new node with these boards
        move.move = str(subboard) + "/" + str(actual_pos) + " " + str(rot) # assign the move to this node

        node_boards = self.__get_board_dict()
        self.gb.place_piece(self.color, str(subboard) + "/" + str(actual_pos), node_boards) # place piece
        self.gb.do_rotation(rot, node_boards) # do rotation
        # print("move: " + str(move.move))
        return move

    def get_utility(self):
        """Updates the utility value of this node based on a heuristic."""
        winning_score = 99999       # Winner
        winning_combo_score = 500   # 3 on one board, 2 on the other
        three_row_score = 100       # 3
        two_row_score = 50          # 2

        node_boards = self.__get_board_dict()
        winner = self.gb.check_game_complete_for_boards(node_boards)
        if winner == self.color:
            # if game is complete for this node, make utility winner
            return winning_score
        else:
            h = self.__get_h(two_row_score, three_row_score, winning_combo_score)
            return h

    def __get_h(self, two_row_score, three_row_score, winning_combo_score):
        # checks if it has at least three or two in a row
        score = 0
        conseq_tile_score = 50
        filled_spots = self.__get_filled_spots()

        for pos in filled_spots: # loop through all spots
            current_pos = pos
            # print("pos: " + str(pos))
            # check all diag up left
            while current_pos-7 in filled_spots:
                score += conseq_tile_score
                current_pos -= 7
            current_pos = pos # reset

            # check all up
            while current_pos-6 in filled_spots:
                score += conseq_tile_score
                current_pos -= 6
            current_pos = pos # reset

            # check all up diag right
            while current_pos-5 in filled_spots:
                score += conseq_tile_score
                current_pos -= 5
            current_pos = pos # reset

            # check all right
            while current_pos+1 in filled_spots:
                score += conseq_tile_score
                current_pos += 1
            current_pos = pos # reset

            # check all down diag right
            while current_pos+7 in filled_spots:
                score += conseq_tile_score
                current_pos += 7
            current_pos = pos # reset

            # check all down
            while current_pos+6 in filled_spots:
                score += conseq_tile_score
                current_pos += 6
            current_pos = pos # reset

            # check all down diag left
            while current_pos+5 in filled_spots:
                score += conseq_tile_score
                current_pos += 5
            current_pos = pos # reset

            while pos-1 in filled_spots: # check all left
                score += conseq_tile_score
                pos -= 1
            current_pos = pos # reset

            # # CHECK TWO IN A ROW
            # # diagonal
            # if (sb == "1" or sb == "3"): # if we're subboards 1 or 3
            #     if (pos % 3) < 3): # and we're not bordering another board
            #         if ((sb, pos-4) in filled_spots     # up diag left
            #             or
            #             or (sb, pos-2) in filled_spots  # up diag right
            #             or (sb, pos)
            #             ):
            #             score += two_row_score
            #     else: # we're bordering board
            #
            # else: # subboard 2 or 4


        # two_found_board = None
        # three_found_board = None

        # for board in boards.values():
        #     # DIAGONAL RATING
        #     # 2inrow - four different ways
        #     if ((board[0][0] == self.color
        #             and board[0][1] == self.color)
        #         or (board[1][1] == self.color
        #             and board[2][2] == self.color)
        #         or (board[0][2] == self.color
        #             and board[1][1] == self.color)
        #         or (board[1][1] == self.color
        #             and board[2][2] == self.color)):
        #             score += two_row_score
        #             two_found_board = board
        #
        #     # 3inrow - two different ways
        #     if ((board[0][0] == self.color
        #         and board[1][1] == self.color
        #         and board[2][2] == self.color)
        #         or (board[0][2] == self.color
        #             and board[1][1] == self.color
        #             and board[2][0] == self.color)):
        #             score += three_row_score
        #             three_found_board = board
        #
        #     if ((two_found_board and three_found_board)
        #         and two_found_board != three_found_board): # we found a winning combo
        #         score += winning_combo_score
        #         two_found_board = None
        #         three_found_board = None
        #
        #     # HORIZONTAL/VERTICAL RATING
        #     for i in range(3):
        #         # check threeinrow
        #         if ((board[i][0] == self.color # horizontal
        #             and board[i][1] == self.color
        #             and board[i][2] == self.color)
        #             or (board[0][i] == self.color
        #                 and board[1][i] == self.color
        #                 and board[2][i] == self.color)): # vertical
        #             score += three_row_score
        #             two_found_board = board
        #
        #         if (i<2): # skip the twoinrow checking if we're checking row/col #3
        #             for j in range(2):
        #                 # check twoinrow
        #                 if (board[i][j] == self.color
        #                     and board[i][j+1] == self.color): # check horizonal
        #                     score += two_row_score
        #                 if (board[i][j] == self.color
        #                     and board[i+1][j] == self.color): # check vertical
        #                     score += two_row_score
        #                     two_found_board = board
        #
        #         if ((two_found_board and three_found_board)
        #             and two_found_board != three_found_board): # we found a winning combo
        #             score += winning_combo_score
        #             two_found_board = None
        #             three_found_board = None

        return score

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
                            spots.append(("3", ((i%3)*3)+(j+1)) )
                else:
                    if (i < 3):
                        # second board
                        if self.board2[i][j%3] == marker:
                            spots.append(("2", (i*3)+((j%3)+1)) )
                    else:
                        # fourth board
                        if self.board4[i%3][j%3] == marker:
                            spots.append(("4", ((i%3)*3)+((j%3)+1)) )
        return spots

    def __get_filled_spots(self):
        """Gets the filled spots 1-36 on the board."""
        spots = []
        marker = self.color
        for i in range(6):
            for j in range(6):
                if (j < 3):
                    if (i < 3):
                        # first board
                        if self.board1[i][j] == marker:
                            spots.append((i*6)+j+1) # get pos 1-36
                    else:
                        # third board
                        if self.board3[i%3][j] == marker:
                            spots.append((i*6)+j+1)
                else:
                    if (i < 3):
                        # second board
                        if self.board2[i][j%3] == marker:
                            spots.append((i*6)+j+1)
                    else:
                        # fourth board
                        if self.board4[i%3][j%3] == marker:
                            spots.append((i*6)+j+1)
        return spots
