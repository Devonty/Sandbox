import pygame
import random as rd


class Cell:
    # Шаблон со свойствами клетки меню инструментов
    def __init__(self, game, x, y, cell_size=75):
        self.x = x
        self.y = y
        self.game = game
        self.cell_size = cell_size

        self.colors = [pygame.Color("Gray")]
        self.cur = 0
        self.color = self.colors[self.cur]

        self.name_tag = "Name"
        self.setup()

    # Для изменения свойств, без переопределения __init__
    def setup(self):
        pass

    # Реализация свойств кнопки
    def make_func(self):
        pass

    def get_click(self, pos):
        x, y = pos
        if self.x <= x <= self.x + self.cell_size and \
                self.y <= y <= self.y + self.cell_size:
            self.make_func()
            return True
        return False

    def render(self, screen):
        color = self.color
        params = (self.x, self.y, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, color, params)

        font = pygame.font.Font(None, 17)
        text = font.render(self.name_tag, True, (100, 255, 100))
        screen.blit(text, (self.x, self.y + self.cell_size))


class PauseCell(Cell):
    # Кнопка паузы
    def setup(self):
        self.colors = [pygame.Color('Green'), pygame.Color('Red')]
        self.color = self.colors[self.cur]
        self.cur = (self.cur + 1) % len(self.colors)
        self.name_tag = "Пауза"

    def make_func(self):
        self.color = self.colors[self.cur]
        self.cur = (self.cur + 1) % len(self.colors)

        self.game.paused = not self.game.paused


class CleanerCell(Cell):
    # Ластик
    def setup(self):
        self.name_tag = "Ластик"

    def make_func(self):
        self.game.choosed_material = None

    def render(self, screen):
        self.color = pygame.Color('Green') if self.game.choosed_material is None else pygame.Color(
            'Red')
        Cell.render(self, screen)


class PeroPointCell(Cell):
    # Пере в 1 клетку
    def setup(self):
        self.name_tag = "Перо Точка"

    def make_func(self):
        self.game.pero = 1

    def render(self, screen):
        self.color = pygame.Color('Green') if self.game.pero == 1 else pygame.Color(
            'Red')
        Cell.render(self, screen)


class PeroKrestCell(Cell):
    # Перо крестом
    def setup(self):
        self.name_tag = "Перо Крест"

    def make_func(self):
        self.game.pero = 2

    def render(self, screen):
        self.color = pygame.Color('Green') if self.game.pero == 2 else pygame.Color(
            'Red')
        Cell.render(self, screen)


class PeroSqareCell(Cell):
    # Квадрат 3x3
    def setup(self):
        self.name_tag = "Перо Квадрат"

    def make_func(self):
        self.game.pero = 3

    def render(self, screen):
        self.color = pygame.Color('Green') if self.game.pero == 3 else pygame.Color(
            'Red')
        Cell.render(self, screen)


class FillerCell(Cell):
    # Не отображается в меню, нужен для кастамизации меню
    def setup(self):
        self.name_tag = ""

    def make_func(self):
        pass

    def render(self, screen):
        pass


class ClearAllSqareCell(Cell):
    # Очистка поля
    def setup(self):
        self.color = pygame.Color('Green')
        self.name_tag = "Очистить поле"

    def make_func(self):
        game_board = self.game.game_board
        for j in range(game_board.width):
            for i in range(game_board.height):
                game_board.board[i][j].clear()

    def render(self, screen):
        Cell.render(self, screen)
