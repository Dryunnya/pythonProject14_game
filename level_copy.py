import pygame
import sys
import random
import math


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.animation_count = 0
        self.image = player_image[self.animation_count]
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = 5
        self.direction = 1
        self.hp = 100  # Начальное здоровье

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            for sprite in all_sprites:
                sprite.rect.x += self.speed
            self.rect.x -= self.speed
            self.direction = -1
            self.animation_count = (self.animation_count + 1) % len(player_image)
            self.image = pygame.transform.flip(player_image[self.animation_count], self.direction == -1, False)
        if keys[pygame.K_d]:
            for sprite in all_sprites:
                sprite.rect.x -= self.speed
            self.rect.x += self.speed
            self.direction = 1
            self.animation_count = (self.animation_count + 1) % len(player_image)
            self.image = pygame.transform.flip(player_image[self.animation_count], self.direction == -1, False)
        if keys[pygame.K_w]:
            for sprite in all_sprites:
                sprite.rect.y += self.speed
            self.rect.y -= self.speed
            self.animation_count = (self.animation_count + 1) % len(player_image)
            self.image = pygame.transform.flip(player_image[self.animation_count], self.direction == -1, False)
        if keys[pygame.K_s]:
            for sprite in all_sprites:
                sprite.rect.y -= self.speed
            self.rect.y += self.speed
            self.animation_count = (self.animation_count + 1) % len(player_image)
            self.image = pygame.transform.flip(player_image[self.animation_count], self.direction == -1, False)

        enemy_collisions = pygame.sprite.spritecollide(self, enemi_group, False)
        for enemy in enemy_collisions:
            self.hp -= 0.5  # Уменьшение здоровья при столкновении с врагом

        # Проверка на отрицательное здоровье (если нужно)
        if self.hp < 0:
            self.hp = 0


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player_rect, mouse_position):
        super().__init__()
        self.original_image = pygame.transform.scale(load_image("bullet.png"),
                                                     (60, 30))  # Replace "bullet_image.png" with your bullet image file
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = player_rect.center
        self.direction = math.atan2(mouse_position[1] - player_rect.centery,
                                    mouse_position[0] - player_rect.centerx)
        self.speed = 25

    def update(self):
        self.rect.x += self.speed * math.cos(self.direction)
        self.rect.y += self.speed * math.sin(self.direction)

        if self.rect.x > width or self.rect.x < 0 or self.rect.y > height or self.rect.y < 0:
            self.kill()  # Remove bullets when they go off-screen

        # Rotate the image based on the direction
        self.image = pygame.transform.rotate(self.original_image, math.degrees(-self.direction))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(enemi_group, all_sprites)
        self.animation_count = 0
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = 5
        self.reset_offset = 0
        self.offset_x = random.randrange(-300, 300)
        self.offset_y = random.randrange(-300, 300)
        self.hp = 100

    def update(self):
        # Логика движения врага
        if self.reset_offset == 0:
            self.offset_x = random.randrange(-300, 300)
            self.offset_y = random.randrange(-300, 300)
            self.reset_offset = random.randrange(80, 150)
        else:
            self.reset_offset -= 1

            if player_spr.pos_x + self.offset_x > self.rect.x:
                self.rect.x += 1
            else:
                self.rect.x -= 1

            if player_spr.pos_y + self.offset_y > self.rect.y:
                self.rect.y += 1
            else:
                self.rect.y -= 1

        # Обновление анимации врага
        self.animation_count = (self.animation_count + 1) % len(enemi_image)
        self.image = enemi_image[self.animation_count]


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.transform.scale(load_image('Sunrise.png'), (80, 80))]  # List to store animation frames
        # Load your explosion images into self.images
        for i in range(5):  # Assuming you have 5 frames
            image = pygame.Surface((30, 30))  # Replace with the actual size of your explosion images
            image.fill((255, 255, 0))  # Yellow color, you can replace with actual explosion image
            self.images.append(image)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Update the animation frames
        self.index += 1
        if self.index >= len(self.images):
            self.kill()  # Remove the explosion sprite when the animation is complete
        else:
            self.image = self.images[self.index]


player_spr = None
enemy_spr = None
display_scroll = [0, 0]


class Field:
    def __init__(self, file_path):
        self.field_data = self.load_level(file_path)
        self.sprite_size = 50

    def load_level(self, file_path):
        with open(file_path, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '-'), level_map))

    def generate_level(self):
        global player_spr, enemy_spr
        for y, row in enumerate(self.field_data):
            for x, cell in enumerate(row):
                if self.field_data[y][x] == '.':
                    Tile('empty', x, y)
                elif self.field_data[y][x] == '#':
                    Tile('wall', x, y)
                elif self.field_data[y][x] == '-':
                    Tile('back', x, y)
                elif self.field_data[y][x] == '@':
                    Tile('empty', x, y)
                    player_spr = Player(x * self.sprite_size, y * self.sprite_size)  # Create a Player object
                    player_group.add(player_spr)
                elif self.field_data[y][x] == '*':
                    Tile('over', x, y)
                elif self.field_data[y][x] == 't':
                    Tile('over', x, y)
                    Tile('plant', x, y)
                elif self.field_data[y][x] == 'F':
                    Tile('over', x, y)
                    Tile('decor', x, y)
                elif self.field_data[y][x] == 'P':
                    Tile('over', x, y)
                    Tile('tree', x, y)
                elif self.field_data[y][x] == '1':
                    Tile('empty', x, y)
                    enemy_image = pygame.transform.scale(load_image("yeti (47).png"), (70, 70))

                    # Создание объекта Enemy с загруженным изображением
                    enemy_spr = Enemy(x * self.sprite_size, y * self.sprite_size, enemy_image)
                    enemi_group.add(enemy_spr)


def load_image(filename):
    filename = 'project/' + filename
    return pygame.image.load(filename).convert_alpha()


def terminate():
    pygame.quit()
    sys.exit()


def error_screen():
    text = ['Произошла ошибка',
            'Нажмите любую клавишу',
            'для выхода из игры']

    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    fon1 = pygame.transform.scale(load_image('Background02.png'), (width, height))
    screen.blit(fon1, (0, 0))

    fon2 = pygame.transform.scale(load_image('Muntain.png'), (width, height))
    screen.blit(fon2, (0, 0))

    fon3 = pygame.transform.scale(load_image('Cloud.png'), (width, height))
    screen.blit(fon3, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# filename = str(input('название файла: '))
filename = 'pole.txt'
pygame.init()
size = width, height = 1500, 800

screen = pygame.display.set_mode(size)
FPS = 120
clock = pygame.time.Clock()

start_screen()

tile_images = {'wall': pygame.transform.scale(load_image('bricks.jpg'), (50, 50)),
               'empty': pygame.transform.scale(load_image('floor.png'), (50, 50)),
               'back': pygame.transform.scale(load_image('fon_colour.png'), (50, 50)),
               'over': pygame.transform.scale(load_image('sand.png'), (50, 50)),
               'plant': pygame.transform.scale(load_image('tree.png'), (45, 45)),
               'decor': pygame.transform.scale(load_image('flower.png'), (45, 45)),
               'tree': pygame.transform.scale(load_image('pink_tree.png'), (45, 45))}
player_image = [pygame.transform.scale(load_image(f"walk{i}.png"), (70, 70)) for i in range(1, 11)]
enemi_image = [pygame.transform.scale(load_image(f"yeti ({i}).png"), (70, 70)) for i in range(1, 48)]

tile_width = tile_height = 50

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
field_group = pygame.sprite.Group()
enemi_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


# player_spr = Player(width // 2, height // 2)
# player_group.add(player_spr)

fields = Field(filename)
fields.generate_level()

for sprite in tiles_group:
    field_group.add(sprite)


def update_hp_text(player_hp):
    font = pygame.font.Font(None, 36)
    if player_hp <= 80 and player_hp >= 40:
        text_color = (255, 205, 255)
    elif player_hp <= 40:
        text_color = (255, 0, 0)
    else:
        text_color = (255, 255, 255)

    player_hp = '%.1f' % player_hp
    text = font.render(f'HP: {player_hp}', True, text_color)
    screen.blit(text, (10, 10))
    screen.blit(text, (10, 10))


restart_count = 0  # Variable to count restarts


def restart_game():
    global player_spr, enemy_spr, display_scroll, restart_count

    restart_count += 1

    player_spr.hp = 100

    fields.generate_level()


font_restart = pygame.font.Font(None, 36)


def update_restart_text(count):
    text_restart = font_restart.render(f'Restarts: {count}', True, (255, 255, 255))
    screen.blit(text_restart, (10, 50))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
            mouse_position = pygame.mouse.get_pos()
            # Shoot bullets towards the mouse click position
            weapon = Weapon(player_spr.rect, mouse_position)
            weapon_group.add(weapon)

    player_group.update()
    weapon_group.update()
    enemi_group.update()
    explosion_group.update()

    screen.fill((0, 0, 0))

    player_center = player_spr.rect.center
    screen_center = (width // 2, height // 2)
    screen_x, screen_y = screen_center[0] - player_center[0], screen_center[1] - player_center[1]
    for sprite in all_sprites:
        sprite.rect.x += screen_x
        sprite.rect.y += screen_y

    collisions = pygame.sprite.groupcollide(weapon_group, enemi_group, True, False)
    for bullet, hit_enemies in collisions.items():
        for enemy in hit_enemies:
            enemy.hp -= 20  # Decrease enemy's health on bullet hit
            if enemy.hp <= 0:
                # Create an explosion sprite at the enemy's position when killed
                explosion = Explosion(enemy.rect.x, enemy.rect.y)
                explosion_group.add(explosion)
                enemy.kill()

    all_sprites.update()
    all_sprites.draw(screen)
    player_group.draw(screen)
    enemi_group.draw(screen)
    weapon_group.draw(screen)
    explosion_group.draw(screen)

    update_hp_text(player_spr.hp)
    if player_spr.hp == 0:
        restart_game()
    update_restart_text(restart_count)

    pygame.display.flip()
    clock.tick(30)
