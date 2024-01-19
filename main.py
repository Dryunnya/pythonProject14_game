import os
import random
import sys
import pygame
import math
import random

# моргание происходит из-за отрисовки поля. поменять координаты местами у главного спрайта и остального поля


pygame.init()
size = WIDTH, HEIGHT = 1550, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

player_walk_image = [pygame.image.load("project/walk1.png"), pygame.image.load("project/walk2.png"), pygame.image.load(
    "project/walk3.png"),
                     pygame.image.load("project/walk4.png"), pygame.image.load("project/walk5.png"), pygame.image.load(
        "project/walk6.png"),
                     pygame.image.load("project/walk7.png"), pygame.image.load("project/walk8.png"),
                     pygame.image.load("project/walk9.png"), pygame.image.load("project/walk10.png")]

yeti_animation = [pygame.image.load("project/yeti (1).png"), pygame.image.load("project/yeti (2).png"),
                  pygame.image.load("project/yeti (3).png"), pygame.image.load("project/yeti (4).png"),
                  pygame.image.load("project/yeti (5).png"), pygame.image.load("project/yeti (6).png"),
                  pygame.image.load("project/yeti (7).png"), pygame.image.load("project/yeti (8).png"),
                  pygame.image.load("project/yeti (9).png"), pygame.image.load("project/yeti (10).png"),
                  pygame.image.load("project/yeti (11).png"), pygame.image.load("project/yeti (12).png"),
                  pygame.image.load("project/yeti (13).png"), pygame.image.load("project/yeti (14).png"),
                  pygame.image.load("project/yeti (15).png"), pygame.image.load("project/yeti (16).png"),
                  pygame.image.load("project/yeti (17).png"), pygame.image.load("project/yeti (18).png"),
                  pygame.image.load("project/yeti (19).png"), pygame.image.load("project/yeti (20).png"),
                  pygame.image.load("project/yeti (21).png"), pygame.image.load("project/yeti (22).png"),
                  pygame.image.load("project/yeti (23).png"), pygame.image.load("project/yeti (24).png"),
                  pygame.image.load("project/yeti (25).png"), pygame.image.load("project/yeti (26).png"),
                  pygame.image.load("project/yeti (27).png"), pygame.image.load("project/yeti (28).png"),
                  pygame.image.load("project/yeti (29).png"), pygame.image.load("project/yeti (30).png"),
                  pygame.image.load("project/yeti (31).png"), pygame.image.load("project/yeti (32).png"),
                  pygame.image.load("project/yeti (33).png"), pygame.image.load("project/yeti (34).png"),
                  pygame.image.load("project/yeti (35).png"), pygame.image.load("project/yeti (36).png"),
                  pygame.image.load("project/yeti (37).png"), pygame.image.load("project/yeti (38).png"),
                  pygame.image.load("project/yeti (39).png"), pygame.image.load("project/yeti (40).png"),
                  pygame.image.load("project/yeti (41).png"), pygame.image.load("project/yeti (42).png"),
                  pygame.image.load("project/yeti (43).png"), pygame.image.load("project/yeti (44).png"),
                  pygame.image.load("project/yeti (45).png"), pygame.image.load("project/yeti (46).png"),
                  pygame.image.load("project/yeti (47).png"), pygame.image.load("project/yeti (48).png")]

weapon = pygame.image.load('project/weapon.png').convert_alpha()
# weapon.set_colorkey((255, 255, 255))
weapon = pygame.transform.scale(weapon, (30, 20))

# WIN_WIDTH = 1200  # Ширина создаваемого окна
# WIN_HEIGHT = 750  # Высота
# DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную

BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = 30
PLATFORM_HEIGHT = 60
PLATFORM_COLOR = "#FF6262"



class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def weapon_player(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        weapon_pos_x, weapon_pos_y = mouse_x - player.x, mouse_y - player.y
        angle = -math.atan2(weapon_pos_y, weapon_pos_x) * (180 / math.pi)

        copy_player_weapon = pygame.transform.rotate(weapon, angle)
        screen.blit(copy_player_weapon,
                    (self.x + 45 - int(weapon.get_width() / 2),
                     self.y + 45 - int(weapon.get_height() / 2)))

    def main(self, screen):
        if self.animation_count + 1 == 10:
            self.animation_count = 0
        else:
            self.animation_count += 1
        if (self.moving_right or self.moving_up) and not self.moving_left:
            screen.blit(pygame.transform.scale(player_walk_image[self.animation_count], (70, 70)),
                        (self.x, self.y))
        elif self.moving_left or self.moving_down:
            screen.blit(
                pygame.transform.scale(
                    pygame.transform.flip(player_walk_image[self.animation_count], True, False),
                    (70, 70)), (self.x, self.y))
        else:
            screen.blit(pygame.transform.scale(player_walk_image[0], (70, 70)),
                        (self.x, self.y))

        self.weapon_player(screen)

        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False


class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 10
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def main(self, screen):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        pygame.draw.circle(screen, 'red', (self.x, self.y), 5)


class YetiEnimy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-300, 300)
        self.offset_y = random.randrange(-300, 300)

    def main(self, screen):
        if self.animation_count + 0.1 >= 47:
            self.animation_count = 0
        else:
            self.animation_count += 0.1

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-300, 300)
            self.offset_y = random.randrange(-300, 300)
            self.reset_offset = random.randrange(80, 150)
        else:
            self.reset_offset -= 1

        if player.x + self.offset_x > self.x - display_scroll[0]:
            self.x += 1
        else:
            self.x -= 1

        if player.y + self.offset_y > self.y - display_scroll[1]:
            self.y += 1
        else:
            self.y -= 1

        screen.blit(pygame.transform.scale(yeti_animation[int(self.animation_count)], (50, 50)),
                    (self.x - display_scroll[0], self.y - display_scroll[1]))
        # print(display_scroll[0], display_scroll[1])
        print(pygame.time.get_ticks())


enimies = [YetiEnimy(400, 400)]

display_scroll = [0, 0]

player_bulets = []

player = Player(775, 150, 40, 40)
while True:

    screen.fill((100, 255, 200))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.QUIT

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player_bulets.append(PlayerBullet(player.x + 50, player.y + 50, mouse_x, mouse_y))
    bg = pygame.Surface((1500, 850))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(pygame.Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом
    level = ['------------------------------------------------------------------------------------------------',
             '-----#########################------------------------------------------------------------------',
             '-----#.....................@.#------------------------------------------------------------------',
             '-----#.......................#------------------------------------------------------------------',
             '-----#.......#################------------------------------------------------------------------',
             '-----#.......#----------------------------------------------------------------------------------',
             '-----#.......#----------------######################################----------------------------',
             '-----#.......########---------#..................*.................#----------------------------',
             '-----#..............#---------#.....##.............................#----------------------------',
             '-----#..............#---------#....................................#----------------------------',
             '-----######.........#---------#............############............#----------------------------',
             '----------#.........#---------#............#----------#.......*....#----------------------------',
             '----------#.........#---------#...*........#----------#............#----------------------------',
             '----------#.........#---------#............#----------#............###########################--',
             '----------#.........#---------#.......##...#----------#......................................#--',
             '----------#.........###########.........####----------#........##...........................##--',
             '----------#...................*.........#----------####..............**.........................',
             '----------#............#................#----------#........................................##--',
             '----------#.......*.................*...#----------#.....*...................................#--',
             '----------########...#......#############----------###########################################--',
             '-----------------#..........#-------------------------------------------------------------------',
             '-----------------#..........#-------------------------------------------------------------------',
             '-----------------#..........#-------------------------------------------------------------------',
             '-----------------#..........#-------------------------------------------------------------------',
             '-----------------#..........#-------------------------------------------------------------------',
             '-----------------#..........#-------------------------------------------------------------------',
             '-----------------#..........#-------------------------------------------------------------------',
             '-----------------#....*..*..#-------------------------------------------------------------------',
             '-----------------#..........#-------------------------------------------------------------------',
             '-----------------############-------------------------------------------------------------------',
             '------------------------------------------------------------------------------------------------',
             '------------------------------------------------------------------------------------------------']
    screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                # создаем блок, заливаем его цветом и рисеум его
                pf = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                pf.fill(pygame.Color(PLATFORM_COLOR))
                screen.blit(pf, (x - display_scroll[0], y - display_scroll[1]))
            if col == '#':
                pf = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                pf.fill(pygame.Color('yellow'))
                screen.blit(pf, (x - display_scroll[0], y - display_scroll[1]))
            if col == '.':
                pf = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                pf.fill(pygame.Color('white'))
                screen.blit(pf, (x - display_scroll[0], y - display_scroll[1]))
            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке
        # clock.tick(100)

    keys = pygame.key.get_pressed()

    pygame.draw.rect(screen, 'brown', (100 - display_scroll[0], 100 - display_scroll[1], 20, 20))

    if keys[pygame.K_w]:
        display_scroll[1] -= 5

        player.moving_up = True

        for bullet in player_bulets:
            bullet.y += 5

    if keys[pygame.K_s]:
        display_scroll[1] += 5

        player.moving_down = True

        for bullet in player_bulets:
            bullet.y -= 5

    if keys[pygame.K_a]:
        display_scroll[0] -= 5
        player.moving_left = True
        for bullet in player_bulets:
            bullet.x += 5

    if keys[pygame.K_d]:
        display_scroll[0] += 5
        player.moving_right = True

        for bullet in player_bulets:
            bullet.x -= 5

    player.main(screen)
    for bullet in player_bulets:
        bullet.main(screen)

    for model in enimies:
        model.main(screen)

    clock.tick(120)
    pygame.display.flip()
    # pygame.display.update()
