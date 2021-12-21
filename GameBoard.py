import pygame
import math
import random
from copy import deepcopy
from Materials import *


class Cell:
    def __init__(self, material=None):
        self.material = material

    def set_material(self, new_material):
        self.material = new_material

    def get_material(self):
        return self.material

    def clear(self):
        self.material = None

    def render(self, screen, x, y, cell_size=30):
        size = (x, y, cell_size, cell_size)

        if self.material is not None:
            self.material.render(screen, x, y, cell_size)
        else:
            pygame.draw.rect(screen, pygame.Color('Black'), size)

        pygame.draw.rect(screen, pygame.Color('White'), size, 1)

    def __copy__(self):
        return Cell(self.material)


class GameBoard:
    # создание поля
    def __init__(self, parent, width, height, cell_color=pygame.Color('Green'), cell_size=30):
        self.parent = parent
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # значения по умолчанию
        self.paused = False
        self.gravity_direction = 1 # Up - 0, Right - 1, Down - 2, Left - 3
        self.left = 10
        self.top = 10
        self.fps_count = 0
        self.board = [[Cell(material=None) for _ in range(width)] for _ in range(height)]
        self.screen = None

    def on_mousewheel(self, event_y):
        self.gravity_direction = (self.gravity_direction + event_y) % 4

    def get_cell(self, mouse_pos):
        # Приведение координат
        x, y = mouse_pos
        x -= self.left
        y -= self.top

        if not (0 <= x <= self.width * self.cell_size) or \
                not (0 <= y <= self.height * self.cell_size):
            return None
        i = y // self.cell_size
        j = x // self.cell_size
        return i, j

    def on_click(self, cord):
        if cord is None:
            return None
        y, x = cord
        cell = self.board[y][x]
        if cell.get_material() is None:
            cell.set_material(SandMaterial())

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        # print(cell)
        if cell is None:
            return None
        self.on_click(cell)

    def update(self):
        if self.paused:
            return

        self.fps_count += 1
        pole = self.board
        tmp_pole = deepcopy(self.board)


        for i in range(self.height):
            for j in range(self.width):
                cell = pole[i][j]
                tmp_cell = tmp_pole[i][j]
                material = cell.get_material()

                if material is None:
                    continue

                gravity = cell.material.gravity
                if gravity:
                    cur = (self.gravity_direction + max(0, gravity - 1) * 2) % 4
                    X = [0, 1, 0, -1][cur]
                    Y = [-1, 0, 1, 0][cur]
                    if 0 <= i + Y < self.height and 0 <= j + X < self.width:
                        cell_down = self.board[i + Y][j + X]
                        tmp_cell_down = tmp_pole[i + Y][j + X]
                        if cell_down.get_material() is None:
                            tmp_cell_down.set_material(material)
                            tmp_cell.clear()
        self.board = tmp_pole

    def render(self, screen):
        self.screen = screen
        for i in range(self.height):
            for j in range(self.width):
                cord = (j * self.cell_size + self.left, i * self.cell_size + self.top)
                self.board[i][j].render(screen, *cord, self.cell_size)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

