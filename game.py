import pygame
import os
import sqlite3
import random
import sys
import time

pygame.init()
size = width, height = 1200, 600
screen = pygame.display.set_mode(size)
screen2 = pygame.display.set_mode(size)


def check_level_star(number):
    name = 'level_star.db'
    fullname = os.path.join('data/', name)
    con = sqlite3.connect(fullname)
    cur = con.cursor()
    result = cur.execute("""SELECT kolvo FROM star
                WHERE id == {}""".format(number))
    for i in result:
        n = i[0]
    con.close()
    return n


def update_level_star(number, kolvo_star):
    name = 'level_star.db'
    fullname = os.path.join('data/', name)
    con = sqlite3.connect(fullname)
    cur = con.cursor()
    cur.execute("""Update star SET kolvo = {} WHERE id = {}""".format(kolvo_star, number))
    con.close()


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


def start_screen():
    running = True
    i = 0
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 = event.pos
                if x1 in range(75, 400) and y1 in range(51, 137):
                    running = False
                elif x1 in range(75, 400) and y1 in range(310, 396):
                    pygame.quit()
        screen.blit(load_image("GUI.png"), (0, 0))
        screen.blit(img_names[i % 95], (500, 0))
        i += 1
        all_sprite.update()
        all_sprite.draw(screen)
        clock.tick(30)
        pygame.display.flip()


def vibor_level():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                all_keys = pygame.key.get_pressed()
                if all_keys[pygame.K_ESCAPE]:
                    start_screen()
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 = event.pos
                for i in level_coord:
                    if x1 in i[0] and y1 in i[1]:
                        return level_coord.index(i) + 1
        star = []
        for i in range(1, 11):
            star.append(check_level_star(i))
        screen.blit(load_image("vibor_level.png"), (0, 0))
        for i in range(10):
            screen.blit(load_image("star_level_{}.png".format(star[i])),
                        (level_coord[i][0][0], level_coord[i][1][0] + 65))
        clock.tick(30)
        pygame.display.flip()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            # if level[y][x] == '@':
            #   Tile('start', x, y)
            if level[y][x] == ',':
                Tile('wall', x, y)
            elif level[y][x] == '#':
                new_player = Player(x, y)
            elif level[y][x] == 'w':
                Thorns('thornsw', x, y)
            elif level[y][x] == 'r':
                Thorns('thornsr', x, y)
            elif level[y][x] == 'l':
                Thorns('thornsl', x, y)
            elif level[y][x] == 'd':
                Thorns('thornsd', x, y)
            elif level[y][x] == 'm':
                Monetka('monetka', x, y)
            elif level[y][x] == 'V':
                Exit('vuhod', x, y)
            elif level[y][x] == 'b':
                Bat(x, y)
            elif level[y][x] == 's':
                Shoter(x, y)
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    fulename = "data/" + filename
    with open(fulename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


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


class Exit(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(exit_sprite)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if pygame.sprite.collide_rect(self, player):
            print(1)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(sprite_player)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 1, tile_height * pos_y + 1)

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
        self.f = False

        if pygame.sprite.spritecollideany(self,
                                          all_sprite_thorns) or pygame.sprite.spritecollideany(self,
                                                                                               all_sprite_bat):
            self.rect.x -= x
            self.f = 'game_over'
            if pygame.sprite.spritecollideany(self,
                                              all_sprite_thorns) or pygame.sprite.spritecollideany(
                self, all_sprite_bat):
                self.rect.x += x
                self.rect.y -= y
                if pygame.sprite.spritecollideany(self,
                                                  all_sprite_thorns) or pygame.sprite.spritecollideany(
                    self, all_sprite_bat):
                    self.rect.x -= x
                    self.rect.y -= y
        elif pygame.sprite.spritecollideany(self, all_sprite_wall):
            self.rect.x -= x
            self.f = True
            if pygame.sprite.spritecollideany(self, all_sprite_wall):
                self.rect.x += x
                self.rect.y -= y
                if pygame.sprite.spritecollideany(self, all_sprite_wall):
                    self.rect.x -= x
                    self.rect.y -= y

    def check(self):
        return self.f


class Thorns(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprite_thorns)
        self.image = tile_images[tile_type]
        if tile_type == 'thornsw' or tile_type == 'thornsl':
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        elif tile_type == 'thornsr':
            self.rect = self.image.get_rect().move(tile_width * pos_x + 3, tile_height * pos_y)
        elif tile_type == 'thornsd':
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y + 3)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprite_wall)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall':
            self.add(all_sprite_wall)


class Shoter(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprite_shoter)
        self.image = load_image('trap_shooter_of.png')
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self, i):

        if i % 120 <= 5:
            self.image = load_image('trap_shooter_on.png')
        else:
            self.image = load_image('trap_shooter_of.png')


class Bat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprite_bat)
        self.image = bat_r[0]
        self.x = 1
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self, i):
        self.rect.x += self.x
        if i % 9 == 0:
            if self.x > 0:
                self.image = bat_r[i % 12]
            else:
                self.image = bat_l[i % 12]
        if pygame.sprite.spritecollideany(self, all_sprite_wall) or pygame.sprite.spritecollideany(
                self, all_sprite_thorns) or pygame.sprite.spritecollideany(self, all_sprite_shoter):
            self.rect.x -= self.x
            self.x *= (-1)


class Monetka(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprite_monetka)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.i = 0

    def update(self):
        if pygame.sprite.collide_rect(self, player):
            self.i += 1
            self.kill()

    def count(self):
        return self.i


tile_images = {'wall': load_image('stena.png'), 'start': load_image('start.png'),
               'player': load_image('player_tomb_mask.png'), 'thornsw': load_image('thornsw.png'),
               'thornsr': load_image('thornsr.png'), 'thornsl': load_image('thornsl.png'),
               'thornsd': load_image('thornsd.png'), 'monetka': load_image('monetka.png'),
               'vuhod': load_image('vuhod.png')}
bat_r = [load_image("bat_r_1.png"), load_image("bat_r_2.png"), load_image("bat_r_3.png"),
         load_image("bat_r_4.png"), load_image("bat_r_5.png"), load_image("bat_r_6.png"),
         load_image("bat_r_6.png"), load_image("bat_r_5.png"), load_image("bat_r_4.png"),
         load_image("bat_r_3.png"), load_image("bat_r_2.png"), load_image("bat_r_1.png")]
bat_l = [load_image("bat_l_1.png"), load_image("bat_l_2.png"), load_image("bat_l_3.png"),
         load_image("bat_l_4.png"), load_image("bat_l_5.png"), load_image("bat_l_6.png"),
         load_image("bat_l_6.png"), load_image("bat_l_5.png"), load_image("bat_l_4.png"),
         load_image("bat_l_3.png"), load_image("bat_l_2.png"), load_image("bat_l_1.png")]
level_coord = []
for i in range(5):
    level_coord.append((range(75 + i * 193 + 15, 185 + 193 * i), range(35, 143)))
for i in range(5):
    level_coord.append((range(945 - i * 193 + 15, 1055 - 193 * i), range(227, 335)))
player_image = load_image('player_tomb_mask.png')
tile_width = tile_height = 30

# Задействие музыки в игре
# file = 'crash.wav.mp3'
pygame.init()
pygame.mixer.init()
# pygame.mixer.music.load(file)
# pygame.mixer.music.play(-1)


player = None
all_sprite = pygame.sprite.Group()
all_sprite_monetka = pygame.sprite.Group()
all_sprite_start_end = pygame.sprite.Group()
all_sprite_thorns = pygame.sprite.Group()
all_sprite_wall = pygame.sprite.Group()
sprite_player = pygame.sprite.Group()
exit_sprite = pygame.sprite.Group()
all_sprite_bat = pygame.sprite.Group()
all_sprite_shoter = pygame.sprite.Group()
clock = pygame.time.Clock()
img_names = []
for i in range(96):
    img_names.append(load_image("Anime/DCk-{}.png".format(i)))
running = True
s = 0
t = 0
x, y = 0, 0
i = 0
f = True
game_over = True
f2 = False
sostoinie = 'main_menu'
start_screen()
a = vibor_level()
sostoinie = 'vibor_level'
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            all_keys = pygame.key.get_pressed()
            if game_over:
                game_over = False
                f2 = True
                if all_keys[pygame.K_LEFT]:
                    x = (-3)
                elif all_keys[pygame.K_RIGHT]:
                    x = 3
                elif all_keys[pygame.K_UP]:
                    y = (-3)
                elif all_keys[pygame.K_DOWN]:
                    y = 3
            if all_keys[pygame.K_ESCAPE]:
                print('Здесь должно быть мини меню а пока выбор уровня')
                a = vibor_level()
                sostoinie = 'vibor_level'
    if f:
        player, level_x, level_y = generate_level(load_level('{}.txt'.format(a)))
        f = False
        sostoinie = 'play'
    screen.fill((0, 0, 0))

    exit_sprite.draw(screen)
    all_sprite_monetka.draw(screen)
    all_sprite_wall.draw(screen)
    sprite_player.draw(screen)
    all_sprite_thorns.draw(screen)
    all_sprite_bat.draw(screen)
    all_sprite_shoter.draw(screen)
    all_sprite_thorns.draw(screen)
    i += 1
    all_sprite_bat.update(i)
    all_sprite_shoter.update(i)
    if f2:
        player.update(x, y)
        all_sprite_monetka.update()
        exit_sprite.update()
        game_over = player.check()
        if game_over == 'game_over':
            f2 = False
        elif game_over:
            f2 = False
            x = 0
            y = 0
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
