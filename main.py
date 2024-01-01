import os
import random
import sys
import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
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


# class AnimatedSprite(pygame.sprite.Sprite):
#     def __init__(self, sheet, columns, rows, x, y):
#         super().__init__(all_sprites)
#         self.frames = []
#         self.cut_sheet(sheet, columns, rows)
#         self.cur_frame = 0
#         self.image = self.frames[self.cur_frame]
#         self.rect = self.rect.move(x, y)
#
#     def cut_sheet(self, sheet, columns, rows):
#         self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
#                                 sheet.get_height() // rows)
#         for j in range(rows):
#             for i in range(columns):
#                 frame_location = (self.rect.w * i, self.rect.h * j)
#                 self.frames.append(sheet.subsurface(pygame.Rect(
#                     frame_location, self.rect.size)))
#
#     def update(self):
#         self.cur_frame = (self.cur_frame + 1) % len(self.frames)
#         self.image = self.frames[self.cur_frame]


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
            screen.blit(pygame.transform.scale(player_walk_image[0], (70, 70)), (self.x, self.y))

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
        pygame.draw.circle(screen, 'yellow', (self.x, self.y), 5)


class YetiEnimy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-300, 300)
        self.offset_y = random.randrange(-300, 300)

    def main(self, screen):
        if self.animation_count + 0.2 >= 47:
            self.animation_count = 0
        else:
            self.animation_count += 0.2

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

        screen.blit(pygame.transform.scale(yeti_animation[int(self.animation_count)], (30, 30)),
                    (self.x - display_scroll[0], self.y - display_scroll[1]))
        print(pygame.time.get_ticks())


enimies = [YetiEnimy(400, 400)]

player = Player(400, 300, 40, 40)

display_scroll = [0, 0]

player_bulets = []

while True:
    screen.fill((100, 255, 200))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.QUIT
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player_bulets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))

    keys = pygame.key.get_pressed()

    pygame.draw.rect(screen, 'pink', (100 - display_scroll[0], 100 - display_scroll[1], 20, 20))

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

    clock.tick(40)

    pygame.display.update()
