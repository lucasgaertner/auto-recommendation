import pygame
import sys
from time import sleep
import numpy as np
import pandas as pd
import os
import re

#from auto.main import *
from constant import BLOCKSIZE, BLUE, GREY, GREEN, WHITE
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



    win_width = 550 
    win_height = 500

    row = 2
    col = 2

    LIMIT = 0
    DONE = False
    choosen = False
    choose_counter = 0
    position_dict = {}
    board = Board()
    SCREEN, CLOCK = board.Grid(win_height, win_width)
    
    font = pygame.font.Font('freesansbold.ttf', 32)
    while not DONE:      
        events = pygame.event.get()
        edits = False
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
                print("this is the last typed word:", word)
                n_best = get_corrections(word, probs, vocab, n=2, verbose=False)
                print("nbest solutions:", n_best)
                if n_best != [] and len(n_best[0]) > 1:
                    edits = True
                    choosen = True
                    print("Got a n_best Solution", n_best)
                    source = word
                    # recommendation over text ares
                    solutions = len(n_best[0])
                    pygame.draw.rect(SCREEN,GREEN,(10,win_width/2,win_height-20,50))
                    for idx, n in enumerate(n_best):
                        set_rect = (win_height/solutions*idx + 10,win_width/2,win_height-20, 50)
                        text = font.render(str(n[0]), True, WHITE)
                        SCREEN.blit(text, set_rect)

                    #targeting = board.selection(n_best,win_height,margin)
                    target = n_best[0][0]
                    matrix, min_edits, tmp_matrix = min_edit_distance(source, target)
                    idx = list('#' + source)
                    cols = list('#' + target)
                    df = pd.DataFrame(matrix, index=idx, columns= cols)
                    row, col = df.shape[0], df.shape[1]
                    grid = board.Matrix(row, col)
                else:
                    edits = False
                    print("No Solution Matrix")
                board.draw_squares(SCREEN, CLOCK, row, col, grid)
                if edits:
                    board.set_source(SCREEN, CLOCK, row, col, df, source, target)
                    pygame.display.update()
                    board.fill(SCREEN, CLOCK, row, col, tmp_matrix, source, target)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and choosen:
                pygame.draw.rect(SCREEN,GREY,(win_height/solutions*0 + 10,win_width/2 + 30,win_height/2, 20))
                choose = True
                choosen = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and choose:
                print("get the number from the field", n_best[choose_counter][0])
                choose = False
                #reset the recommendation
                pygame.draw.rect(SCREEN,GREY,(10,win_width/2,win_height-20,50))
                # reset the grid
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and choose:
                old_choosen = choose_counter
                if choose_counter >= solutions-1:
                    choose_counter = 0
                else:
                    choose_counter += 1
                pygame.draw.rect(SCREEN,GREY,(win_height/solutions*choose_counter + 10,win_width/2 + 30,win_height/2, 20))
                pygame.draw.rect(SCREEN,GREEN,(win_height/solutions*old_choosen -10 ,win_width/2 + 30,win_height/2, 20))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and choose:
                old_choosen = choose_counter
                if choose_counter > solutions:
                    choose_counter = 0
                else:
                    choose_counter += 1
                pygame.draw.rect(SCREEN,GREEN,(win_height/solutions*old_choosen + 10,win_width/2 + 30,win_height/2, 20))
                pygame.draw.rect(SCREEN,GREY,(win_height/solutions*choose_counter + 10,win_width/2 + 30,win_height/2, 20))
        print(type(textinput))
        pygame.draw.rect(SCREEN,BLUE,(0,win_width/2 + 50,win_width,win_width/3 + 50)) # Plus 50 because of recommendation
        text = textinput.update(events)
        # Blit its surface onto the screen
        SCREEN.blit(textinput.get_surface(), (10, win_width/2 + 50))
        pygame.display.update()
        CLOCK.tick(30)


if __name__ == '__main__':
    main()