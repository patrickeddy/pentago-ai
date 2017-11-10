# AI Module

from board import GameBoard

class AI():
    def __init__(self, color):
        self.color = color

    def move(self, board):
        """Finds best move via Minimax alpha-beta pruning, and makes the move."""
        start_node = Node(board, self.color, [board.board1, board.board2, board.board3, board.board4]) # creates the start node for alphabeta
        (best_move, heuristic) = self.alphabeta(start_node, 2, 99999, -99999, True)
        print("best move was: " + str(best_move))
        board.play_move(self.color, best_move) # ai makes move

    def alphabeta(self, node, depth, alpha, beta, maxPlayer):
        if depth = 0:
            return node.get_utility()

        node.get_move_options() # gets and sets the children for the node

        if node.color == maxPlayer:
            node.v = -99999
            for child in node.children:
                node.v = max(node.v, self.alphabeta(child, depth-1, alpha, beta, False)) # going to the min player
                alpha = max(alpha, node.v) # get the max of the nodes utility or alpha
                if beta <= alpha:
                    break # cut off this node subtree
            return (node.move, node.v)
        else:
            node.v = 99999
            for child in node.children:
                node.v = min(node.v, self.alphabeta(child, depth-1, alpha, beta, True))
                beta = min(beta, node.v)
                if beta <= alpha:
                break # cut off this node subtree

            return (node.move, node.v)

class Node():
    def __init__(self, game_board, color, boards):
        self.gb = game_board                        # primary GameBoard that manages the game
        self.opp_color = color                      # make parent color the opposing color
        self.color = "b" if color == "w" else "w"   # alternate color as Node is created from parent
        # Found this array deepcopy solution from Ryan Ye at stackoverflow.com/a/6533065
        self.board1 = [row[:] for row in boards[0]] # copy all of the boards into this one
        self.board2 = [row[:] for row in boards[1]]
        self.board3 = [row[:] for row in boards[2]]
        self.board4 = [row[:] for row in boards[3]]

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
        return move

    def get_utility(self):
        """Updates the utility value of this node based on a heuristic."""
        winning_score = 99999   # Winner
        three_row = 100         # 3
        two_row = 50            # 2
        node_boards = {
            "board1": self.board1,
            "board2": self.board2,
            "board3": self.board3,
            "board4": self.board4
        }
        winner = self.gb.check_game_complete_for_boards(node_boards)
        if winner == self.color:
            # if game is complete for this node, make utility winner
            return winning_score
        else:
            return self.__get_h(node_boards, two_row, three_row)

    def __get_h(self, boards, two_row_score, three_row_score):
        # checks if it has at least three or two in a row
        score = 0
        three_row = False
        two_row = False
        for board in boards.values():
            # DIAGONAL RATING
            # 2inrow - four different ways
            if (board[0][0] == self.color
                and board[0][1] == self.color)
                or (board[1][1] == self.color
                    and board[2][2] == self.color)
                or (board[0][2] == self.color
                    and board[1][1] == self.color)
                or (board[1][1] == self.color
                    and board[2][2] == self.color):
                    score += two_row_score
            # 3inrow - two different ways
            if (board[0][0] == self.color
                and board[1][1] == self.color
                and board[2][2] == self.color)
                or (board[0][2] == self.color
                    and board[1][1] == self.color
                    and board[2][0] == self.color):
                    score += three_row_score

            # HORIZONTAL/VERTICAL RATING
            for (i in range(3)):
                # check threeinrow
                if (board[i][0] == self.color # horizontal
                    and board[i][1] == self.color
                    and board[i][2] == self.color)
                    or (board[0][i] == self.color
                        and board[1][i] == self.color
                        and board[2][i] == self.color) # vertical
                    score += three_row_score

                if (i<2): # skip the twoinrow checking if we're checking row/col #3
                    for (j in range(2)):
                        # check twoinrow
                        if (board[i][j] == self.color
                            and board[i][j+1] == self.color): # check horizonal
                            score += two_row_score
                        if (board[i][j] == self.color
                            and board[i+1][j] == self.color): # check vertical
                            score += two_row_score

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
