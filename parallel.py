import matplotlib.pyplot as plt
import matplotlib.animation as animation
from copy import deepcopy
import time, math
import multiprocessing
from multiprocessing import Semaphore
import os

# Read Maze
def readMaze(mazeIndex):
    # Read first line to find dimmension
    textMaze = open("textMaze/Maze_{index}.txt".format(index=mazeIndex), "r")
    tmpDimmension = textMaze.readline()
    mazeDimmension = len(tmpDimmension.strip())
    textMaze.close()

    # Read the whole maze and create 2D array
    textMaze = open("textMaze/Maze_{index}.txt".format(index=mazeIndex), "r")
    mazeArr = [[0 for i in range(mazeDimmension)] for j in range(mazeDimmension)]
    for i,line in enumerate(textMaze):
        mazeDimmension = int((len(line)-1)/2)
        for j,block in enumerate(line.strip()):
            mazeArr[i][j] = int(block)
    textMaze.close()

    return mazeArr, mazeDimmension

def solveMaze(mazeInfo):
    mazeArr, mazeDimmension = mazeInfo
    tmp = deepcopy(mazeArr)
    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    # For checking all directions
    def movable(coord, direction, mazeArr):
        x,y = coord
        dirX,dirY = direction
        if mazeArr[y+dirY][x+dirX] == 0: return True

        return False
    
    stack = []
    curX,curY = (1,1)
    while(True):
        mazeArr[curY][curX] = -1
        if curX == mazeDimmension*2-1 and curY == mazeDimmension*2-1:
            stack.append((curX,curY))
            break

        moved = False
        for direction in directions:
            if movable((curX,curY),direction,mazeArr):
                stack.append((curX,curY))
                curX += direction[0]
                curY += direction[1]
                moved = True
                break

        if not moved:
            mazeArr[curY][curX] = -2
            curX,curY = stack.pop()

    return tmp, stack

def showPath(mazeInfo, index):
    # update is called for each path point in the maze
    def update(frame):
        line.set_data(*zip(*[(p[0], p[1]) for p in mazePath[:frame+1]]))  # update the data
        plt.savefig("Solution/Solution_{num}.png".format(num=index+1))
        return line,

    mazeArr, mazePath = mazeInfo
    figure, axes = plt.subplots(figsize=(2,2))
    figure.patch.set_linewidth(0)
    axes.imshow(mazeArr, cmap=plt.cm.binary, interpolation='nearest')
    figure.subplots_adjust(left=0, bottom=0, right=1, top=1)
    
    axes.set_xticks([])
    axes.set_yticks([])

    line, = axes.plot([], [], color='red', linewidth=2)
    
    ani = animation.FuncAnimation(figure, update, frames=range(len(mazePath)), blit=True, repeat = False, interval=20)
    # plt.savefig("Solution/Solution_{num}.png".format(num=index+1))

    # plt.show()
    
    animation.FuncAnimation.save(ani, filename="GIF/Solved_{num}.gif".format(num=index+1))

def program(index, sema):
    sema.acquire()
    print("Starting Maze",index+1)
    showPath(solveMaze(readMaze(index+1)),index)
    print("Completed Maze",index+1)
    sema.release()    

# # Parallel
if __name__ == "__main__":
    choice = int(input("Enter the number: \n1. Seequential\n2. Parallel\n\nChoice: "))
    # Create a Process only for GUI

    # MultiProcesssing for logic
    if choice == 1:
        start = time.time()
        for i in range(15):
            print("Starting Maze",i+1)
            showPath(solveMaze(readMaze(i+1)),i)
            print("Completed Maze",i+1)

        math.factorial(100000)
        end = time.time()
        
        print(f"{end - start:.5f} sec")

    else:
        start = time.time()

        sema = Semaphore(100)
        processes = []
        counter = 0
        for i in range(9):
            p = multiprocessing.Process(target=program, args=(i, sema))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        math.factorial(100000)
        end = time.time()

        print(f"{end - start:.5f} sec")


