# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 23:16:48 2020

@author: snice
"""

import numpy as np

#On initialise les variables globales qui définissent la taille du board
NB_ROWS=6
NB_COLS=7

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


def connect4():
    
    board=create_board()
    print(board)
    game_over=False
    turn=0
     
    while not game_over:               
        
        #Le Joueur 1 choisi sa colonne
        if turn%2==0:
            piece=1
            col = int(input("Player 1 make your selection (1-7):"))-1
            if is_valid_location(board, col):
                row=get_next_open_row(board, col)
                drop_piece(board, row, col, piece)
                if winning_move(board,piece):
                    print("Player 1 wins !!")
                    game_over=True
        #Le Joueur 2 choisi sa colonne
        else:
            piece=2
            col = int(input("Player 2 make your selection (1-7):"))-1
            if is_valid_location(board, col):
                row=get_next_open_row(board, col)
                drop_piece(board, row, col, piece)
                if winning_move(board,piece):
                    print("Player 2 wins !!")
                    game_over=True
        print(board)
        turn +=1  
    