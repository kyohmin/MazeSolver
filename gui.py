import pygame

pygame.init()
screen = pygame.display.set_mode((620,620))
pygame.display.set_caption("Sequence")
clock = pygame.time.Clock()
DEFAULT_IMAGE_SIZE = (200, 200)
textBackground = pygame.Surface(0,0)
screen.fill((66, 66, 66))
textBackground.fill("")

images = []
for i in range(9):
        images.append(pygame.transform.scale(pygame.image.load("originalMaze/Maze_{num}.png".format(num=i+1)),DEFAULT_IMAGE_SIZE))

screen.fill("White")
while True:
    for i in range(9):
        try:
            images[i] = pygame.transform.scale(pygame.image.load("Solution/Solution_{num}.png".format(num=i+1)),DEFAULT_IMAGE_SIZE)
        except:
            # images[i] = pygame.transform.scale(pygame.image.load("originalMaze/Maze_{num}.png".format(num=i+1)),DEFAULT_IMAGE_SIZE)
             pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    for i in range(9):
        screen.blit(images[i],(0+int(i%3)*210,0+int(i/3)*210))
        
    pygame.display.update()
    clock.tick(60)