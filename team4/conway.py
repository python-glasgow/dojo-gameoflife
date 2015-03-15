import sys
import time
import numpy as np
import os

def display(grid):
	os.system('clear')
	topbot = '+' + '-'*(grid.shape[0]*2-1) + '+'
	print topbot
	for i in range(grid.shape[0]):
		row = '|'
		for j in range(grid.shape[1]):
			row += '* ' if grid[i][j] else '  '
		print row[:-1]+'|'
	print topbot
	time.sleep(0.1)

def get_state(i, j, grid):
	surroundings = grid[[i-1,i-1,i-1,i,i,i+1,i+1,i+1],[j-1,j,j+1,j-1,j+1,j-1,j,j+1]]
	alive_neighbours = np.count_nonzero(surroundings)
	alive = grid[i][j]
	if alive and alive_neighbours in {2,3}:
		return 1
	if not alive and alive_neighbours == 3:
		return 1
	return 0

def run(grid, x, y):
	while True:
		display(grid)
		grid = np.pad(grid, 1, mode='wrap')
		new_grid = np.zeros((x, y), dtype=np.int)
		for i in range(1, x+1):
			for j in range(1, y+1):
				new_grid[i-1][j-1] = get_state(i, j, grid)
		grid = new_grid
	return grid


if __name__ == '__main__':
	x = int(sys.argv[1])
	y = int(sys.argv[2])

	conway_grid = np.random.randint(2, size=(x, y))
	#conway_grid = np.zeros((5,5), dtype=np.int)
	#conway_grid[2,1] = 1
	#conway_grid[2,2] = 1
	#conway_grid[2,3] = 1
	run(conway_grid, x, y)
	
