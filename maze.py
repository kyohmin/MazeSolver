import random
from create_maze import Room

def make(prev, room, maze, size):
    room.prev = prev
    if room.prev is None:
        mazeMap[0][1] = "S"
    else:
        r = prev.r - room.r
        c = prev.c - room.c
        mazeMap[(room.r+1) * 2-1 + r][(room.c + 1) * 2 -1 +c] = ' '

    room.visit = 1
    mazeMap[(room.r+1)*2-1][(room.c+1)*2-1] = " "
    print("\nCurrent: {0}, {1}".format(room.r,room.c))
    while True:
        if len(room.drct) == 0:
            break
        nr, nc = room.drct.pop()
        if nr >= 0 and nr < size and nc >= 0 and nc < size:
            if not maze[nr][nc].visit == 1:
                make(room,maze[nr][nc], maze, size)
            else:
                print("방문")
        else:
            print("qnfrk")

size = 40
maze = [[Room(r,c) for c in range(size)] for r in range(size)]
mazeMap = [['█' for c in range(size*2+1)] for r in range(size*2+1)]

make(None, maze[0][0], maze, size)

while True:
    r = random.randint(1, size*2)
    if mazeMap[r][-2] == "█":
        pass
    mazeMap[r][-1] = "E"
    break

file = open("maze.txt", "w")
for r in mazeMap:
    for c in r:
        file.write(c)
    file.write('\n')
file.close()