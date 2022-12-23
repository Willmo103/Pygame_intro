import pygame, time, random, os
pygame.font.init()

pygame.init()
WIDTH, HEIGHT = (750, 750)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Background
BG = pygame.image.load("assets/assets/background-black.png").convert()
BG = pygame.transform.scale(BG, (750, 750))

# Ships
GREEN_SHIP = pygame.image.load("assets/assets/pixel_ship_green_small.png").convert_alpha()
BLUE_SHIP = pygame.image.load("assets/assets/pixel_ship_blue_small.png").convert_alpha()
RED_SHIP = pygame.image.load("assets/assets/pixel_ship_red_small.png").convert_alpha()

# player ship
PLAYER_SHIP = pygame.image.load("assets/assets/pixel_ship_yellow.png").convert_alpha()

# lasers
RED_LASER = pygame.image.load("assets/assets/pixel_laser_red.png").convert_alpha()
BLUE_LASER= pygame.image.load("assets/assets/pixel_laser_blue.png").convert_alpha()
GREEN_LASER = pygame.image.load("assets/assets/pixel_laser_green.png").convert_alpha()
YELLOW_LASER = pygame.image.load("assets/assets/pixel_laser_yellow.png").convert_alpha()

class Laser:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not self.y <= height and self.y >= 0

    def collision(self, obj):
        return collide(obj, self)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.laser_image = None
        self.lasers = []
        self.cooldown_counter = 0

    def draw(self, window):
        window.blit(self.ship_image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)



    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_height()

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x - (self.get_width()/2), self.y, self.laser_image)
            self.lasers.append(laser)
            self.cooldown_counter = 1


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SHIP, RED_LASER),
        "blue": (BLUE_SHIP, BLUE_LASER),
        "green": (GREEN_SHIP, GREEN_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_image, self.laser_image = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_image)

    def move(self, vel):
        self.y += vel

class Player(Ship):
    COOLDOWN = 15
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_image = PLAYER_SHIP
        self.laser_image = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None



player = Player(300, 650)

def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    player_vel = 8
    main_font = pygame.font.SysFont("comicsans", 50)
    enemies = []
    wave_length = 5
    enemy_vel = 1
    enemy_laser_vel = 4
    player_laser_vel = -5

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0,0))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemies.append(Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"])))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()


        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_lasers(enemy_laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

        player.move_lasers(player_laser_vel, enemies)

        redraw_window()
main()

