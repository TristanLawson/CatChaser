# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 13:01:15 2020

@author: trist
"""

import pygame
import numpy

pygame.init()


display_width = 255
display_height = 255

width = 10
height = 10

square_width = 20
square_height = 20
MARGIN = 5

cat_pos = [5,4]
human_pos = [9,9]

catIsPlayer = False
humanIsPlayer = True

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Cat Chaser')

black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)

clock = pygame.time.Clock()
exitGame = False
humanTurn = True

gameGrid = [[0 for w in range(width)] for h in range(height)]
walls = [[[[0 for row1 in range(height)] for col1 in range(width)] for row2 in range(height)] for col2 in range(width)]


def displayScreen():
    gameDisplay.fill(black)
    for row in range(10):
        for col in range(10):
            if cat_pos[0] == row and cat_pos[1] == col:
                colour = red
            elif human_pos[0] == row and human_pos[1] == col:
                colour = blue
            else:
                colour = white
            pygame.draw.rect(gameDisplay,colour,[(MARGIN + square_width) * col + MARGIN,
                                                (MARGIN + square_height) * row + MARGIN,
                                                square_width,
                                                square_height])
    if humanTurn:
        colour = blue
    else:
        colour = red
    pygame.draw.rect(gameDisplay,colour,[0,0,5,5])

def eventHandler():
    global exitGame
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            exitGame = True
            return []
            
        
        if event.type == pygame.KEYUP:
            
            
            if event.key == pygame.K_UP:
                move = [-1,0]
            elif event.key == pygame.K_DOWN:
                move = [1,0]
            elif event.key == pygame.K_LEFT:
                move = [0,-1]
            elif event.key == pygame.K_RIGHT:
                move = [0,1]
            elif event.key == pygame.K_SPACE:
                move = [0,0]
            else:
                move = []
            
            return move
        
    return []

def humanMove():
    global exitGame, humanTurn, cat_pos, human_pos
    
    if humanIsPlayer:
        move = eventHandler()
        if move == []:
            return
        else:
            new_pos = numpy.add(human_pos,move)
            if validMove(human_pos,new_pos):
                human_pos = new_pos
                humanTurn = False
    else:
        move = humanBestMove()
        humanTurn = False
        
def humanBestMove():
    bestMove = human_pos
    bestMoveScore = checkHumanScore(bestMove)
    
    moves = [[1,0],[0,1],[-1,0],[0,-1]]
    
    for m in range(4):
        new_pos = numpy.add(human_pos,moves[m])
        if validMove(human_pos,new_pos):
            score = checkHumanScore(new_pos)
        else:
            score = 0
        
        if score > bestMoveScore:
            bestMove = new_pos
            bestMoveScore = score
    
    return bestMove

def checkHumanScore(pos):
    displacement = numpy.subtract(human_pos, pos)
    score = width + height - abs(displacement[0]) - abs(displacement[1])
    return score

def validMove(old_pos,new_pos):
    if old_pos[0] in range(0,height) and old_pos[1] in range(0,width) \
        and walls[old_pos[0],old_pos[1],new_pos[0],new_pos[1]] == 0:
        return True
    else:
        return False

def checkCatScore(pos):
    displacement = numpy.subtract(human_pos, pos)
    score = abs(displacement[0]) + abs(displacement[1])
    return score
    
def catBestMove():
    bestMove = cat_pos
    bestMoveScore = checkCatScore(bestMove)
    
    moves = [[1,0],[0,1],[-1,0],[0,-1]]
    
    for m in range(4):
        new_pos = numpy.add(cat_pos,moves[m])
        if validMove(cat_pos,new_pos):
            score = checkCatScore(new_pos)
        else:
            score = 0
        
        if score > bestMoveScore:
            bestMove = new_pos
            bestMoveScore = score
    
    return bestMove


def catMove():
    global exitGame, humanTurn, cat_pos, human_pos
    
    if catIsPlayer:
        move = eventHandler()
        if move == []:
            return
        else:
            new_pos = numpy.add(cat_pos,move)
            if validMove(cat_pos,new_pos):
                cat_pos = new_pos
                humanTurn = True
    else:
        cat_pos = catBestMove()
        humanTurn = True
        

while not exitGame:
    
    if humanTurn:
        humanMove()
    else:
        catMove()
    
    displayScreen()
        
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()