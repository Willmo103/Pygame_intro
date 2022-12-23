import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png")
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.4)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()

    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index > len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
            self.frame_rate = .2

        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
            self.frame_rate = .1

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += self.frame_rate
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()


def collision_sprite():
    collisions = pygame.sprite.spritecollide(player.sprite, obstacle_group, False)
    if collisions:
        obstacle_group.empty()
        return True
    return False

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

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
music_track = pygame.mixer.Sound("audio/music.wav")
pygame.display.set_caption("Mucus Man 3000")
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
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


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
music = False

# enter game loop
while True:
    if not music and game_active:
        music_track.play(loops = -1)
        music = True
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
                    obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))
                # if randint(0, 2):
                    # obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900, 1100), 300)))
                # else:
                #     obstacle_group.add(Obstacle('snail'))
                #     obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900, 1100), 210)))

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
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # detect player and enemy collisions

        if collision_sprite():
            game_active = False
            game_lost = True

    # display the intro/gameover screen
    if not game_active:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        music_track.stop()
        music = False

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
# sprite class makes everything easier

