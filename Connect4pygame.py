# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 01:30:00 2020

@author: snice
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 23:16:48 2020

@author: snice
"""

import numpy as np
import pygame
import sys

#On initialise les couleurs en RGB
BLUE = (0,0,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)

#On initialise les paramètres graphiques du board
SQUARESIZE=100
RADIUS=int(SQUARESIZE/2 -5)

#On initialise les variables globales qui définissent la taille du board
NB_ROWS=6
NB_COLS=7

#On initialise les jetons jouer et IA
PLAYER=0
AI=1


pygame.init() #On initialise le jeu
    

width=NB_COLS*SQUARESIZE
height=(NB_ROWS+1)*SQUARESIZE #Une de plus pour pouvoir choisir où on met le jeton
size=(width,height)
screen=pygame.display.set_mode(size) #On définit la taille de la fenêtre de jeu

myfont=pygame.font.SysFont("monospace",75)


def create_board():
    board=np.zeros((NB_ROWS,NB_COLS))
    return board


def drop_piece(board,row,col,piece):
    """Placer le jeton dans le board"""
    board[row][col]=piece
    

def is_valid_location(board,col):
    """La colonne choisie par le joueur est-elle libre ?"""
    return(board[0][col]==0)


def get_next_open_row(board,col):
    """A quelle hauteur la pièce va-t-elle se placer ?"""
    for r in range(NB_ROWS-1,-1,-1):
        if board[r][col]==0:
            return r
    return ("This column is not valid !")    

def winning_move(board,piece):
    #On reagard d'abord toutes les lignes
    #On commence par les lignes du bas pour plus de rapidité
    #On pourrait commencer par la ligne où a été déposé la dernière pièce
    for r in range (NB_ROWS):
        for c in range(NB_COLS-3): #Inutile d'aller plus loin
            if np.all(board[r,c:c+4]==[piece]*4): #On  regarde s'il y a 4 jetons identiques d'affilé sur une ligne
                return (True)
    #On fait de même pour toutes les colonnes
    for c in range (NB_COLS):
        for r in range(NB_ROWS-3): #Inutile d'aller plus loin
            #print(board[r:r+4,c])
            if np.all(board[r:r+4,c]==[piece]*4): #On  regarde s'il y a 4 jetons identiques d'affilé sur une ligne
                return (True)    
    #De même pour les diagonales 
    for r in range(NB_ROWS-3):
        for c in range(NB_COLS-3):
            #diag=[board[i][j] for i in range(r,r-4) for j in range(c,c+4)]
            diagpos=[]
            diagneg=[]
            for i in range(4):
                diagpos.append(board[NB_ROWS-1-r-i][c+i])
                diagneg.append(board[r+i][c+i])
            if np.all(diagpos==[piece]*4) or np.all(diagneg==[piece]*4):
                return (True)  
            
            
def draw_board(board):
    for r in range (NB_ROWS):
          for c in range(NB_COLS):
              #On définit un rectangle par la surface où il est dessiné, sa couleur 
              #et un tuple(x,y,width,height) avec (x,y) coordonnées du coin en haut à gauche comme dans Image.Draw
              pygame.draw.rect(screen,BLUE,(c*SQUARESIZE,(r+1)*SQUARESIZE,SQUARESIZE,SQUARESIZE))  
              if board[r][c]==0:
                  pygame.draw.circle(screen, BLACK,(int((c+0.5)*SQUARESIZE),int((r+1+0.5)*SQUARESIZE)),RADIUS)
              elif board[r][c]==1:
                  pygame.draw.circle(screen, RED,(int((c+0.5)*SQUARESIZE),int((r+1+0.5)*SQUARESIZE)),RADIUS)
              else:
                  pygame.draw.circle(screen, YELLOW,(int((c+0.5)*SQUARESIZE),int((r+1+0.5)*SQUARESIZE)),RADIUS)
    pygame.display.update()
       


    
board=create_board()
draw_board(board)
game_over=False
turn=0


while not game_over:
    #On définit ce qu'il se passe lorsque pyagme détecte un event
    for event in pygame.event.get():
        
        if event.type==pygame.QUIT: #On quitte le jeu en appiyant sur la croix rouge
            #sys.exit()
            pygame.quit()
        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            posx=event.pos[0]
            if turn%2==0:
                pygame.draw.circle(screen,RED,(posx,SQUARESIZE//2),RADIUS)
            else:
                pygame.draw.circle(screen,YELLOW,(posx,SQUARESIZE//2),RADIUS)
        pygame.display.update()  #Always update the display after changing something 
        
        if event.type==pygame.MOUSEBUTTONDOWN: #Si (et seulement si) on appuie avec la souris
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            #print(event.pos) #prints list of the 2 coordinates of the mouse click
            if turn%2==0:#Le Joueur 1 choisi sa colonne
                posx=event.pos[0]
                col = posx//SQUARESIZE
                piece=1
                if is_valid_location(board, col):
                    row=get_next_open_row(board, col)
                    drop_piece(board, row, col, piece)
                    if winning_move(board,piece):
                        label=myfont.render("Player 1 wins !",1,RED)
                        screen.blit(label,(40,10)) #Only update this part of the screen
                        game_over=True
                        
            else: #Le Joueur 2 choisi sa colonne
                posx=event.pos[0]
                col = posx//SQUARESIZE
                piece=2
                if is_valid_location(board, col):
                    row=get_next_open_row(board, col)
                    drop_piece(board, row, col, piece)
                    if winning_move(board,piece):
                        label=myfont.render("Player 2 wins !",1,YELLOW)
                        screen.blit(label,(40,10)) #Only update this part of the screen
                        game_over=True
            draw_board(board)
            turn +=1  
            
            if game_over: #Wait 1 sec before closing
                pygame.time.wait(1000)
                    
