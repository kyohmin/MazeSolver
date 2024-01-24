import matplotlib.pyplot as plt
from random import shuffle
from queue import Queue
import multiprocessing

class Room:
    def __init__(self):
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        shuffle(self.directions)


def create_maze(dimmension):
    # Create a grid filled with walls
    mazeMap = [[1 for row in range(dimmension*2+1)] for col in range(dimmension*2+1)]
    x,y = 0,0
    mazeMap[x+1][y+1] = 0
    record = [(x,y)]


    while True:
        if len(record) == 0: break

        x,y = record[-1]

        currentRoom = Room()
        
        for tmpY, tmpX in currentRoom.directions:
            newY = tmpY + y
            newX = tmpX + x

            if newX >= 0 and newY >= 0 and newX < dimmension and newY < dimmension and mazeMap[2*newY+1][2*newX+1] == 1:
                mazeMap[2*newY+1][2*newX+1] = 0
                mazeMap[2*y+1+tmpY][2*x+1+tmpX] = 0
                record.append((newX, newY))
                break
        else:
            record.pop()

    return mazeMap


mazeMap = create_maze(10)
for i in mazeMap:
    print(i)
