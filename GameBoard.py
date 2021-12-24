import pygame
import math
import random
import numpy as np
from copy import deepcopy
from Materials import *
from SomeUsefulTypes import CircleList


class Cell:
    def __init__(self, material=None):
        self.material = material
        self.was_moved = False
        self.direction = rd.choice([-1, 1])

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

        # pygame.draw.rect(screen, pygame.Color('White'), size, 1)

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
        self.gravity_direction = 2  # Up - 0, Right - 1, Down - 2, Left - 3
        self.left = 10
        self.top = 10
        self.fps_count = 0
        self.board = [[Cell(material=None) for _ in range(width)] for _ in range(height)]
        self.screen = None
        self.background_color = pygame.Color('White')

        self.X = CircleList([0, 1, 1, 1, 0, -1, -1, -1])
        self.Y = CircleList([-1, -1, 0, 1, 1, 1, 0, -1])
        self.J = [
            (0, self.width, 1),
            (0, self.width, 1),
            (self.width - 1, -1, -1),
            (self.width - 1, -1, -1),
        ]
        self.I = [
            (self.height - 1, -1, -1),
            (0, self.height, 1),
            (self.height - 1, -1, -1),
            (0, self.height, 1),
        ]

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
        try:
            if cord is None:
                return None
            y, x = cord
            cell = self.board[y][x]
            if cell.get_material() is None:
                cell.set_material(self.parent.choosed_material())
        except Exception:
            pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        # print(cell)
        if cell is None:
            return None
        self.on_click(cell)

    def swap_cells_by_weight(self, cell1, cell2, fps_cnt=None):
        fps_cnt = fps_cnt if fps_cnt is not None else self.parent.fps_count
        material1 = cell1.get_material()
        material2 = cell2.get_material()

        if material1 is None:
            return False

        if material2 is None:
            cell2.set_material(material1)
            cell1.clear()

            cell1.was_moved = 0
            cell2.was_moved = fps_cnt
            return True

        if material1.weight > material2.weight and material2.like_water:
            cell2.set_material(material1)
            cell1.set_material(material2)

            cell1.was_moved = fps_cnt
            cell2.was_moved = fps_cnt
            return True

        return False

    def swap_cells(self, cell1, cell2, fps_cnt=None):
        fps_cnt = fps_cnt if fps_cnt is not None else self.parent.fps_count
        material1 = cell1.get_material()
        material2 = cell2.get_material()

        if material1 is None:
            return False

        if material2 is None:
            cell2.set_material(material1)
            cell1.clear()

            cell1.was_moved = 0
            cell2.was_moved = fps_cnt
            return True

        return False

    def update(self):
        if self.paused:
            return

        self.fps_count += 1
        pole = self.board
        # tmp_pole = deepcopy(self.board)

        h = self.height
        w = self.width

        beg_i, end_i, step_i = self.I[self.gravity_direction % 4]
        beg_j, end_j, step_j = self.J[self.gravity_direction % 4]

        # print()
        # print(beg_i, end_i, step_i)
        # print(beg_j, end_j, step_j)
        fps_cnt = self.parent.fps_count
        for i in range(beg_i, end_i, step_i):
            for j in range(beg_j, end_j, step_j):
                cell = pole[i][j]
                material = cell.get_material()

                if cell.was_moved == fps_cnt:
                    continue

                if material is None:
                    continue

                was_moved_local = cell.was_moved
                gravity = cell.material.gravity

                if gravity:
                    cur = ((self.gravity_direction + max(0, gravity - 1) * 2) % 4 * 2) % 8

                    X = self.X
                    Y = self.Y

                    # падение вниз
                    if 0 <= i + Y[cur] < self.height and 0 <= j + X[cur] < self.width:
                        cell_down = self.board[i + Y[cur]][j + X[cur]]
                        if self.swap_cells_by_weight(cell, cell_down):
                            was_moved_local = fps_cnt

                    # диагональный вниз в пустое место
                    if was_moved_local != fps_cnt and \
                            (material.like_dust or material.like_water):

                        cell_choosen = list()

                        if 0 <= i + Y[cur - 1] < self.height and 0 <= j + X[cur - 1] < self.width:
                            tmp = self.board[i + Y[cur - 1]][j + X[cur - 1]]
                            if tmp.get_material() is None:
                                cell_choosen.append(tmp)

                        if 0 <= i + Y[cur + 1] < self.height and 0 <= j + X[cur + 1] < self.width:
                            tmp = self.board[i + Y[cur + 1]][j + X[cur + 1]]
                            if tmp.get_material() is None:
                                cell_choosen.append(tmp)

                        if cell_choosen:
                            cell_choosen = rd.choice(cell_choosen)
                            # Сдвиг
                            if self.swap_cells(cell, cell_choosen):
                                was_moved_local = fps_cnt

                    # горизонтальный вниз
                    if was_moved_local != fps_cnt and material.like_water:

                        cell_choosen = list()

                        if 0 <= i + Y[cur - 2] < self.height and 0 <= j + X[cur - 2] < self.width:
                            tmp = self.board[i + Y[cur - 2]][j + X[cur - 2]]
                            if tmp.get_material() is None:
                                cell_choosen.append(tmp)

                        if 0 <= i + Y[cur + 2] < self.height and 0 <= j + X[cur + 2] < self.width:
                            tmp = self.board[i + Y[cur + 2]][j + X[cur + 2]]
                            if tmp.get_material() is None:
                                cell_choosen.append(tmp)

                        if cell_choosen:
                            # print(len(cell_choosen))
                            cell_choosen = rd.choice(cell_choosen)
                            # Сдвиг
                            if self.swap_cells(cell, cell_choosen):
                                was_moved_local = fps_cnt

                    # веса материалов
                    if was_moved_local != fps_cnt:
                        if 0 <= i + Y[cur] < self.height and 0 <= j + X[cur] < self.width:
                            cell_down = self.board[i + Y[cur]][j + X[cur]]
                            if self.swap_cells(cell, cell_down):
                                was_moved_local = fps_cnt

                            # диагональный вниз
                            if was_moved_local != fps_cnt and (material.like_dust or material.like_dust):

                                cell_choosen = list()

                                if 0 <= i + Y[cur - 1] < self.height and 0 <= j + X[
                                    cur - 1] < self.width:
                                    tmp = self.board[i + Y[cur - 1]][j + X[cur - 1]]
                                    if tmp.get_material() is None:
                                        cell_choosen.append(tmp)

                                if 0 <= i + Y[cur + 1] < self.height and 0 <= j + X[
                                    cur + 1] < self.width:
                                    tmp = self.board[i + Y[cur + 1]][j + X[cur + 1]]
                                    if tmp.get_material() is None:
                                        cell_choosen.append(tmp)

                                if cell_choosen:
                                    cell_choosen = rd.choice(cell_choosen)
                                    # Сдвиг
                                    if self.swap_cells_by_weight(cell, cell_choosen, fps_cnt):
                                        was_moved_local = fps_cnt

        # self.board = tmp_pole

    def render(self, screen):
        self.screen = screen
        pygame.draw.rect(self.screen, self.background_color, (
            self.left - 1, self.top - 1, 2 + self.width * self.cell_size,
            2 + self.height * self.cell_size))
        for i in range(self.height):
            for j in range(self.width):
                cord = (j * self.cell_size + self.left, i * self.cell_size + self.top)
                self.board[i][j].render(screen, *cord, self.cell_size)
        # Граница поля
        pygame.draw.rect(self.screen, pygame.Color('White'), (
            self.left - 1, self.top - 1, 2 + self.width * self.cell_size,
            2 + self.height * self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
