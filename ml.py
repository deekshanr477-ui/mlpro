import numpy as np
import tkinter as tk
from maze_levels import maze_dataset

CELL_SIZE = 50

# -------------------------------
# Level Dataset
# -------------------------------

level_index = 0
maze = maze_dataset[level_index]

start = (0,0)
goal = (9,9)

score = 0
visited = set()

# -------------------------------
# Tkinter Window
# -------------------------------

root = tk.Tk()
root.title("Autonomous Maze Agent")

title = tk.Label(
    root,
    text="Autonomous Game Agent : Maze Navigation",
    font=("Arial",18,"bold")
)
title.pack(pady=10)

canvas = tk.Canvas(
    root,
    width=maze.shape[1]*CELL_SIZE,
    height=maze.shape[0]*CELL_SIZE
)
canvas.pack()

# -------------------------------
# Labels
# -------------------------------

score_label = tk.Label(root,text="Score: 0",font=("Arial",12))
score_label.pack()

level_label = tk.Label(root,text="Level: 1",font=("Arial",12))
level_label.pack()

feedback = tk.Label(root,text="",font=("Arial",12))
feedback.pack()

# -------------------------------
# Helper Functions
# -------------------------------

def is_valid(state):

    x,y = state

    if x < 0 or y < 0 or x >= maze.shape[0] or y >= maze.shape[1]:
        return False

    if maze[x][y] == 1:
        return False

    return True


def get_next_state(state,action):

    x,y = state

    if action == "up":
        return (x-1,y)

    if action == "down":
        return (x+1,y)

    if action == "left":
        return (x,y-1)

    if action == "right":
        return (x,y+1)


# -------------------------------
# Draw Maze
# -------------------------------

user_pos = list(start)

def draw_maze():

    canvas.delete("all")

    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):

            x1=j*CELL_SIZE
            y1=i*CELL_SIZE
            x2=x1+CELL_SIZE
            y2=y1+CELL_SIZE

            if maze[i][j] == 1:
                color="black"
            elif (i,j) in visited:
                color="yellow"
            else:
                color="white"

            canvas.create_rectangle(x1,y1,x2,y2,fill=color,outline="gray")

    # Start
    canvas.create_rectangle(
        start[1]*CELL_SIZE,
        start[0]*CELL_SIZE,
        start[1]*CELL_SIZE+CELL_SIZE,
        start[0]*CELL_SIZE+CELL_SIZE,
        fill="blue"
    )

    # Goal
    canvas.create_rectangle(
        goal[1]*CELL_SIZE,
        goal[0]*CELL_SIZE,
        goal[1]*CELL_SIZE+CELL_SIZE,
        goal[0]*CELL_SIZE+CELL_SIZE,
        fill="green"
    )

    # Agent
    canvas.create_oval(
        user_pos[1]*CELL_SIZE+10,
        user_pos[0]*CELL_SIZE+10,
        user_pos[1]*CELL_SIZE+CELL_SIZE-10,
        user_pos[0]*CELL_SIZE+CELL_SIZE-10,
        fill="red"
    )


# -------------------------------
# Agent Movement
# -------------------------------

def move_agent(action):

    global score

    next_state = get_next_state(tuple(user_pos),action)

    if not is_valid(next_state):

        score -= 5
        feedback.config(text="Unsafe Move (-5)")
        score_label.config(text=f"Score: {score}")
        return

    user_pos[0],user_pos[1] = next_state

    if next_state in visited:

        score -= 20
        feedback.config(text="Visited Again (-20)")

    else:

        score += 10
        visited.add(next_state)
        feedback.config(text="Safe Move (+10)")

    score_label.config(text=f"Score: {score}")

    if tuple(user_pos) == goal:

        feedback.config(text="Level Complete!")
        root.after(1500,next_level)

    draw_maze()


# -------------------------------
# Reset Level
# -------------------------------

def reset_level():

    global visited,user_pos

    visited=set()
    user_pos=list(start)

    draw_maze()


# -------------------------------
# Next Level
# -------------------------------

def next_level():

    global level_index,maze

    level_index += 1

    if level_index >= len(maze_dataset):

        feedback.config(text="All Levels Completed!")
        return

    maze = maze_dataset[level_index]

    level_label.config(text=f"Level: {level_index+1}")

    reset_level()


# -------------------------------
# Refresh Level
# -------------------------------

def refresh_level():

    global score

    score = 0

    score_label.config(text="Score: 0")

    feedback.config(text="Level Restarted")

    reset_level()


# -------------------------------
# Buttons
# -------------------------------

frame=tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame,text="Up",
command=lambda:move_agent("up")).grid(row=0,column=1)

tk.Button(frame,text="Left",
command=lambda:move_agent("left")).grid(row=1,column=0)

tk.Button(frame,text="Right",
command=lambda:move_agent("right")).grid(row=1,column=2)

tk.Button(frame,text="Down",
command=lambda:move_agent("down")).grid(row=2,column=1)

refresh_btn=tk.Button(root,
text="Refresh Level",
command=refresh_level)

refresh_btn.pack(pady=10)

# -------------------------------
# Start Game
# -------------------------------

draw_maze()

root.mainloop()