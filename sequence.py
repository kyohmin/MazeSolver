import matplotlib.pyplot as plt
import matplotlib.animation as animation
from copy import deepcopy
import time, math
from random import shuffle
import multiprocessing
from multiprocessing import Semaphore
import os

# MAZE ROOM Class
class Room:
    def __init__(self, row, col, dimmension):
        self.visit = False
        self.directions = [(row, col+2), (row+2, col), (row, col-2), (row-2, col)]
        tmp = [(row, col+2), (row+2, col), (row, col-2), (row-2, col)]

        for x,y in tmp:
            if x < 0 or y < 0 or x > dimmension*2 or y > dimmension*2: # Need to remove when it goes over the boundary
                self.directions.remove((x,y))

        shuffle(self.directions)

# Folder Generating function
def folderExist():
    pathList = []
    pathList.append("./Resources")
    pathList.append("./Resources/GIF_Maze")
    pathList.append("./Resources/Solved_Maze")
    pathList.append("./Resources/Solved_Maze/Sequence_Maze_Result")
    pathList.append("./Resources/Solved_Maze/Parallel_Maze_Result")
    pathList.append("./Resources/Unsolved_Maze")
    pathList.append("./Resources/Unsolved_Maze/Text_Maze")
    pathList.append("./Resources/Unsolved_Maze/Image_Maze")
    
    for path in pathList:
        if not os.path.exists(path):
            os.mkdir(path)

    sequenceTime = open("./Resources/sequenceTime.txt", "w")
    sequenceTime.write("0.000 sec")
    sequenceTime.close()

# Maze Generator
def createMaze(dimmension):
    # Create a grid filled with walls and rooms
    mazeMap = [[1 for _ in range(dimmension*2+1)] for _ in range(dimmension*2+1)]
    for row in range(1,2*dimmension+1, 2):
        for col in range(1,2*dimmension+1,2):
            mazeMap[row][col] = Room(col,row, dimmension)

    # Starting Point of Maze
    x,y = (0,0)
    mazeMap[x+1][y+1].visit = True
    record = [(1,1)]

    # Repeat until all rooms are visited
    while True:
        if len(record) == 0: break

        x,y = record[-1]

        currentRoom = mazeMap[y][x]
        
        for newX,newY in currentRoom.directions:
            dirX, dirY = int((newX - x)/2), int((newY - y)/2)

            if mazeMap[newY][newX].visit == False:
                mazeMap[newY][newX].visit = True # Set as visited
                wallX, wallY = x+dirX, y+dirY
                mazeMap[wallY][wallX] = 0 # Break wall
                record.append((newX, newY))
                mazeMap[newY][newX].directions.remove((x,y))
                break
        else:
            record.pop()

    return mazeMap

def textifyMaze(mazeArr):
    for i, line in enumerate(mazeArr):
        for j, block in enumerate(line):
            if block != 1:
                mazeArr[i][j] = 0

    return mazeArr

def saveMaze(mazeArr,numbering):
    fig, ax = plt.subplots(figsize=(10,10))
    fig.patch.set_linewidth(0)

    # Save as Image
    ax.imshow(mazeArr, cmap=plt.cm.binary, interpolation='nearest')
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    fileName = "Maze_{index}"
    plt.savefig("./Resources/Unsolved_Maze/Image_Maze/"+fileName.format(index = numbering) + ".png", bbox_inches = 'tight',pad_inches = 0)
    plt.close()

    # Save as Text
    with open("./Resources/Unsolved_Maze/Text_Maze/"+fileName.format(index = numbering)+".txt", 'w') as f:
            for line in mazeArr:
                for block in line:
                    f.write(str(block))
                f.write("\n")

# Maze Generating function
def mazeExist(mazes,dimmension):
    for i in range(100):
        if os.path.isfile("./Resources/Solved_Maze/Parallel_Maze_Result/Maze_{num}.png".format(num=i+1)):
            os.remove("./Resources/Solved_Maze/Parallel_Maze_Result/Maze_{num}.png".format(num=i+1))
        if os.path.isfile("./Resources/Solved_Maze/Sequence_Maze_Result/Maze_{num}.png".format(num=i+1)):
            os.remove("./Resources/Solved_Maze/Sequence_Maze_Result/Maze_{num}.png".format(num=i+1))

    tmpFile = "./Resources/Unsolved_Maze/Image_Maze/Maze_1.png"

    if not os.path.isfile(tmpFile):
        print("Maze not found\nCreating Maze...")
        for i in range(mazes):
            mazeMap = createMaze(dimmension)
            mazeMap = textifyMaze(mazeMap)
            saveMaze(mazeMap, i+1)
        print("Maze created in './Resources/Unsolved_Maze'")

# Read Maze for creating image
def readMaze(mazeIndex):
    # Read first line to find dimmension
    textMaze = open("./Resources/Unsolved_Maze/Text_Maze/Maze_{index}.txt".format(index=mazeIndex), "r")
    tmpDimmension = textMaze.readline()
    mazeDimmension = len(tmpDimmension.strip())
    textMaze.close()

    # Read the whole maze and create 2D array
    textMaze = open("./Resources/Unsolved_Maze/Text_Maze/Maze_{index}.txt".format(index=mazeIndex), "r")
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
        plt.savefig("./Resources/Solved_Maze/Sequence_Maze_Result/Maze_{num}.png".format(num=index+1))
        return line,

    mazeArr, mazePath = mazeInfo
    figure, axes = plt.subplots(figsize=(2,2))
    figure.patch.set_linewidth(0)
    axes.imshow(mazeArr, cmap=plt.cm.binary, interpolation='nearest')
    figure.subplots_adjust(left=0, bottom=0, right=1, top=1)
    
    axes.set_xticks([])
    axes.set_yticks([])

    line, = axes.plot([], [], color='red', linewidth=3.7)
    
    ani = animation.FuncAnimation(figure, update, frames=range(len(mazePath)), blit=True, repeat = False, interval=20)    
    animation.FuncAnimation.save(ani, filename="./Resources/GIF_Maze/Solved_{num}.gif".format(num=index+1))

def program(index, sema):
    sema.acquire()
    print("Starting Maze",index+1)
    showPath(solveMaze(readMaze(index+1)),index)
    print("Completed Maze",index+1)
    sema.release()    

# # Parallel
if __name__ == "__main__":
    # === Start =================================================
    # Check if folders exist and create if it does not
    folderExist()

    # Check if Maze exists and create if it does not
    mazeExist(100,15) # 100 mazes with 49*49 in size

    # Maze Solving Logic
    start = time.time()

    # Start Timer
    sequenceTime = open("./Resources/sequenceTime.txt", "w")
    sequenceTime.write("Recording")
    sequenceTime.close()

    for i in range(10):
        print("Starting Maze",i+1)
        showPath(solveMaze(readMaze(i+1)),i)
        print("Completed Maze",i+1)

    math.factorial(100000)
    end = time.time()
    
    # Record Time
    sequenceTime = open("./Resources/sequenceTime.txt", "w")
    sequenceTime.write(f"{end - start:.3f} sec")
    sequenceTime.close()

    print(f"{end - start:.3f} sec")
