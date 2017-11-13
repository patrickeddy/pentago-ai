# AI Module

from board import GameBoard
from random import randint
from copy import deepcopy

class AI():
    def __init__(self, color):
        self.color = color
        self.nodes_expanded = 0

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

        self.nodes_expanded = 0 # reset nodes expanded to zero before alg

        # get the heuristic and best move
        # h = self.minimax(start_node, 2, True)                       # Minimax
        h = self.alphabeta(start_node, 2, -99999, 99999, True)    # Alpha-Beta
        best_move = self.__get_best_move_from_h(start_node, h)

        print(": " + str(best_move))

        # print("Nodes expanded: " + str(self.nodes_expanded))

        # ai makes the move
        board.play_move(self.color, best_move)

    def __get_best_move_from_h(self, node, h):
        """Fetches the actual move from the children based on the heuristic."""
        if h == 99999:
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

    def minimax(self, node, depth, maxPlayer):
        if depth == 0:
            # print("utility is: " + str(node.get_utility()))
            return node.get_utility()

        node.get_move_options() # gets and sets the children for the node

        if maxPlayer:
            best_value = -99999
            for child in node.children:
                self.nodes_expanded += 1

                node.v = self.minimax(child, depth-1, False) # going to the min player
                best_value = max(best_value, node.v) # get the max of the nodes

            return best_value
        else:
            best_value = 99999
            for child in node.children:
                self.nodes_expanded += 1

                node.v = self.minimax(child, depth-1, True)
                best_value = min(best_value, node.v)
            return best_value


    def alphabeta(self, node, depth, alpha, beta, maxPlayer):
        # print("node move: " + str(node.move))
        # print("node v: " + str(node.v))
        if depth == 0:
            # print("utility is: " + str(node.get_utility()))
            return node.get_utility()

        node.get_move_options() # gets and sets the children for the node

        if maxPlayer:
            node.v = -99999
            current_alpha = alpha
            for child in node.children:
                self.nodes_expanded += 1
                node.v = max(node.v, self.alphabeta(child, depth-1, current_alpha, beta, False)) # going to the min player
                current_alpha = max(current_alpha, node.v) # get the max of the nodes utility or alpha
                if beta <= current_alpha:
                    break # cut off this node subtree

            return node.v
        else:
            node.v = 99999
            current_beta = beta
            for child in node.children:
                self.nodes_expanded += 1
                node.v = min(node.v, self.alphabeta(child, depth-1, alpha, current_beta, True))
                current_beta = min(current_beta, node.v)
                if current_beta <= alpha:
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
        move = Node(self.gb, color, self.__get_board_dict()) # creates a new node with these boards
        move.move = str(subboard) + "/" + str(pos) + " " + str(rot) # assign the move to this node

        node_boards = self.__get_board_dict()
        self.gb.place_piece(self.color, str(subboard) + "/" + str(pos), node_boards) # place piece
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

        max_conseq = 0
        for pos in filled_spots: # loop through all spots

            # check all diag up left
            nc = self.__get_conseq_count(filled_spots, conseq_tile_score, pos, -7)
            max_conseq = nc if nc > max_conseq else max_conseq

            # check all up
            nc = self.__get_conseq_count(filled_spots, conseq_tile_score, pos, -6)
            max_conseq = nc if nc > max_conseq else max_conseq

            # check all up diag right
            nc = self.__get_conseq_count(filled_spots, conseq_tile_score, pos, -5)
            max_conseq = nc if nc > max_conseq else max_conseq

            # check all right
            nc = self.__get_conseq_count(filled_spots, conseq_tile_score, pos, 1)
            max_conseq = nc if nc > max_conseq else max_conseq

            # check all down diag right
            nc = self.__get_conseq_count(filled_spots, conseq_tile_score, pos, 7)
            max_conseq = nc if nc > max_conseq else max_conseq

            # check all down
            nc = self.__get_conseq_count(filled_spots, conseq_tile_score, pos, 6)
            max_conseq = nc if nc > max_conseq else max_conseq

            # check all down diag left
            nc = self.__get_conseq_count(filled_spots, conseq_tile_score, pos, 5)
            max_conseq = nc if nc > max_conseq else max_conseq

            # check all left
            nc = self.__get_conseq_count(filled_spots, conseq_tile_score, pos, -1)
            max_conseq = nc if nc > max_conseq else max_conseq


            if max_conseq  <= 2:
                score = max_conseq * 100
            elif max_conseq <= 4:
                score = max_conseq * 1000

        return score

    def __get_conseq_count(self, filled_spots, conseq_tile_score, pos, vector):
        """Find the max conseq count for direction."""
        current_pos = pos
        count = 0
        while current_pos+vector in filled_spots:
            current_pos += vector
            count += 1
        return count

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
                        if self.gb.board1[i][j] == marker:
                            spots.append(("1", (i*3)+(j+1)) ) # get the subboard and pos
                    else:
                        # third board
                        if self.gb.board3[i%3][j] == marker:
                            spots.append(("3", ((i%3)*3)+(j+1)) )
                else:
                    if (i < 3):
                        # second board
                        if self.gb.board2[i][j%3] == marker:
                            spots.append(("2", (i*3)+((j%3)+1)) )
                    else:
                        # fourth board
                        if self.gb.board4[i%3][j%3] == marker:
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
