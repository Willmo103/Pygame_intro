import pygame
from sys import exit
from random import randint

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 80)
start_time = 0
game_active = False
game_lost = False

def update_score():
    time = pygame.time.get_ticks() / 1000
    global test_font
    score_value = int(time) - start_time
    score_display = test_font.render("Score: " + str(score_value), False, (0, 0, 0))
    score_display_rect = score_display.get_rect(center = (400, 50))
    screen.blit(score_display, score_display_rect)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for rect in obstacle_list:
            rect.x -= 5
            if rect.bottom == 300:
                screen.blit(snail_surface, rect)
            else:
                screen.blit(fly_surface, rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > 0]
        return obstacle_list
    else: return []

def player_animation():
    global player_surface, player_index
    if player_rect.bottom != ground_rect.top:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

# Background surfaces:

# -- sky
sky_surface = pygame.image.load("graphics/Sky.png").convert()

# -- ground
ground_surface = pygame.image.load("graphics/ground.png").convert()
ground_rect = ground_surface.get_rect(topleft = (0, 300))

# -- intro
intro_surface = test_font.render(" Mucus Man ", False, (0, 0, 0))
intro_rect = intro_surface.get_rect(center = (400, 50))



# -- game_over
game_over_surface = test_font.render(" GAME OVER ", False, (0, 0, 0))
game_over_rect = game_over_surface.get_rect(center = (400, 50))

# -- game over continue
continue_surface = test_font.render("Press SPACE to Restart", False, (0, 0, 0))
continue_rect = continue_surface.get_rect(center = (400, 350))

# -- new game start
start_surface = test_font.render("Press SPACE to start", False, (0, 0, 0))
start_rect = start_surface.get_rect(center = (400, 350))

# -- snail
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames_list = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames_list[snail_frame_index]

# -- fly
fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_frames_list = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames_list[fly_frame_index]


obstacle_rect_list = []

# -- player
player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_jump = pygame.image.load("graphics/Player/jump.png")
player_index = 0
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0


# -- intro Screen
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2.5)
player_stand_rect = player_stand.get_rect(center = (400, 200))

# Obstacle Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Snail Animation timer
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 300)

# Fly Animation timer
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 100)

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
                        player_gravity -= 20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                obstacle_rect_list = []
                start_time = int(pygame.time.get_ticks() / 1000)
                player_gravity = 0
                player_rect.midbottom = (80, 300)

        if game_active:
            if event.type == obstacle_timer :
                rand = randint(1, 100)
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900, 1100), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames_list[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames_list[fly_frame_index]



    if game_active:
        # place BG Images
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, ground_rect)

        # update the score
        update_score()

        # player
        player_gravity += 1
        player_rect.y += player_gravity

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # detect collisions with the ground surface
        if player_rect.colliderect(ground_rect):
            player_rect.bottom = ground_rect.top
            player_gravity = 0

        # update player
        player_animation()
        screen.blit(player_surface, player_rect)

        # detect player and enemy collisions
        if obstacle_rect_list:
            for obstacle in obstacle_rect_list:
                if player_rect.colliderect(obstacle):
                    game_active = False
                    game_lost = True
                    break

    # display the intro/gameover screen
    if not game_active:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        if game_lost:
            screen.blit(game_over_surface, game_over_rect)
            screen.blit(continue_surface, continue_rect)
        else:
            screen.blit(intro_surface, intro_rect)
            screen.blit(start_surface, start_rect)

    pygame.display.update()
    # setting framerate floor to 60 cycle/sec
    clock.tick(60)


# display surfaces is the background images
# regular surfaces are separate stack-able surfaces
# use the convert method on images to help pygame handle them better and your game run faster.
# use rectangles to calculate collisions
# usr timer to randomize spawning enemies

