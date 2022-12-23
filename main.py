import pygame
from sys import exit

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 80)

# Background surfaces
sky_surface = pygame.image.load("graphics/Sky.png").convert()

ground_surface = pygame.image.load("graphics/ground.png").convert()
ground_rect = ground_surface.get_rect(topleft = (0, 300))

score_surface = test_font.render(" Mucus Man ", False, (64, 64, 64))
score_rect = score_surface.get_rect(center = (400, 50))

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(bottomright = (600, 300))

player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0

# enter game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("space pressed")
                if player_gravity == 0:
                    player_gravity -= 20
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                print("space released")

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, ground_rect)
    # pygame.draw.rect(screen, "Teal", score_rect, 10)
    # pygame.draw.rect(screen, "Teal", score_rect)
    screen.blit(score_surface, score_rect)

    snail_rect.x -= 4
    if snail_rect.right <= 0: snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)

    # player
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.colliderect(snail_rect):
        # print("collision")
        ...
    if player_rect.colliderect(ground_rect):
        player_rect.bottom = ground_rect.top
        player_gravity = 0

    screen.blit(player_surface, player_rect)

    pygame.display.update()
    # setting framerate floor to 60 cycle/sec
    clock.tick(60)


# display surfaces is the background images
# regular surfaces are separate stack-able surfaces
# use the convert method on images to help pygame handle them better and your game run faster.
