import time
import os
import sys

# The size of the board
x_size = 40
y_size = 40

# Game rules - at what number of neighbours should a cell be born or die?
born = [3]
die = [0, 1, 4, 5, 6]


def create_new_grid():
    return [[0 for col in range(x_size)] for row in range(y_size)]


def print_grid(grid):
    os.system('clear')
    for line in grid:
        line_string = ""
        for item in line:
            line_string += ("■" if item else " ") + " "
        print(line_string)


def sum_neighbours(grid, x, y):
    sum = -grid[y][x]
    for y2 in range(y-1, y+2):
        if y2 > y_size-1:
            y2 = 0
        for x2 in range(x-1, x+2):
            if x2 > x_size-1:
                x2 = 0
            sum += grid[y2][x2]
    return sum


def evolve(grid):
    new_grid = create_new_grid()
    for y in range(y_size):
        for x in range(x_size):
            i = grid[y][x]
            s = sum_neighbours(grid, x, y)
            new = i
            if i == 0:  # dead
                if s in born:
                    new = 1
            else:  # alive
                if s in die:
                    new = 0

            new_grid[y][x] = new

    # stop on a stale grid
    if grid == new_grid:
        sys.exit()

    return new_grid


def insert(grid, pattern, x, y):
    for y2, row in enumerate(pattern):
        for x2, value in enumerate(row):
            grid[y + y2][x + x2] = value

# Define some 'creatures'
blinker = [
    [0, 0, 0],
    [1, 1, 1],
    [0, 0, 0]
]

glider = [
    [0, 0, 1],
    [1, 0, 1],
    [0, 1, 1]
]

acorn = [
    [0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 1]
]

# Create the initial grid & add creatures
first_grid = create_new_grid()

insert(first_grid, acorn, x_size//2, y_size//2)
# insert(first_grid, glider, 1, 1)
# insert(first_grid, glider, 5, 1)
# insert(first_grid, glider, 10, 5)
# insert(first_grid, blinker, 17, 10)
# insert(first_grid, glider, 12, 1)

# Main loop
grid = first_grid
generation = 0
while True:
    print_grid(grid)
    generation += 1
    print("generation {0}".format(generation))
    grid = evolve(grid)
    time.sleep(0.05)
