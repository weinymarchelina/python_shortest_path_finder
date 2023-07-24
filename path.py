import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "#", "#", "#", "O", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", "#", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "X", "#", "#", "#", "#", "#", "#", "#"]
]

"""
for i, row in enumerate(maze):  
        for j, value in enumerate(row):
            print(j, value)
"""

def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):  
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", RED)
            else:
                stdscr.addstr(i, j*2, value, BLUE) 

def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
            
    return None

# def find_end():

def find_neighbors(maze, row, col):
    neighbors = []

    # check each direction one by one while the neighbor's node is still in range (prevent accessing out of range element)
    if row > 0:  # look up
        neighbors.append((row - 1, col))

    if row + 1 < len(maze):  # look down
        neighbors.append((row + 1, col))

    if col > 0:  # look left
        neighbors.append((row, col - 1))

    if col + 1 < len(maze[0]):  # look right
        neighbors.append((row, col + 1))

    return neighbors

def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    q = queue.Queue() # the first element inserted is the first element that come out
    q.put((start_pos, [start_pos])) # the first parameter is the position that we are currently on, while the second parameter is a list that is used to store the path

    visited = set() # the node that we have visited

    while not q.empty():
        current_pos, path = q.get() # the get function returns the element in front of the queue, in this case it will return the first element (started with start_pos) and also return the path
        row, col = current_pos # break it to row and col (since it returns 2 value, which is its row and col index a.k.a i and j from the function find_start)

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.3)
        stdscr.refresh()

        if maze[row][col] == end:
            return path
        
        # do these if have not found the end node
        neighbors = find_neighbors(maze, row, col)

        for neighbor in neighbors:
            if neighbor in visited:
                continue

            neighbor_row, neighbor_col = neighbor
            if maze[neighbor_row][neighbor_col] == "#": # skips wall element
                continue

            new_path = path + [neighbor] # the new_path is bascially adding the old path with the valid blank neighbor
            q.put((neighbor, new_path))
            visited.add(neighbor) # add neighbor to the visited list so that we won't process it multiple times


def main(stdscr): # standard output screen
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getch()

"""
def main(stdscr): # standard output screen
    # curses module: brings you to a new window, then returns you back to the main terminal once you click something

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) # id 1 pair means we can use blue (text) and black (background)
    blue_and_black = curses.color_pair(1) # set the pair into the variable

    stdscr.clear()
    stdscr.addstr(5, 0, "hello world!", blue_and_black) # row and col, then the string; addstr = prints
    stdscr.refresh()
    stdscr.getch()
"""

wrapper(main)