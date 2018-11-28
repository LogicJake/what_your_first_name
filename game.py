# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2018-11-27 16:21:39
# @Last Modified time: 2018-11-28 16:20:29
# 调用pygame模块
import pygame
import sys
from pygame.locals import *
from math import sqrt, ceil
from prepare_data import *
import time
WINDOWWIDTH = 1080
WINDOWHEIGHT = 640

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)


def exit_windows():
    pygame.quit()
    sys.exit()


def show_en_text(content, x, y, size):
    font = pygame.font.Font(os.path.join('ttf', 'papyrus.ttf'), size)
    font.set_bold(True)
    pressKeySurf = font.render(content, True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.center = (x, y)
    SURFACE.blit(pressKeySurf, pressKeyRect)


def show_text(content, x, y, size, bold=False):
    font = pygame.font.Font(os.path.join('ttf', 'simsun.ttf'), size)
    font.set_bold(bold)
    surf = font.render(content, True, BLACK)
    rect = surf.get_rect()
    rect.center = (x, y)
    SURFACE.blit(surf, rect)


def show_start_screen():
    SURFACE.fill(WHITE)

    content = '根据最新人工智能技术，通过您与程序的交互分析出您的姓，请在测试时在心里默念您的姓!'
    show_text(content, WINDOWWIDTH / 2, WINDOWHEIGHT / 2, 20)
    show_en_text('Press space key to play.',
                 WINDOWWIDTH - 200, WINDOWHEIGHT - 50, 25)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    print('start game')
                    return
                if event.key == K_ESCAPE:
                    exit_windows()


def choose_card():
    card_num = len(CARDS)
    global INDEX
    INDEX = 0
    while True:
        SURFACE.fill(WHITE)

        content = '请确认您的姓在卡片中'
        show_text(content, WINDOWWIDTH / 2, 50, 25)

        content = '← →切换图片, space确认包含您姓的卡片'
        show_text(content, WINDOWWIDTH / 2, 100, 20)

        content = '{}/{}'.format(INDEX + 1, card_num)
        show_text(content, WINDOWWIDTH / 2,
                  WINDOWHEIGHT - WINDOWHEIGHT / 6, 25)

        card = pygame.image.load(os.path.join(
            'fig', 'card_{}.jpg'.format(INDEX)))
        size = card.get_rect().size
        card = card.convert()
        SURFACE.blit(card, (WINDOWWIDTH / 2 -
                            size[0] / 2, WINDOWHEIGHT / 2 - size[1] / 2))
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                exit_windows()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    INDEX = (INDEX - 1) % card_num
                if event.key == K_RIGHT:
                    INDEX = (INDEX + 1) % card_num
                if event.key == K_SPACE:
                    return

        pygame.display.flip()


def display_all_names():
    global SURFACE, CHOICE, DATA

    pic = pygame.image.load(os.path.join(
        'fig', 'names.jpg'))
    size = pic.get_rect().size
    pic = pic.convert()

    WINDOWWIDTH = size[0]
    WINDOWHEIGHT = size[1] + 50
    SURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    message_box = []

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                exit_windows()
            if event.type == KEYDOWN:
                key_num = event.key
                if key_num > 47 and key_num < 58:
                    message_box.append(str(key_num - 48))
                elif key_num == 8 and len(message_box) is not 0:
                    message_box.pop()  # delete the last value
                if event.key == K_SPACE:
                    if len(''.join(message_box)) != 0 and int(''.join(message_box)) < len(DATA):
                        CHOICE = int(''.join(message_box))
                        return
        SURFACE.fill(WHITE)
        SURFACE.blit(pic, (0, 0))

        text = ''.join(message_box)  # join the list value to a string
        show_text('请找出含有您姓名的一组，并输入对应序号，space键确认', WINDOWWIDTH / 2,
                  size[1], 20)
        show_text(text, WINDOWWIDTH / 2,
                  size[1] + 20, 25)
        pygame.display.flip()


def show_res():
    WINDOWWIDTH = 1080
    WINDOWHEIGHT = 640
    SURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    global INDEX, CHOICE, DATA
    SURFACE.fill(WHITE)
    show_en_text('Analysing!', WINDOWWIDTH / 2, WINDOWHEIGHT / 2, 50)
    pygame.display.update()
    time.sleep(2)

    while True:
        SURFACE.fill(WHITE)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit_windows()
                if event.key == K_SPACE:
                    return

        i = INDEX // num_b
        j = INDEX % num_b
        ans = DATA[CHOICE][i][j]
        show_text("您的姓是: " + ans, WINDOWWIDTH / 2, WINDOWHEIGHT / 2, 50)
        show_en_text('Press space key to play again.',
                     WINDOWWIDTH - 200, WINDOWHEIGHT - 50, 25)

        pygame.display.flip()


def main():
    global SURFACE, CARDS, DATA
    CARDS = os.listdir('fig')
    CARDS.remove('names.jpg')
    DATA = prepare()
    while True:
        WINDOWWIDTH = 1080
        WINDOWHEIGHT = 640
        pygame.init()
        SURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        SURFACE.fill(WHITE)
        pygame.display.set_caption('人工智能测出你的姓')

        show_start_screen()
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                exit_windows()
        choose_card()
        display_all_names()
        show_res()
        pygame.display.flip()


if __name__ == '__main__':
    main()
