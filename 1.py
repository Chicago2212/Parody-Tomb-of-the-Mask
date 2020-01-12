
import pygame
import os
import sqlite3
import random
import sys


pygame.init()
size = width, height = 1200, 600
screen = pygame.display.set_mode(size)

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




img_names = []
i = 0
s = True
while s:
    img_names.append(load_image("{}.png".format(i % 67)))
    i += 1
    for img in img_names:
        dog_rect = img.get_rect()
        screen.blit(img, dog_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
