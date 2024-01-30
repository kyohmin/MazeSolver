import pygame

def gui():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1243,750))
    pygame.display.set_caption("Maze Solving Visualizer")

    clock = pygame.time.Clock()

    DEFAULT_IMAGE_SIZE = (180, 180)
    parallelBackground = pygame.Surface((622,750))
    parallelBackground.fill((66, 66, 66))

    # Font
    pygame.font.init()
    font = pygame.font.Font(pygame.font.get_default_font(),40)
    timeFont = pygame.font.Font(pygame.font.get_default_font(),30)
    sequenceTitle = font.render("SEQUENCE", True,(0,0,0))
    parallelTitle = font.render("PARALLEL", True,(255,255,255))

    sequenceMaze,parallelMaze = [],[]
    for i in range(9):
            sequenceMaze.append(pygame.transform.scale(pygame.image.load("./Resources/Unsolved_Maze/Image_Maze/Maze_{num}.png".format(num=i+1)),DEFAULT_IMAGE_SIZE))
    for i in range(9):
            parallelMaze.append(pygame.transform.scale(pygame.image.load("./Resources/Unsolved_Maze/Image_Maze/Maze_{num}.png".format(num=i+1)),DEFAULT_IMAGE_SIZE))

    while True:
        screen.fill("White")
        screen.blit(parallelBackground,(622,0))
        # Default display
        screen.blit(sequenceTitle,(200,20))
        screen.blit(parallelTitle,(830,20))

        # Sequence Timer Text
        sequenceTime = open("./Resources/sequenceTime.txt", "r")
        sequenceRecord = sequenceTime.readline()
        sequenceTime.close()
        if sequenceRecord != "0.000 sec":
            sequenceTimeText = timeFont.render(sequenceRecord, True,(0,0,0))
        else:
            sequenceTimeText = "Recording"
        screen.blit(sequenceTimeText, (250,680))

        # Parallel Timer Text
        parallelTime = open("./Resources/parallelTime.txt", "r")
        parallelRecord = parallelTime.readline()
        parallelTime.close()
        if parallelRecord != "0.000 sec":
            parallelTimeText = timeFont.render(parallelRecord, True,(0,0,0))
        else:
            parallelTimeText = "Recording"
        screen.blit(parallelTimeText, (880,680))
        
        

        for i in range(9):
            try:
                sequenceMaze[i] = pygame.transform.scale(pygame.image.load("./Resources/Solved_Maze/Sequence_Maze_Result/Maze_{num}.png".format(num=i+1)),DEFAULT_IMAGE_SIZE)
            except:
                pass

        for i in range(9):
            try:
                parallelMaze[i] = pygame.transform.scale(pygame.image.load("./Resources/Solved_Maze/Parallel_Maze_Result/Maze_{num}.png".format(num=i+1)),DEFAULT_IMAGE_SIZE)
            except:
                pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        for i in range(9):
            screen.blit(sequenceMaze[i],(35+int(i%3)*190,80+int(i/3)*190))

        for i in range(9):
            screen.blit(parallelMaze[i],(655+int(i%3)*190,80+int(i/3)*190))

        
            
        pygame.display.update()
        clock.tick(60)

gui()