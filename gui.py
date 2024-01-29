import pygame

pygame.init()
screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption("Sequence")
clock = pygame.time.Clock()
DEFAULT_IMAGE_SIZE = (75, 75)

images = []
for i in range(5):
        images.append(pygame.transform.scale(pygame.image.load("originalMaze/Maze_{num}.png".format(num=i+1)),DEFAULT_IMAGE_SIZE))

screen.fill("White")

while True:
    for i in range(5):
        try:
            images[i] = pygame.transform.scale(pygame.image.load("Solution/Solution_{num}.png".format(num=i+1)),DEFAULT_IMAGE_SIZE)
        except:
            pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    for i in range(5):
        screen.blit(images[i],(0+i*100,0))
        
    pygame.display.update()
    clock.tick(60)


