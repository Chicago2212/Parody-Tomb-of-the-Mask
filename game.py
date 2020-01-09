import pygame
import os
import random
import sys

pygame.init()
size = width, height = 500, 500
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


# Задействие музыки в игре
file = 'crash.wav.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play(-1)

all_sprite = pygame.sprite.Group()
dragon = AnimatedSprite(load_image('dragon_sheet8x2.png'), 8, 2, 20, 375)
clock = pygame.time.Clock()
running = True
s = 0
t = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if x in range(170, 336) and y in range(170, 216):
                Mask = Game(load_image('mar.png'), 8, 2, 20, 375)
                s = 1
    screen.fill((255, 255, 255))
    all_sprite.update()
    if s == 0:
        all_sprite.draw(screen)
        start_screen()
    clock.tick(20)
    pygame.display.flip()
pygame.quit()
