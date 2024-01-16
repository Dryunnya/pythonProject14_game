import os
import pygame
import pygame_menu
import time


def terminate():
    pygame.quit()
    exit()


def run_menu():
    def start_game():
        os.startfile(""'main.exe'"")

    def start_game_core():
        start_game()
        time.sleep(5)
        terminate()

    menu = pygame_menu.Menu(title='PumpRun',
                            width=monitor_size[0], height=monitor_size[1],
                            theme=theme)
    menu.add.button('START GAME', start_game_core)

    menu.add.button('QUIT', pygame_menu.events.EXIT)

    while True:
        clock.tick(FPS)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
        menu.draw(display)
        menu.update(events)

        pygame.display.flip()


ACT_RECOUNT_EVENT = pygame.USEREVENT + 1

pygame.init()

pygame.time.set_timer(ACT_RECOUNT_EVENT, 500)

FPS = 60

monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
DISPLAY_S = min(monitor_size)
display = pygame.display.set_mode(monitor_size, display=0)

clock = pygame.time.Clock()

all_time = 0
mouse_pos = (0, 0)
score = 0

size = 0

cell_s = 100
half = cell_s / 2
quarter = cell_s / 4

arrow_size = (cell_s, cell_s * 3 // 8)
cam_dx = 0
cam_dy = 0

last_given_uid = -1
forbidden_damages = []

projectiles = []
temp_text = []
mag_circles = []
locations = dict()
locations_names = []

theme = pygame_menu.themes.THEME_GREEN.copy()
theme.title_background_color = 50, 50, 50
theme.title_font_color = 59, 215, 5
theme.title_font_shadow = False
theme.title_font = pygame_menu.font.FONT_BEBAS

theme.widget_font_size = 40
theme.background_color = 173, 100, 1
theme.widget_font_color = 139, 69, 19
theme.selection_color = 255, 236, 20
theme.widget_selection_effect = pygame_menu.widgets.selection.LeftArrowSelection()
theme.widget_font = pygame_menu.font.FONT_8BIT

run_menu()
