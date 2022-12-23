import math
import pygame
from sys import exit

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 80)
start_time = 0
game_active = False
game_lost = False
# Background surfaces:

# -- sky
sky_surface = pygame.image.load("graphics/Sky.png").convert()

# -- ground
ground_surface = pygame.image.load("graphics/ground.png").convert()
ground_rect = ground_surface.get_rect(topleft = (0, 300))

# -- intro
intro_surface = test_font.render(" Mucus Man ", False, (0, 0, 0))
intro_rect = intro_surface.get_rect(center = (400, 50))

def update_score():
    time = pygame.time.get_ticks() / 1000
    global test_font
    score_value = int(time) - start_time
    score_display = test_font.render("Score: " + str(score_value), False, (0, 0, 0))
    score_display_rect = score_display.get_rect(center = (400, 50))
    screen.blit(score_display, score_display_rect)


# -- game_over
game_over_surface = test_font.render(" GAME OVER ", False, (0, 0, 0))
game_over_rect = game_over_surface.get_rect(center = (400, 50))

# -- game over continue
continue_surface = test_font.render("Press SPACE to Restart", False, (0, 0, 0))
continue_rect = continue_surface.get_rect(center = (400, 350))

# -- new game start
start_surface = test_font.render("Press SPACE to start", False, (0, 0, 0))
start_rect = start_surface.get_rect(center = (400, 350))

# -- snail/ enemy
snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(bottomright = (600, 300))

# -- player
player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0

# -- intro Screen
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2.5)
player_stand_rect = player_stand.get_rect(center = (400, 200))



# enter game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_gravity == 0:
                        player_gravity -= 25
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # place BG Images
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, ground_rect)

        # update the score
        update_score()

        # move/respawn the enemy
        snail_rect.x -= 4
        if snail_rect.right <= 0: snail_rect.left = 800
        screen.blit(snail_surface, snail_rect)

        # player
        player_gravity += 1
        player_rect.y += player_gravity

        # detect collisions with the ground surface
        if player_rect.colliderect(ground_rect):
            player_rect.bottom = ground_rect.top
            player_gravity = 0

        # update player
        screen.blit(player_surface, player_rect)

        # detect player and enemy collisions
        if player_rect.colliderect(snail_rect):
            game_active = False
            game_lost = True

    # display the intro/gameover screen
    if not game_active:
        screen.fill((94, 129, 162))

        if game_lost:
            screen.blit(game_over_surface, game_over_rect)
            screen.blit(player_stand, player_stand_rect)
            screen.blit(continue_surface, continue_rect)
        else:
            screen.blit(intro_surface, intro_rect)
            screen.blit(player_stand, player_stand_rect)
            screen.blit(start_surface, start_rect)

    pygame.display.update()
    # setting framerate floor to 60 cycle/sec
    clock.tick(60)


# display surfaces is the background images
# regular surfaces are separate stack-able surfaces
# use the convert method on images to help pygame handle them better and your game run faster.
# use rectangles to calculate collisions

