import numpy as np
import random
from enum import Enum
import os
import time
clear = lambda: os.system('clear')
clear()


class StateError(ValueError):
    pass

class GameState(Enum):
    BUSY = 0
    WAITING_FOR_MOVE_DECISION = 1
    WAITING_FOR_TAKE_DECISION = 2
    TAKE_DECISION_MADE = 3

class Game:
    def __init__(self, gui=None):
        self.gui = gui
        self.width = 8
        self.inventory = []
        marble_idxs = list(range(4*2*self.width))
        random.shuffle(marble_idxs)

        self.board = np.ones([4, self.width], np.object_)
        for i in range(4):
            for j in range(self.width):
                self.board[i, j] = []
                for k in range(2):
                    self.board[i, j].append(marble_idxs[i*self.width*2+j*2+k])

        self.active_player = 0
        self.active_hole = None
        self.take_hole = None
        self.direction = None
        self.state = GameState.WAITING_FOR_MOVE_DECISION

    def print_board(self, info=None):
        time.sleep(0.5)
        if self.gui:
            self.gui.repaint()

    def nboard(self):
        nboard = np.zeros([4, self.width], np.int8)
        for i in range(4):
            for j in range(self.width):
                nboard[i, j] = len(self.board[i, j])
        return nboard

    def turn(self, x, y, direction):
        if self.state == GameState.WAITING_FOR_MOVE_DECISION:
            self.state = GameState.BUSY
            self.direction = direction
            self._move([x, y], direction)
        else:
            raise StateError()

    def _flip(self):
        self.board = self.get_flipped()

    def get_flipped(self):
        return self.board[::-1, ::-1]

    def take_decision(self, take):
        if self.state == GameState.WAITING_FOR_TAKE_DECISION:
            if take:
                self.inventory += self._at(self.take_hole)
                self._set(self.take_hole, [])
            self.state = GameState.TAKE_DECISION_MADE
            self.take_hole = None
            self._move(self.active_hole, self.direction)
        else:
            raise StateError()

    def _move(self, starthole, direction):
        if len(self.inventory) == 1\
            and len(self._at(starthole)) > 0\
            and self._get_opposite(starthole)\
            and len(self._at(self._get_opposite(starthole))) > 0\
            and not self.state == GameState.TAKE_DECISION_MADE:
            self.active_hole = starthole
            self.take_hole = self._get_opposite(starthole)
            self.state = GameState.WAITING_FOR_TAKE_DECISION
            self.print_board()
            return

        self.state = GameState.BUSY

        self.inventory += self._at(starthole)
        self._set(starthole, [])
        hole = starthole
        self.active_hole = hole
        self.print_board()
        while len(self.inventory) > 1:
            hole = self.step(hole, direction)
        next_hole = self._get_next_hole(hole, direction)
        self.active_hole = next_hole
        if len(self._at(next_hole)) > 0:
            self._move(next_hole, direction)
        else:
            self._set(next_hole, self.inventory)
            self.inventory = []
            self.print_board()
            self.active_hole = None
            self._flip()
            self.active_player = (self.active_player + 1) % 2
            self.print_board()
            self.state = GameState.WAITING_FOR_MOVE_DECISION

    def step(self, hole, direction):
        next_hole = self._get_next_hole(hole, direction)
        self._add(next_hole, [self.inventory.pop()])
        self.active_hole = next_hole
        self.print_board()
        return next_hole

    def _at(self, hole):
        return self.board[hole[0], hole[1]]

    def _set(self, hole, value):
        self.board[hole[0], hole[1]] = value

    def _add(self, hole, value):
        self._set(hole, self._at(hole) + value)

    def _get_opposite(self, hole):
        if hole[0] == 1:
            return [2, hole[1]]
        else:
            return False

    def _get_next_hole(self, hole, direction):
        if hole[0] == 1:
            hole[1] = self.width - hole[1] - 1
        n_hole = hole[0] * self.width + hole[1]
        next_n_hole = np.int8((n_hole + direction) % (self.width * 2))
        next_hole = [np.floor_divide(next_n_hole, self.board.shape[1]), next_n_hole % self.width]
        if next_hole[0] == 1:
            next_hole[1] = self.width - next_hole[1] - 1
        return next_hole

#game = Game()
#game.start()
