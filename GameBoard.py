import pygame
import math
import random
import numpy as np
from copy import deepcopy
from Materials import *
from SomeUsefulTypes import CircleList


class Cell:
    def __init__(self, material=None, i = 0, j = 0):
        self.i = i
        self.j = j
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
        self.board = [[Cell(material=None, i = i, j = j) for j in range(width)] for i in range(height)]
        self.screen = None
        self.background_color = pygame.Color('White')
        self.mouse_x = 0
        self.mouse_y = 0


        self.X = CircleList([0, 1, 1, 1, 0, -1, -1, -1])
        self.Y = CircleList([-1, -1, 0, 1, 1, 1, 0, -1])
        self.J = [
            (self.width - 1, -1, -1),
            (self.width - 1, -1, -1),
            (0, self.width, 1),
            (0, self.width, 1),
        ]
        self.I = [
            (0, self.height, 1),
            (self.height - 1, -1, -1),
            (self.height - 1, -1, -1),
            (0, self.height, 1),
        ]

    def on_mousewheel(self, event_y):
        return # отключено
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
            elif cell.get_material().weight < self.parent.choosed_material().weight:
                cell.set_material(self.parent.choosed_material())
        except Exception as ex:
            print(ex)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        # print(cell)
        if cell is None:
            return None
        self.on_click(cell)

    def spawn_on_up_space(self, material, i, j):
        cur = (self.gravity_direction * 2 + 4) % len(self.X)
        while(self.board[i][j].material is not None):
            i += self.Y[cur]
            j += self.X[cur]
            if not( 0 <= i + self.Y[cur] < self.height and 0 <= j + self.X[
                cur] < self.width):
                return
        self.board[i][j].set_material(material())


    def make_reaction(self, cell1, cell2, fps_cnt=None):
        fps_cnt = fps_cnt if fps_cnt is not None else self.parent.fps_count

        material1 = cell1.get_material()
        material2 = cell2.get_material()

        react1 = material1.reaction_with_material
        react2 = material2.reaction_with_material

        was_reacted = False

        def react_local():
            if material_with.__class__ in react.keys():
                cl = react[material_with.__class__]

                if cl == DONT_CREATE_NEW_MATERIAL:
                    cl = material_me
                    cell.set_material(cl)
                elif isinstance(cl, list):
                    cl_fir, cl_sec = cl
                    cell.set_material(cl_fir())
                    self.spawn_on_up_space(cl_sec, cell.i, cell.j)
                elif cl is not None:
                    cl = cl()
                    was_reacted = True
                    cell.set_material(cl)
                elif cl is None:
                    was_reacted = True
                    cell.set_material(cl)


        react = react1
        cell = cell1
        material_me = material1
        material_with = material2
        react_local()

        react = react2
        cell = cell2
        material_me = material2
        material_with = material1
        react_local()

        return was_reacted

    def swap_cells_by_weight(self, cell1, cell2, fps_cnt=None):
        fps_cnt = fps_cnt if fps_cnt is not None else self.parent.fps_count
        material1 = cell1.get_material()
        material2 = cell2.get_material()

        if material1 is None:
            return False

        if material2 is None:
            cell2.set_material(material1)
            cell1.clear()

            material1.was_moved = fps_cnt
            return True

        if self.make_reaction(cell1, cell2):
            pass

        if material1.weight > material2.weight and (
                (material2.like_water and material1.like_water) or\
                (material2.like_water and material1.like_dust)
        ):
            cell2.set_material(material1)
            cell1.set_material(material2)

            material1.was_moved = fps_cnt
            material2.was_moved = fps_cnt
            return True

        return False

    def update(self):
        if self.paused:
            return

        self.fps_count += 1
        pole = self.board

        h = self.height
        w = self.width

        beg_i, end_i, step_i = self.I[self.gravity_direction % 4]
        beg_j, end_j, step_j = self.J[self.gravity_direction % 4]
        fps_cnt = self.parent.fps_count
        for k in range(1, 3 + 1):
            for i in range(beg_i, end_i, step_i):
                for j in range(beg_j, end_j, step_j):
                    cell = pole[i][j]
                    material = cell.get_material()

                    if material is None:
                        continue

                    # Обновление материала
                    material.update()

                    if material.to_kill:
                        cell.set_material(None)
                        continue

                    if material.need_to_become_new_material:
                        cell.set_material(material.to_material())
                        continue


                    if material.was_moved == fps_cnt:
                        continue

                    gravity = cell.material.gravity
                    direction = material.direction

                    if gravity:
                        cur = ((self.gravity_direction + max(0, gravity - 1) * 2) * 2) % 8

                        X = self.X
                        Y = self.Y

                        # Огонь
                        if material.__class__ is FireMaterial:
                            if 0 <= i + Y[material.move_direction] < self.height and 0 <= j + X[
                                material.move_direction] < self.width:
                                cell_down = self.board[i + Y[material.move_direction]][
                                    j + X[material.move_direction]]
                                if self.swap_cells_by_weight(cell, cell_down):
                                    material.was_moved = fps_cnt
                                    continue
                        # падение вниз
                        if material.was_moved != fps_cnt:
                            if 0 <= i + Y[cur] < self.height and 0 <= j + X[
                                cur] < self.width and k >= 1:
                                cell_down = self.board[i + Y[cur]][j + X[cur]]
                                self.swap_cells_by_weight(cell, cell_down)


                        # диагональный вниз
                        if material.was_moved != fps_cnt and \
                                (material.like_dust or material.like_water) and k >= 2:
                            if 0 <= i + Y[cur + direction] < self.height and \
                                    0 <= j + X[cur + direction] < self.width:
                                cell_choosen = self.board[i + Y[cur + direction]][
                                    j + X[cur + direction]]
                                # Сдвиг
                                self.swap_cells_by_weight(cell, cell_choosen)
                        # горизонтальный вниз
                        if material.was_moved != fps_cnt and material.like_water:
                            if 0 <= i + Y[cur + 2 * direction] < self.height and \
                                    0 <= j + X[cur + 2 * direction] < self.width and k >= 3:
                                cell_choosen = self.board[i + Y[cur + 2 * direction]][
                                    j + X[cur + 2 * direction]]
                                # Сдвиг
                                self.swap_cells_by_weight(cell, cell_choosen)

                    if material.was_moved != fps_cnt:
                        material.dont_move()
                        if material.need_to_become_new_material:
                            cell.set_material(material.to_material())

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

        # ВРЕМЕННОЕ отображение материала
        pygame.draw.rect(screen, self.parent.choosed_material().color, (1000, 1000, 10, 10))

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
