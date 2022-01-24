import pygame
import math
import random
from copy import deepcopy


class Cell:

    def __init__(self, x, y, material, cell_size=75):
        self.x = x
        self.y = y
        self.material = material
        self.cell_size = cell_size

    def get_click(self, pos):
        x, y = pos
        if self.x <= x <= self.x + self.cell_size and \
                self.y <= y <= self.y + self.cell_size:
            return self.material
        return None

    def render(self, screen):
        color = self.material().color
        params = (self.x, self.y, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, color, params)

        font = pygame.font.Font(None, 17)
        text = font.render(self.material().name_tag, True, (100, 255, 100))
        screen.blit(text, (self.x, self.y + self.cell_size))

class MaterialMenu:

    def __init__(self, parent, material_list, height=200, width=1800):
        self.parent = parent
        self.material_list = material_list
        # Значения по умолчанию
        self.height = height
        self.width = width
        self.left = 10
        self.top = 900
        self.cell_size = 75
        self.split_space = 30

    def generate_pole(self):
        # Отрисовка списка
        now_x = self.split_space // 2 + self.left
        now_y = self.split_space // 2 + self.top
        step = self.split_space + self.cell_size

        self.pole = list()
        for material in self.material_list:
            if now_x + self.cell_size + self.split_space >= self.left + self.width:
                now_x = self.split_space // 2 + self.left
                now_y += step
            self.pole.append(Cell(now_x, now_y, material))
            now_x += step

    def update(self):
        pass

    def render(self, screen):
        # Граница
        params = (self.left, self.top, self.width, self.height)
        pygame.draw.rect(screen, pygame.Color('White'), params, 1)
        # Материалы
        for cell in self.pole:
            cell.render(screen)

    def get_cell(self, mouse_pos):
        pass

    def on_click(self, cord):
        pass

    def get_click(self, mouse_pos):
        for cell in self.pole:
            material = cell.get_click(mouse_pos)
            if material is not None:
                break
        if material is not None:
            self.parent.choosed_material = material

    def on_mousewheel(self, event_y):
        pass

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.generate_pole()
