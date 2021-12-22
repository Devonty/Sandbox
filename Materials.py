import random as rd
import pygame

# родителький класс
class Material:

    def __init__(self):
        self.color_list = list((0,0,0)) # Список цветов
        self.color = rd.choice(self.color_list) # случайный цвет
        self.gravity = 0 # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 0 # Вес
        self.like_dust = False # как песок
        self.like_water = False # как вода
        self.temperature = 0 # температура текущая
        self.temperature_to_fire = None # температура плавления

    def set_gravity(self, bool_gravity):
        self.gravity = bool_gravity

    def set_temperature(self, new_temperature):
        self.temperature = new_temperature

    def add_temperature(self, delta_temperature):
        self.temperature += delta_temperature

    def render(self, screen, x, y, cell_size):
        size = (x, y, cell_size, cell_size)
        pygame.draw.rect(screen, self.color, size)

class Expamle(Material):

    def __init__(self):
        super().__init__()



class SandMaterial(Material):

    def __init__(self):
        super().__init__()
        self.color_list = [(255, 255, 0), (200, 200, 10)]
        self.color = rd.choice(self.color_list)
        self.gravity = 1 # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 1600
        self.like_dust = True
        self.temperature = 0
        self.temperature_to_fire = None

class WaterMaterial(Material):

    def __init__(self):
        super().__init__()
        self.like_water = True
        self.weight = 1000
        self.color_list = [(0, 0, 205), (0, 0, 139)]
        self.color = rd.choice(self.color_list)
        self.gravity = 1

class GasMaterial(Material):

    def __init__(self):
        super().__init__()
        self.like_water = True
        self.weight = 1000
        self.color_list = [(100, 100, 100), (45, 45, 45)]
        self.color = rd.choice(self.color_list)
        self.gravity = 2