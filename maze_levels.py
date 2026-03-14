import numpy as np
import random
from collections import deque

# ---------------------------
# Example predefined levels
# ---------------------------

level1 = np.array([
[0,0,0,0,1,0,1,0,0,1],
[1,1,0,1,0,1,1,0,1,0],
[0,1,0,0,0,1,0,0,1,1],
[0,1,0,1,0,0,0,1,0,1],
[1,0,1,0,0,1,0,1,1,0],
[0,1,0,1,0,0,0,0,0,1],
[0,0,0,0,1,0,1,0,0,1],
[1,1,0,1,0,1,1,0,0,0],
[0,1,0,1,0,1,0,0,1,0],
[0,1,1,0,0,0,1,1,1,0]
])

level2 = np.array([
[0,0,1,0,0,0,1,0,0,0],
[0,1,1,0,1,0,1,0,1,0],
[0,0,0,0,1,0,0,0,1,0],
[1,1,0,1,0,1,1,0,0,0],
[0,0,0,1,0,0,0,1,1,0],
[0,1,0,0,0,1,0,0,0,0],
[0,1,1,1,0,1,0,1,0,1],
[0,0,0,1,0,0,0,1,0,0],
[1,1,0,0,0,1,0,0,0,1],
[0,0,0,1,0,0,0,1,0,0]
])
# ----------------------------------
# Generate thousands of random mazes
# ----------------------------------

def generate_random_maze(size=10):

    maze = np.zeros((size,size), dtype=int)

    for i in range(size):
        for j in range(size):
            if random.random() < 0.3:
                maze[i][j] = 1

    maze[0][0] = 0
    maze[size-1][size-1] = 0

    return maze


# create dataset with 1000+ mazes
maze_dataset = [level1, level2]

for i in range(1000):
    maze_dataset.append(generate_random_maze())


def is_solvable(maze):

    rows, cols = maze.shape
    start = (0,0)
    goal = (rows-1,cols-1)

    queue = deque([start])
    visited = set([start])

    directions = [(1,0),(-1,0),(0,1),(0,-1)]

    while queue:

        x,y = queue.popleft()

        if (x,y) == goal:
            return True

        for dx,dy in directions:

            nx,ny = x+dx,y+dy

            if 0<=nx<rows and 0<=ny<cols:
                if maze[nx][ny]==0 and (nx,ny) not in visited:

                    visited.add((nx,ny))
                    queue.append((nx,ny))

    return False
maze_dataset = []

def generate_maze(size=10):

    while True:

        maze = np.random.randint(0,2,(size,size))

        maze[0][0] = 0
        maze[size-1][size-1] = 0

        if is_solvable(maze):
            return maze


for i in range(1000):
    maze_dataset.append(generate_maze())

