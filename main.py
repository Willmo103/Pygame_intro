import pygame
from sys import exit

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

test_surface = pygame.Surface((100, 200))
test_surface.fill('Blue')

# enter game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(test_surface, (350, 100))
    pygame.display.update()

    # setting framerate floor to 60 cycle/sec
    clock.tick(60)


# display surfaces is the background images
# regular surfaces are separate stack-able surfaces
