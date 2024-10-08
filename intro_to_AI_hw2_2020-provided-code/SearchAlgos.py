"""Search Algos: MiniMax, AlphaBeta
"""
from utils import ALPHA_VALUE_INIT, BETA_VALUE_INIT

# TODO: you can import more modules, if needed
import numpy as np
from utils import get_directions
import time


class SearchAlgos:
    def __init__(self, utility, succ, perform_move, goal=None):
        """The constructor for all the search algos.
        You can code these functions as you like to, 
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move

    def search(self, state, depth, maximizing_player):
        pass


class MiniMax(SearchAlgos):

    def search(self, state, depth, maximizing_player):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        if time.time() > state.turn_end_time:
            return 'interrupted'
        succs = self.succ(state, maximizing_player)
        # print(succs[0])
        if succs == [None, None, None, None]:
            return self.utility(state, False, maximizing_player), (0, 0)
        if depth == 0:
            return self.utility(state, True, maximizing_player), (0, 0)
        if maximizing_player:
            max_score = (-np.inf, (0, 0))
            index = 0
            empty = 0
            for succ in succs:
                if not succ:
                    index += 1
                    empty += 1
                    continue
                res = self.search(succ, depth - 1, False)
                if res == 'interrupted':
                    return 'interrupted'
                if res[0] > max_score[0]:
                    max_score = (res[0], get_directions()[index])
                index += 1
            return max_score
        else:
            min_score = (np.inf, (0, 0))
            index = 0
            empty = 0
            for succ in succs:
                if not succ:
                    index += 1
                    empty += 1
                    continue
                res = self.search(succ, depth - 1, True)
                if res == 'interrupted':
                    return 'interrupted'
                if res[0] < min_score[0]:
                    min_score = (res[0], None)
                index += 1
            return min_score


class AlphaBeta(SearchAlgos):

    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """

        if time.time() > state.turn_end_time:
            return 'interrupted'
        succs = self.succ(state, maximizing_player)
        # print(succs[0])
        if succs == [None, None, None, None]:
            return self.utility(state, False, maximizing_player), (0, 0)
        if depth == 0:
            return self.utility(state, True, maximizing_player), (0, 0)
        if maximizing_player:
            max_score = (-np.inf, (0, 0))
            index = 0
            empty = 0
            for succ in succs:
                if not succ:
                    index += 1
                    empty += 1
                    continue
                res = self.search(succ, depth - 1, False, alpha=alpha, beta=beta)
                if res == 'interrupted':
                    return 'interrupted'
                if res[0] > max_score[0]:
                    max_score = (res[0], get_directions()[index])
                alpha = max(max_score[0], alpha)
                if max_score[0] >= beta:
                    return np.inf, (0,0)
                index += 1
            return max_score
        else:
            min_score = (np.inf, (0, 0))
            index = 0
            empty = 0
            for succ in succs:
                if not succ:
                    index += 1
                    empty += 1
                    continue
                res = self.search(succ, depth - 1, True, alpha=alpha, beta=beta)
                if res == 'interrupted':
                    return 'interrupted'
                if res[0] < min_score[0]:
                    min_score = (res[0], None)
                beta = min(beta, min_score[0])
                if min_score[0] <= alpha:
                    return -np.inf, None
                index += 1
            return min_score

        # TODO: erase the following line and implement this function.
        raise NotImplementedError
