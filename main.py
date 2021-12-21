import pygame
import math
import random
from copy import deepcopy

from MaterialMenu import MaterialMenu
from GameBoard import GameBoard
from ToolsMenu import ToolsMenu
from Materials import *


class Game:

    def __init__(self, width=1920, height=1080):
        self.cell_size = 20
        self.width = width
        self.height = height
        self.size = (width, height)

        self.fps = 150
        self.fps_count = 0

        self.material_menu = MaterialMenu(parent=self)
        self.tools_menu = ToolsMenu(parent=self)

        self.game_board = GameBoard(parent=self, width=50, height=20)
        self.game_board.set_view(100, 100, self.cell_size)

        self.choosed_material = WaterMaterial

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
        pygame.time.set_timer(UPDATE, 50)

        running = True
        left_mouse_button_pressed = False

        clock = pygame.time.Clock()

        while running:
            # print(self.fps_count)
            self.fps_count += 1

            self.screen.fill(pygame.Color('Black'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Выход
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:  #
                    if event.button == 1:
                        # ЛКМ зажата
                        left_mouse_button_pressed = True
                        # Обработка ЛКМ
                        self.game_board.get_click(event.pos)
                        self.tools_menu.get_click(event.pos)
                        self.material_menu.get_click(event.pos)
                    if event.button == 3:
                        self.choosed_material = WaterMaterial if self.choosed_material is SandMaterial else SandMaterial
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # ЛКМ отжата
                        left_mouse_button_pressed = False

                if event.type == pygame.MOUSEMOTION:
                    if left_mouse_button_pressed:
                        # ЛКМ удерживается
                        self.game_board.get_click(event.pos)

                if event.type == UPDATE:
                    # Событие на обновление
                    self.update()
                    self.render()

                if event.type == pygame.MOUSEWHEEL:
                    self.game_board.on_mousewheel(event.y)
                    self.tools_menu.on_mousewheel(event.y)
                    self.material_menu.on_mousewheel(event.y)

            self.render()
            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()

    def render(self):
        self.game_board.render(self.screen)
        self.tools_menu.render(self.screen)
        self.material_menu.render(self.screen)


if __name__ == '__main__':
    game = Game()
    game.mainloop()
