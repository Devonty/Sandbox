import pygame
import math
import random
from copy import deepcopy
from ToolObjects import *


class ToolsMenu:

    def __init__(self, parent, height=700, width=200):
        self.parent = parent
        # Значения по умолчанию
        self.height = height
        self.width = width
        self.left = 1500
        self.top = 10
        self.cell_size = 75
        self.split_space = 70

        self.tools_list_class = [
            PauseCell,
            CleanerCell,
            FillerCell,
            PeroPointCell,
            PeroKrestCell,
            PeroSqareCell,
            ClearAllSqareCell,
        ]

        self.tools_list = [i for i in range(len(self.tools_list_class))]

        self.generate_pole()


    def on_click(self, cord):
        pass

    def on_mousewheel(self, event_y):
        pass


    def generate_pole(self):
        now_x = self.split_space // 2 + self.left
        now_y = self.split_space // 2 + self.top
        step = self.split_space + self.cell_size

        for i, cell in enumerate(self.tools_list):
            if now_x + self.cell_size + self.split_space >= self.left + self.width:
                now_x = self.split_space // 2 + self.left
                now_y += step
            self.tools_list[i] = self.tools_list_class[i](self.parent, now_x, now_y)
            now_x += step

    def update(self):
        pass

    def render(self, screen):
        # Граница
        params = (self.left, self.top, self.width, self.height)
        pygame.draw.rect(screen, pygame.Color('White'), params, 1)
        # Инструмены
        for cell in self.tools_list:
            cell.render(screen)


    def get_click(self, mouse_pos):
        x, y  = mouse_pos
        x -= self.left
        y -= self.top
        if not (0 <= x <= self.width) or not (0 <= y <= self.height):
            return
        for tool in self.tools_list:
            if tool.get_click(mouse_pos):
                break



    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.generate_pole()