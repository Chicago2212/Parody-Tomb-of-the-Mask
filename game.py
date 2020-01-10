import pygame
import os
import random
import sys

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
screen2 = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    global fullname
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprite)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def start_screen():
    intro_text = ['Начать игру', '',
                  'Правила игры', '',
                  'Выйти']
    font = pygame.font.Font(None, 30)
    text_coord = 170
    pygame.draw.rect(screen, (255, 0, 0), (170, 170, 165, 45), 0)
    pygame.draw.rect(screen, (255, 0, 0), (170, 230, 165, 45), 0)
    pygame.draw.rect(screen, (255, 0, 0), (170, 290, 165, 45), 0)
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 180
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def terminate():
    pygame.quit()
    sys.exit()


class Game(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprite)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for i in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        cell = (mouse_pos[0] - self.left) // self.cell_size, (
                mouse_pos[1] - self.left) // self.cell_size
        if 0 <= cell[0] < self.width and 0 <= cell[1] < self.height:
            return cell
        return None

    def on_click(self, cell_coords):
        if cell_coords:
            self.board[cell_coords[1]][cell_coords[0]] = 1 - self.board[cell_coords[1]][
                cell_coords[0]]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Movement(Board):
    def __init__(self, width, height):
        super().__init__(width, height)


def load_level(filename):
    fulename = "data/" + filename
    with open(fulename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'wall': load_image('stena.png'), 'start': load_image('start.png'),
               'player': load_image('player_tomb_mask.png')}
player_image = load_image('mar.png')
tile_width = tile_height = 47


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprite_start_end, all_sprite_wall)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        print(tile_type, pos_x, pos_y)
        if tile_type == 'start':
            self.add(all_sprite_start_end)
        if tile_type == 'wall':
            self.add(all_sprite_wall)
        if tile_type == 'player':
            self.add(sprite_player)


def generate_level(spisok):
    for i in range(len(spisok)):
        for j in range(len(spisok[i])):
            print(j)
            if spisok[i][j] == '@':
                Tile('start', j, i)
            if spisok[i][j] == ',':
                Tile('wall', j, i)
            if spisok[i][j] == '!':
                Tile('player', j, i)
    return


# Задействие музыки в игре
# file = 'crash.wav.mp3'
pygame.init()
pygame.mixer.init()
# pygame.mixer.music.load(file)
# pygame.mixer.music.play(-1)

all_sprite = pygame.sprite.Group()
all_sprite_start_end = pygame.sprite.Group()
all_sprite_wall = pygame.sprite.Group()
sprite_player = pygame.sprite.Group()
dragon = AnimatedSprite(load_image('dragon_sheet8x2.png'), 8, 2, 20, 375)
clock = pygame.time.Clock()
running = True
s = 0
t = 0
board = Movement(500, 500)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if x in range(170, 336) and y in range(170, 216):
                Mask = Game(load_image('mar.png'), 8, 2, 20, 375)
                s = 1

    all_sprite.update()
    if s == 0:
        screen.fill((255, 255, 255))
        all_sprite.draw(screen)
        start_screen()
    elif s == 1:
        screen.fill((0, 0, 0))
        generate_level(load_level('1.txt'))
        all_sprite_start_end.draw(screen)
        print(len(all_sprite_start_end.sprites()))
    clock.tick(20)
    pygame.display.flip()
pygame.quit()
