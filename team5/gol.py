from __future__ import unicode_literals

from itertools import product
from numpy import matrix
from random import random
from time import sleep
from os import system


class Board:
    ALIVE = '*'
    DEATH = ' '

    def __init__(self, height, width):
        self.matrix = matrix([[False] * width] * height)
        self.height = height
        self.width = width

    def iter(self):
        return ((i, j) for i, j in product(range(self.height),
                                           range(self.width)))

    def populate(self):
        for i, j in self.iter():
            self.matrix[i, j] = random() > 0.5

    def neighbours(self, x, y):
        for i, j in product(*[[-1, 0, 1]]*2):
            if not i == j == 0:
                i += x
                j += y
                if 0 <= i < self.height and 0 <= j < self.width:
                    yield self.matrix[i, j]

    def tick(self):
        following = Board(self.height, self.width)
        for i, j in self.iter():
            state = self.matrix[i, j]
            neighbours = list(self.neighbours(i, j)).count(True)
            if neighbours < 2 or neighbours > 3:
                state = False
            elif neighbours == 3:
                state = True
            following.matrix[i, j] = state
        return following

    def __repr__(self):
        return '\n'.join([' '.join(self.ALIVE if state else self.DEATH
                                   for state in row)
                          for row in self.matrix.tolist()])


if __name__ == '__main__':
    from colorama import init, Fore, Back
    init()
    board = Board(40, 40)
    board.populate()
    for i in range(1000):
        system('clear')
        print(Back.RED + Fore.GREEN + repr(board))
        board = board.tick()
        sleep(.1)
