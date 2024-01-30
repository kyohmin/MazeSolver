import pygame

pygame.init()
screen = pygame.display.set_mode((1020,640))
pygame.display.set_caption("Sequence")
clock = pygame.time.Clock()
DEFAULT_IMAGE_SIZE = (54, 54)
textBackground = pygame.Surface((400,640))
textBackground.fill((66, 66, 66))

images = []
for i in range(100):
        images.append(pygame.transform.scale(pygame.image.load("originalMaze/Maze_{num}.png".format(num=i+1)),DEFAULT_IMAGE_SIZE))

screen.fill("White")
while True:
    # Deafault display
    screen.blit(textBackground,(640,0))

    for i in range(100):
        try:
            images[i] = pygame.transform.scale(pygame.image.load("Solution/Solution_{num}.png".format(num=i+1)),DEFAULT_IMAGE_SIZE)
        except:
            # images[i] = pygame.transform.scale(pygame.image.load("originalMaze/Maze_{num}.png".format(num=i+1)),DEFAULT_IMAGE_SIZE)
            pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    for i in range(100):
        screen.blit(images[i],(10+int(i%10)*57,10+int(i/10)*57))

    
        
    pygame.display.update()
    clock.tick(60)