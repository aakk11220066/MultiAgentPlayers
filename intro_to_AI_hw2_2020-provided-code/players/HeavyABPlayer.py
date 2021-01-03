"""
MiniMax Player with AlphaBeta pruning with heavy heuristic
"""
from players.AbstractPlayer import AbstractPlayer
from SearchAlgos import AlphaBeta
from utils import get_directions
# TODO: return imports to original absolute format
import numpy as np
import time
import copy


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time,
                                penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()

        self.greys = set()
        self.my_loc = (-1, -1)
        self.opp_loc = (-1, -1)
        self.fruits = {}
        self.board = []
        self.board_height = 0
        self.board_width = 0
        self.alphabeta = AlphaBeta(self.utility, self.succ, self.perform_move)
        self.fruits_turns = 0
        self.my_points = 0
        self.opp_points = 0
        self.turn_end_time = 0

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
        self.fruits_turns = min(self.board_height, self.board_width)
        # Get squares classes
        row_index = 0
        for row in board:
            col_index = 0
            for col in row:
                if col == 0:
                    pass
                elif col == -1:
                    self.greys.add((row_index, col_index))
                elif col == 1:
                    self.my_loc = (row_index, col_index)
                elif col == 2:
                    self.opp_loc = (row_index, col_index)
                else:
                    self.fruits[(row_index, col_index)] = col
                col_index += 1
            row_index += 1
        self.greys.add(self.my_loc)
        self.greys.add(self.opp_loc)

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        # TODO: erase the following line and implement this function.
        self.turn_end_time = np.inf
        depth = 2
        move = self.alphabeta.search(self, depth, True)

        new_loc = (move[1][0] + self.my_loc[0], move[1][1] + self.my_loc[1])
        if new_loc in self.greys:
            return None
        self.greys.add(new_loc)
        self.my_loc = new_loc
        if new_loc in self.fruits.keys():
            self.my_points += self.fruits[new_loc]
            self.fruits.pop(new_loc)

        self.decrease_fruit_turns()

        return move[1]

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

    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        # TODO: erase the following line and implement this function. In case you choose not to use this function,
        # use 'pass' instead of the following line.
        pass

    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed
    def __str__(self):
        return 'My Location : ' + str(self.my_loc) + '\n' + 'Opp Location : ' + str(self.opp_loc) + '\n' + str(
            self.hueristic(self))

    def decrease_fruit_turns(self):
        if self.fruits_turns == 0:
            self.fruits = {}
            return
        self.fruits_turns -= 1
        if self.fruits_turns == 0:
            self.fruits = {}

    ########## helper functions for AlphaBeta algorithm ##########
    def utility(self, state, heuristics, maximizing_player):
        assert isinstance(state, Player)
        if heuristics:
            return self.hueristic(state, maximizing_player=maximizing_player)
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
        new_loc = (loc[0] + direction[0], loc[1] + direction[1])
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

    def manhattanDistance(self, loc1, loc2):
        return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

    def hueristic(self, state, maximizing_player: bool):
        # Need to be fine-tuned
        sum_fruit_weight = 0.1
        closest_fruit_weight = 0.3
        relative_freedom_weight = 1

        score = state.my_points - state.opp_points  # heuristic 1

        closest_fruit_dist = float("inf")
        for fruit_loc in state.fruits:
            if self.manhattanDistance(state.my_loc, fruit_loc) <= state.fruits_turns:
                # print(f"I am at {self.my_loc}, fruit of value {state.fruits[fruit_loc]} is at {fruit_loc} with distance {self.manhattanDistance(self.my_loc, fruit_loc)} and remaining fruit turns {self.fruits_turns}")
                score += sum_fruit_weight * 1 / (0.1 + self.manhattanDistance(state.my_loc, fruit_loc)) * state.fruits[
                    fruit_loc]  # heuristic 2
                closest_fruit_dist = min(closest_fruit_dist, self.manhattanDistance(state.my_loc, fruit_loc))

        score += closest_fruit_weight / closest_fruit_dist  # heuristic 3

        opp_freedom = 4
        my_freedom = 4
        for direction in get_directions():
            opponent_neighbor = (self.opp_loc[0] + direction[0], self.opp_loc[1] + direction[1])
            if opponent_neighbor[0] < 0 \
                    or opponent_neighbor[0] > (state.board_height - 1) \
                    or opponent_neighbor[1] < 0 \
                    or opponent_neighbor[1] > (state.board_width - 1) \
                    or opponent_neighbor in self.greys:
                opp_freedom -= 1
            my_neighbor = (self.my_loc[0] + direction[0], self.my_loc[1] + direction[1])
            if my_neighbor[0] < 0 \
                    or my_neighbor[0] > (state.board_height - 1) \
                    or my_neighbor[1] < 0 \
                    or my_neighbor[1] > (state.board_width - 1) \
                    or my_neighbor in self.greys:
                my_freedom -= 1
        score += relative_freedom_weight * (my_freedom - opp_freedom)  # heuristic 4
        return score
