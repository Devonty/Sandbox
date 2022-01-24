import pygame
import math
import random
from copy import deepcopy
import ast

from MaterialMenu import MaterialMenu
from GameBoard import GameBoard
from ToolsMenu import ToolsMenu
from Materials import *


class Game:

    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height
        self.size = (width, height)

        self.fps = 20
        # Счетчик кадров
        self.fps_count = 0

        self.material_cur = 0
        # Заблокированные/Разблокированные материалы
        self.material_dict = {
            SandMaterial: True,
            LiedGlassMaterial: False,
            GlassMaterial: False,
            WaterMaterial: True,
            SteamMaterial: False,
            GasMaterial: True,
            SeaSaltMaterial: True,
            SaltWaterMaterial: False,
            FireMaterial: True,
            LavaMaterial: False,
            StoneMaterial: True,
            SteelMaterial: True,
        }
        # Список материалов
        self.material_list = list(self.material_dict)
        # Статистические переменные / Изменяются вне этого класса
        self.paused = False
        self.pero = 1
        self.react_count = 0
        self.message = str()
        self.choosed_material = self.material_list[self.material_cur]

        # Объявление элементов игры
        self.material_menu = MaterialMenu(parent=self, material_list=self.material_list)
        self.material_menu.set_view(100, 820, cell_size=75)

        self.tools_menu = ToolsMenu(parent=self, width=375)
        self.tools_menu.set_view(1525, 100, cell_size=25)

        self.game_board = GameBoard(parent=self, width=100, height=50)
        self.game_board.set_view(100, 100, cell_size=14)

    def update(self):
        self.material_menu.update()
        self.tools_menu.update()
        self.game_board.update()

    def mainloop(self):
        pygame.init()
        pygame.display.set_caption('Sandbox')
        self.screen = pygame.display.set_mode(self.size)

        # Событие обновления
        UPDATE = pygame.USEREVENT + 1
        pygame.time.set_timer(UPDATE, 1000 // self.fps)

        running = True
        # ЛКМ Удерживается
        self.left_mouse_button_pressed = False
        # Последняя позиция мыши
        self.x_mouse = 0
        self.y_mouse = 0

        clock = pygame.time.Clock()
        while running:
            self.fps_count += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Выход
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:  # Нажата кнопка мыши
                    # Обновление позиции мыши
                    self.x_mouse, self.y_mouse = event.pos
                    if event.button == 1:
                        # ЛКМ зажата
                        # Обработка нажатий
                        self.tools_menu.get_click(event.pos)
                        self.material_menu.get_click(event.pos)
                        # Флаг на зажатие ЛКМ
                        self.left_mouse_button_pressed = True

                if event.type == pygame.MOUSEBUTTONUP:
                    # Обновление позиции мыши
                    self.x_mouse, self.y_mouse = event.pos
                    if event.button == 1:
                        # ЛКМ отжата
                        self.left_mouse_button_pressed = False

                if event.type == pygame.MOUSEMOTION:
                    self.x_mouse, self.y_mouse = event.pos

                if event.type == UPDATE:
                    if self.left_mouse_button_pressed:
                        # Создавать материал на курсоре, пока зажата ЛКМ
                        pos = (self.x_mouse, self.y_mouse)
                        self.game_board.get_click(pos)

                    # Событие на обновление
                    self.render()
                    if not self.paused:
                        self.update()

                if event.type == pygame.MOUSEWHEEL:
                    # Колесико мыши прокрутили
                    self.game_board.on_mousewheel(event.y)
                    self.tools_menu.on_mousewheel(event.y)
                    self.material_menu.on_mousewheel(event.y)


                # Обработка стрелочек на изменение направления гравитации
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.game_board.gravity_direction = 0
                    elif event.key == pygame.K_RIGHT:
                        self.game_board.gravity_direction = 1
                    elif event.key == pygame.K_DOWN:
                        self.game_board.gravity_direction = 2
                    elif event.key == pygame.K_LEFT:
                        self.game_board.gravity_direction = 3

            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()

    def render(self):
        self.screen.fill(pygame.Color('Black'))
        self.game_board.render(self.screen)
        self.tools_menu.render(self.screen)
        self.material_menu.render(self.screen)


if __name__ == '__main__':
    game = Game()
    game.mainloop()
