import matplotlib.pyplot as plt
from random import shuffle
# import multiprocessing

class Room:
    def __init__(self, row, col, dimmension):
        self.visit = False
        self.directions = [(row, col+2), (row+2, col), (row, col-2), (row-2, col)]
        tmp = [(row, col+2), (row+2, col), (row, col-2), (row-2, col)]

        for x,y in tmp:
            if x < 0 or y < 0 or x > dimmension*2 or y > dimmension*2: # Need to remove when it goes over the boundary
                self.directions.remove((x,y))

        shuffle(self.directions)

def create_maze(dimmension):
    # Create a grid filled with walls and rooms
    mazeMap = [[1 for _ in range(dimmension*2+1)] for _ in range(dimmension*2+1)]
    for row in range(1,2*dimmension+1, 2):
        for col in range(1,2*dimmension+1,2):
            mazeMap[row][col] = Room(col,row, dimmension)

    x,y = (0,0)
    mazeMap[x+1][y+1].visit = True

    record = [(1,1)]

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

def textify(mazeArr):
    for i, line in enumerate(mazeArr):
        for j, block in enumerate(line):
            if block != 1:
                mazeArr[i][j] = 0

    return mazeArr

def createImage(mazeArr,numbering): # Require editting
    fig, ax = plt.subplots(figsize=(10,10))
    fig.patch.set_linewidth(0)

    # Save as Image
    ax.imshow(mazeArr, cmap=plt.cm.binary, interpolation='nearest')
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    fileName = "Maze_{index}"
    plt.savefig("originalMaze/"+fileName.format(index = numbering) + ".png", bbox_inches = 'tight',pad_inches = 0)
    plt.close()

    # Save as Text
    with open("textMaze/"+fileName.format(index = numbering)+".txt", 'w') as f:
            for line in mazeMap:
                for block in line:
                    f.write(str(block))
                f.write("\n")

if __name__ == "__main__":
    for i in range(100):
        mazeMap = create_maze(24)
        mazeMap = textify(mazeMap)
        createImage(mazeMap,i+1)
        
    
    


    


