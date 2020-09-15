import pygame
import sys
from time import sleep
import numpy as np
import pandas as pd
import os
import re

#from auto.main import *
from constant import BLOCKSIZE, BLUE, GREY
from auto.processing import process_data, get_count, get_probs
from auto.min_edit import min_edit_distance
from auto.corrections import get_corrections
from board import Board

import pygame_textinput


def main():

    textinput = pygame_textinput.TextInput()

    # auto correction

    data = os.path.join('auto', 'shakespeare.txt')
    word_l = process_data(data)
    vocab = set(word_l)
    word_count_dict = get_count(word_l)
    probs = get_probs(word_count_dict)



    source =  'play'
    target = 'stay'
    matrix, min_edits, tmp_matrix = min_edit_distance(source, target)
    idx = list('#' + source)
    cols = list('#' + target)
    df = pd.DataFrame(matrix, index=idx, columns= cols)
    row, col = df.shape[0], df.shape[1]
    win_width = row * BLOCKSIZE + 300
    win_height = col * BLOCKSIZE 


    LIMIT = 0
    DONE = False
    position_dict = {}
    board = Board()
    SCREEN, CLOCK = board.Grid(win_height, win_width)
    grid = board.Matrix(row, col)

    while not DONE:      
        events = pygame.event.get()
        for event in events: 
            if event.type == pygame.QUIT:
                DONE = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                words = textinput.get_text()
                word = re.findall('\w+', words)
                l = len(word) - 1
                word = word[l]
                n_best = get_corrections(word, probs, vocab, n=2, verbose=False)
                print(n_best)
                if n_best != [] and len(n_best[0]) > 1:
                    source = word
                    target = n_best[0][0]
                    print()
                    #pygame.draw.rect(SCREEN,GREY,(10, win_height))
                else:
                    pass
                board.draw_squares(SCREEN, CLOCK, row, col, grid)
                board.set_source(SCREEN, CLOCK, row, col, df, source, target)
                pygame.display.update()
                board.fill(SCREEN, CLOCK, row, col, tmp_matrix, source, target)
        pygame.draw.rect(SCREEN,BLUE,(0,win_height+100,win_width,win_height + 200))
        text = textinput.update(events)
        # Blit its surface onto the screen
        SCREEN.blit(textinput.get_surface(), (10, win_height+100))
        pygame.display.update()
        CLOCK.tick(30)


if __name__ == '__main__':
    main()