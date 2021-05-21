# Đào Văn Thắng - 18133050
# I use the code of my teacher : Trần Nhật Quang
# I just code when i understand it, and i learn the code of : https://allaravel.com/blog/ve-do-thi-anh-dong-trong-python-voi-thu-vien-animation-trong-matplotlib#vi-du
# https://www.programcreek.com/python/example/96643/matplotlib.animation.FuncAnimation
# https://www.ics.uci.edu/~welling/teaching/271fall09/InfSearch271f09.pdf


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from IPython.display import HTML


class Node():
    """A node class for A* search"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0  # PATH-COST to the node
        self.h = 0  # heuristic to the goal: straight-line distance hueristic
        self.f = 0  # evaluation function f(n) = g(n) + h(n)
        self.hS = 0
    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a solution from "start" to "end" state in "maze" map using A* search.
    See lecture slide for the A* algorithm."""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []  # frontier queue
    closed_list = []  # explored set

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0 :
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        if current_node.h<=current_node.hS:
            open_list.pop(current_index)
            closed_list.append(current_node)

        # Check if we found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Expansion: Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0 :
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child :
                    continue

            # Create the f, g, and h values
            child.g = current_node.g+1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.hS = ((start_node.position[0] - end_node.position[0]) ** 2) + ((start_node.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g :
                    continue
            def foo(): # I check the child , if it >= open_node , it can continue
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        return True
                return False

            if foo()==True:
                continue
            # Add the child to the open list
            open_list.append(child)


if __name__ == '__main__':

    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 1, 1, 0],  # 1: obstacle position
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]]


    start = (1, 0)
    goal = (8, 9)
    path = astar(maze, start, goal)
    print(path)
    map = np.array(maze)
    path = np.array(path)
    pathx= path[:,0]
    pathy= path[:,1]
    # pathy= np.reshape(pathy,(13,2))
    # pathx = np.reshape(pathx, (13, 2))
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 9), ylim=(10, -1))
    line, = ax.plot([], [], lw=10)
    ax.grid()
    # ax.bar()
    xdata, ydata = [], []

    ref = np.full([9, 9, 3], [255, 255, 255], dtype=np.uint8)
    for s in range(9):
        for j in range(9):
            if map[s, j] == 1:
                ref[s][j] = (239, 23, 18)
    plt.imshow(ref)

    def animate(i):
        a =start[0];
        b=start[1];
        y = pathx[i]
        x = pathy[i]
        xdata.append(x)
        ydata.append(y)
        line.set_data(xdata,ydata)
        return line,

    anim = FuncAnimation(fig, animate, frames=30, interval=300, blit = False)
    anim.save('mygif.gif',writer='imagemagick')
    plt.show()
    # em muốn dùng gif nhưng em ko hiểu sao em không thể lưu đưc gif trên pycharm , nhưng trên jupiter note book đc ạ
    # i convert it to the gif




