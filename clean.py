import os

sequenceTime = open("./Resources/sequenceTime.txt", "w")
sequenceTime.write("0.000 sec")
sequenceTime.close()

parallelTime = open("./Resources/parallelTime.txt", "w")
parallelTime.write("0.000 sec")
parallelTime.close()

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

parallelTime = open("./Resources/parallelTime.txt", "w")
parallelTime.write("0.000 sec")
parallelTime.close()

for i in range(100):
    if os.path.isfile("./Resources/Solved_Maze/Parallel_Maze_Result/Maze_{num}.png".format(num=i+1)):
        os.remove("./Resources/Solved_Maze/Parallel_Maze_Result/Maze_{num}.png".format(num=i+1))
    if os.path.isfile("./Resources/Solved_Maze/Sequence_Maze_Result/Maze_{num}.png".format(num=i+1)):
        os.remove("./Resources/Solved_Maze/Sequence_Maze_Result/Maze_{num}.png".format(num=i+1))