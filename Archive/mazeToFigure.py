import numpy as np
import random
from queue import Queue
import multiprocessing
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def create_maze(dim):
    # Create a grid filled with walls
    maze = np.ones((dim*2+1, dim*2+1))

    # Define the starting point
    x, y = (0, 0)
    maze[2*x+1, 2*y+1] = 0

    # Initialize the stack with the starting point
    stack = [(x, y)]
    while len(stack) > 0:
        x, y = stack[-1]

        # Define possible directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < dim and ny < dim and maze[2*nx+1, 2*ny+1] == 1:
                maze[2*nx+1, 2*ny+1] = 0
                maze[2*x+1+dx, 2*y+1+dy] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()
            
    # Create an entrance and an exit
    maze[1, 0] = 0
    maze[-2, -1] = 0

    return maze

def find_path(maze):
    # BFS algorithm to find the shortest path
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    start = (1, 1)
    end = (maze.shape[0]-2, maze.shape[1]-2)
    visited = np.zeros_like(maze, dtype=bool)
    visited[start] = True
    queue = Queue()
    queue.put((start, []))
    while not queue.empty():
        (node, path) = queue.get()
        for dx, dy in directions:
            next_node = (node[0]+dx, node[1]+dy)
            if (next_node == end):
                return path + [next_node]
            if (next_node[0] >= 0 and next_node[1] >= 0 and 
                next_node[0] < maze.shape[0] and next_node[1] < maze.shape[1] and 
                maze[next_node] == 0 and not visited[next_node]):
                visited[next_node] = True
                queue.put((next_node, path + [next_node]))
    
def draw_maze(maze, num, fig, ax, path=None):
    if num == 0: x,y = (0,0)
    elif num == 1: x,y = (0,1)
    elif num == 2: x,y = (0,2)
    elif num == 3: x,y = (1,0)
    elif num == 4: x,y = (1,1)
    elif num == 5: x,y = (1,2)
    elif num == 6: x,y = (2,0)
    elif num == 7: x,y = (2,1)
    elif num == 8: x,y = (2,2)
    
    # Set the border color to white
    fig.patch.set_edgecolor('white')
    fig.patch.set_linewidth(0)

    ax[x,y].imshow(maze, cmap=plt.cm.binary, interpolation='nearest')
    
    ax[x,y].set_xticks([])
    ax[x,y].set_yticks([])

    if path is not None:
        line, = ax[x,y].plot([], [], color='red', linewidth=4)
        
        def init():
            line.set_data([], [])
            return line,
        
        # update is called for each path point in the maze
        def update(frame):
            if frame == len(path)-1:
                print(f'{frame} == {len(path)-1}; closing!')
            x, y = path[frame]
            line.set_data(*zip(*[(p[1], p[0]) for p in path[:frame+1]]))  # update the data
            return line,
        
        ani = animation.FuncAnimation(fig, update, frames=range(len(path)), init_func=init, blit=True, repeat = False, interval=20)

    return ani

# def solve(dim, i, fig, ax):
    
#     maze = create_maze(dim)
#     path = find_path(maze)
#     draw_maze(maze, i, fig, ax, path)
#     print("maze solved:", i)




# if __name__ == "__main__":
#     done = 0
#     mazeList = []
#     fig, ax = plt.subplots(3,3,figsize=(10,10))
#     processes = [multiprocessing.Process(target=solve, args=(50,i,fig,ax,)) for i in range(10)]
#     for p in processes:
#         p.start()
#     for p in processes:
#         p.join()
    
#     plt.show()
    
if __name__ == "__main__":
    # maze = create_maze(50)
    # path = find_path(maze)
    # draw_maze(maze, path)
    # print("maze solved:", i)
    fig, ax = plt.subplots(3,3,figsize=(10,10))
    fig.tight_layout()

    mazeList = [0,1,2,3,4,5,6,7,8]
    for i in range(9):
        maze = create_maze(20)
        path = find_path(maze)
        if i == 0: print("path:", path)
        mazeList[i] = draw_maze(maze, i,fig,ax,path)
        print("maze solved:", i)

    plt.show()
    plt.close()


