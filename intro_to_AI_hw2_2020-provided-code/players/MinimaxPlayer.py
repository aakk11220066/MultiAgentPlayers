"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
from SearchAlgos import MiniMax
from utils import get_directions
import copy


# TODO: you can import more modules, if needed
import random

class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time,
                                penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        # TODO: initialize more fields, if needed, and the Minimax algorithm from SearchAlgos.py
        self.greys = set()
        self.my_loc = (-1, -1)
        self.opp_loc = (-1, -1)
        self.fruits = {}
        self.board = []
        self.board_height = 0
        self.board_width = 0
        self.minimax = MiniMax(self.utility, self.succ, self.perform_move)
        self.fruits_turns = 0
        self.my_points = 0
        self.opp_points = 0

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        self.board = board
        self.board_height = len(board)
        self.board_width = len(board[0])
        self.fruits_turns = self.board_height if self.board_height < self.board_width else self.board_width
        # Get squares classes
        row_index = 0
        col_index = 0
        for row in board:
            for col in row:
                if col == 0:
                    continue
                elif col == -1:
                    self.greys.add((row_index, col_index))
                elif col == 1:
                    self.my_loc = (row_index, col_index)
                elif col == 2:
                    self.opp_loc = (row_index, col_index)
                else:
                    self.fruits[(row_index, col_index)] = col

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        # TODO: erase the following line and implement this function.
        a = self.minimax.search(self, 3, True)
        print(a[0])
        print(a[1])
        return a[1]
        raise NotImplementedError

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        # TODO: erase the following line and implement this function.
        self.greys.add(pos)
        self.opp_loc = pos
        if pos in self.fruits.keys():
            self.opp_points += self.fruits[pos]
            self.fruits.pop(pos)
        self.decrease_fruit_turns()

    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        # TODO: erase the following line and implement this function. In case you choose not to use it, use 'pass' instead of the following line.
        pass

    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed
    def decrease_fruit_turns(self):
        self.fruits_turns -= 1
        if self.fruits_turns == 0:
            self.fruits = {}

    ########## helper functions for MiniMax algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm
    def utility(self, state, heuristics, maximizing_player):
        assert isinstance(state, Player)
        if heuristics:
            return self.hueristic(state)
        if maximizing_player:
            return state.my_points - state.opp_points - self.penalty_score
        return state.my_points - state.opp_points + self.penalty_score

    def succ(self, state, maximizing_player):
        succs = []
        for direction in get_directions():
            succs.append(self.perform_move(state, direction, maximizing_player))

        return succs

    def perform_move(self, state, direction, maximizing_player):
        assert (isinstance(state, Player))
        new_state = copy.deepcopy(state)
        loc = state.my_loc if maximizing_player else state.opp_loc
        new_loc = loc + direction
        if new_loc[0] < 0 or new_loc[0] > (state.board_height - 1) or new_loc[1] < 0 or new_loc[1] > (
                state.board_width - 1):
            return None
        if new_loc in state.greys:
            return None
        new_state.greys.add(new_loc)
        if maximizing_player:
            new_state.my_loc = new_loc
        else:
            new_state.opp_loc = new_loc
        if new_loc in state.fruits.keys():
            if maximizing_player:
                new_state.my_points += new_state.fruits[new_loc]
            else:
                new_state.opp_points += new_state.fruits[new_loc]
            new_state.fruits.pop(new_loc)
        new_state.decrease_fruit_turns()
        return new_state

    def hueristic(self, state):
        return random.randint(0,2)
        pass
