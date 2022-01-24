import random as rd
import pygame

DONT_CREATE_NEW_MATERIAL = ("Key_to_not_change")


# родителький класс
class Material:

    def __init__(self, temperature=0):
        self.color_list = list((0, 0, 0))  # Список цветов
        self.color = rd.choice(self.color_list)  # случайный цвет
        self.gravity = 0  # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 0  # Вес
        self.like_dust = False  # как песок
        self.like_water = False  # как вода
        self.temperature = temperature  # температура текущая
        self.temperature_to_fire = None  # температура плавления
        self.temperature_to_kill = None
        self.reaction_with_material = dict()
        self.move_direction = rd.randint(0, 7)
        self.name_tag = "Name"
        # СЛУЖЕБНЫЕ! Инициализируются, но не влияют на свойства материала.
        # Нужны для обработки и упрощения физики
        self.direction = rd.choice([-1, 1])
        self.to_kill = False
        self.need_to_become_new_material = False
        self.to_material = None
        self.was_moved = -1

    def dont_move(self):
        self.direction = self.direction * (-1) ** rd.randint(1, 2)

    def update(self):
        pass

    def set_gravity(self, gravity):
        self.gravity = gravity

    def set_temperature(self, new_temperature):
        self.temperature = new_temperature

    def add_temperature(self, delta_temperature):
        self.temperature += delta_temperature

    def render(self, screen, x, y, cell_size):
        size = (x, y, cell_size, cell_size)
        pygame.draw.rect(screen, self.color, size)


class ExpamleMaterial(Material):

    def __init__(self, temperature=None):
        super().__init__()
        self.color_list = [(0, 0, 0)]  # Список цветов
        self.color = rd.choice(self.color_list)  # случайный цвет
        self.gravity = 0  # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 0  # Вес
        self.like_dust = False  # как песок
        self.like_water = False  # как вода
        self.temperature = 0  # температура текущая
        self.temperature_to_fire = None  # температура плавления
        # Словарь реакций (Если я задену Material, то стану newMaterial (Material : newMaterial))
        self.reaction_with_material = dict()


class SandMaterial(Material):

    def __init__(self, temperature=None):
        super().__init__()
        self.color_list = [(255, 255, 0), (200, 200, 10)]
        self.color = rd.choice(self.color_list)
        self.gravity = 1  # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 1600
        self.like_dust = True
        self.temperature = 0
        self.temperature_to_fire = None
        self.reaction_with_material = {
            FireMaterial: LiedGlassMaterial,
            LavaMaterial: LiedGlassMaterial,
        }
        self.name_tag = "Песок"


class WaterMaterial(Material):

    def __init__(self, temperature=None):
        super().__init__()
        self.like_water = True
        self.weight = 1000
        self.gravity = 1
        self.color_list = [(0, 0, 205), (0, 0, 139)]
        self.color = rd.choice(self.color_list)
        self.reaction_with_material = {
            SeaSaltMaterial: SaltWaterMaterial,
            FireMaterial: SteamMaterial,
            LavaMaterial: SteamMaterial
        }
        self.name_tag = "Вода"


class GasMaterial(Material):

    def __init__(self, temperature=None):
        super().__init__()
        self.like_water = True
        self.weight = 1000
        self.color_list = [(100, 100, 100), (45, 45, 45)]
        self.color = rd.choice(self.color_list)
        self.gravity = 2
        self.reaction_with_material = {
            FireMaterial: FireMaterial,
            LavaMaterial: FireMaterial
        }
        self.name_tag = "Метан"


class SeaSaltMaterial(Material):

    def __init__(self, temperature=None):
        super().__init__()
        self.color_list = [(240, 240, 240)]  # Список цветов
        self.color = rd.choice(self.color_list)  # случайный цвет
        self.gravity = 1  # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 2150  # Вес
        self.like_dust = True  # как песок
        self.like_water = False  # как вода
        self.temperature = 20  # температура текущая
        self.temperature_to_fire = None  # температура плавления
        self.reaction_with_material = {
            WaterMaterial: None
        }
        self.name_tag = "Соль"


class SaltWaterMaterial(Material):

    def __init__(self, temperature=None):
        super().__init__()
        self.color_list = [(100, 100, 230)]  # Список цветов
        self.color = rd.choice(self.color_list)  # случайный цвет
        self.gravity = 1  # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 1030  # Вес
        self.like_dust = False  # как песок
        self.like_water = True  # как вода
        self.temperature = 20  # температура текущая
        self.temperature_to_fire = None  # температура плавления
        self.reaction_with_material = {
            FireMaterial: [SeaSaltMaterial, SteamMaterial],
            LavaMaterial: [SeaSaltMaterial, SteamMaterial]
        }
        self.name_tag = "Соленая вода"


class FireMaterial(Material):

    def __init__(self, move_direction=None, temperature=None):
        super().__init__()
        self.color_list = [(255, 0, 0), (255, 69, 0), (255, 215, 0)]  # Список цветов
        self.color = rd.choice(self.color_list)  # случайный цвет
        self.gravity = 2  # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 0  # Вес
        self.like_dust = True  # как песок
        self.like_water = True  # как вода
        # температура текущая
        self.temperature = rd.randint(400, 700) if temperature is None else temperature
        self.temperature_to_fire = None  # температура плавления
        self.temperature_to_kill = 156
        # Словарь реакций (Если я задену Material, то стану newMaterial (Material : newMaterial))
        self.reaction_with_material = {
            WaterMaterial: None,
            SandMaterial: None,
            SaltWaterMaterial: None,
        }
        self.name_tag = "Огонь"

    def update(self):
        self.temperature -= 16
        if self.temperature_to_kill is not None:
            if self.temperature <= self.temperature_to_kill:
                self.to_kill = True
        self.move_direction = rd.randint(0, 7)


class SteamMaterial(Material):

    def __init__(self, temperature=None):
        super().__init__()
        self.color_list = [(200, 200, 240)]  # Список цветов
        self.color = rd.choice(self.color_list)  # случайный цвет
        self.gravity = 2  # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 1.675  # Вес
        self.like_dust = True  # как песок
        self.like_water = False  # как вода
        self.temperature = 100  # температура текущая
        self.temperature_to_fire = None  # температура плавления
        # Словарь реакций (Если я задену Material, то стану newMaterial (Material : newMaterial))
        self.reaction_with_material = dict()
        self.name_tag = "Пар"

    def dont_move(self):
        if self.was_moved != -1:
            self.need_to_become_new_material = True
            self.to_material = WaterMaterial

    def cancel_dont_move(self):
        self.need_to_become_new_material = False
        self.to_material = None


class LavaMaterial(Material):

    def __init__(self, temperature=None):
        super().__init__()
        self.color_list = [(200, 10, 10), (200, 30, 30)]  # Список цветов
        self.color = rd.choice(self.color_list)  # случайный цвет
        self.gravity = 1  # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 3100  # Вес
        self.like_dust = False  # как песок
        self.like_water = True  # как вода# температура текущая
        self.temperature = rd.randint(2000, 3000) if temperature is None else temperature
        self.temperature_to_fire = None  # температура плавления
        self.temperature_to_kill = 0
        # Словарь реакций (Если я задену Material, то стану newMaterial (Material : newMaterial))
        self.reaction_with_material = {
        }
        self.name_tag = "Лава"

    def update(self):
        self.temperature -= rd.randint(6, 11)
        if self.temperature_to_kill is not None:
            if self.temperature <= self.temperature_to_kill:
                self.need_to_become_new_material = True
                self.to_material = StoneMaterial


class LiedGlassMaterial(Material):

    def __init__(self, temperature=None):
        super().__init__()
        self.color_list = [(255, 255, 255)]  # Список цветов
        self.color = rd.choice(self.color_list)  # случайный цвет
        self.gravity = 1  # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 1500  # Вес
        self.like_dust = True  # как песок
        self.like_water = True  # как вода
        self.temperature = 3000  # температура текущая
        self.temperature_to_fire = 1550  # температура плавления
        # Словарь реакций (Если я задену Material, то стану newMaterial (Material : newMaterial))
        self.reaction_with_material = dict()
        self.name_tag = "Жидкое стекло"

    def update(self):
        self.temperature -= rd.randint(6, 11)
        if self.temperature_to_kill is not None:
            if self.temperature <= self.temperature_to_kill:
                self.need_to_become_new_material = True
                self.to_material = GlassMaterial
        if self.temperature_to_fire is not None:
            if self.temperature <= self.temperature_to_fire:
                self.need_to_become_new_material = True
                self.to_material = GlassMaterial


class SteelMaterial(Material):

    def __init__(self, temperature=None):
        super().__init__()
        self.color_list = [(168, 169, 173)]  # Список цветов
        self.color = rd.choice(self.color_list)  # случайный цвет
        self.gravity = 0  # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 7850  # Вес
        self.like_dust = False  # как песок
        self.like_water = False  # как вода
        self.temperature = 0  # температура текущая
        self.temperature_to_fire = None  # температура плавления
        # Словарь реакций (Если я задену Material, то стану newMaterial (Material : newMaterial))
        self.reaction_with_material = dict()
        self.name_tag = "Сталь"


class GlassMaterial(Material):

    def __init__(self, temperature=None):
        super().__init__()
        self.color_list = [("#c9dce2")]  # Список цветов
        self.color = rd.choice(self.color_list)  # случайный цвет
        self.gravity = 0  # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 2200  # Вес
        self.like_dust = False  # как песок
        self.like_water = False  # как вода
        self.temperature = 0  # температура текущая
        self.temperature_to_fire = None  # температура плавления
        # Словарь реакций (Если я задену Material, то стану newMaterial (Material : newMaterial))
        self.reaction_with_material = {
            FireMaterial: LiedGlassMaterial,
            LavaMaterial: LiedGlassMaterial
        }
        self.name_tag = "Стекло"


class StoneMaterial(Material):

    def __init__(self, temperature=None):
        super().__init__()
        self.color_list = [(145, 155, 150), (125, 130, 130)]  # Список цветов
        self.color = rd.choice(self.color_list)  # случайный цвет
        self.gravity = 0  # 0 - no gravity, 1 - down, 2 - up (gas)
        self.weight = 2200  # Вес
        self.like_dust = False  # как песок
        self.like_water = False  # как вода
        self.temperature = 0  # температура текущая
        self.temperature_to_fire = None  # температура плавления
        # Словарь реакций (Если я задену Material, то стану newMaterial (Material : newMaterial))
        self.reaction_with_material = {
            FireMaterial: LavaMaterial,
        }
        self.name_tag = "Камень"
