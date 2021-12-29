# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 01:18:26 2020

@author: snice
"""

import numpy as np
import pygame
import sys
import random as rd

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

#On initialise les joueurs et leur jeton
PLAYER=0
PLAYER_PIECE=1
AI=1
AI_PIECE=2


pygame.init() #On initialise le jeu
    

width=NB_COLS*SQUARESIZE
height=(NB_ROWS+1)*SQUARESIZE #Une de plus pour pouvoir choisir où on met le jeton
size=(width,height)
screen=pygame.display.set_mode(size) #On définit la taille de la fenêtre de jeu

myfont=pygame.font.SysFont("monospace",75)


def create_board():
    """Initialise le board au début de la partie"""
    board=np.zeros((NB_ROWS,NB_COLS))
    return board


def drop_piece(board,row,col,piece):
    """Placer le jeton dans le board"""
    board[row][col]=piece
    

def is_valid_location(board,col):
    """La colonne choisie par le joueur est-elle libre ?"""
    return(board[0][col]==0)

def get_valid_location(board):
    """Ensemble des colonnes libres"""
    valid_loc=[]
    for c in range(NB_COLS):
        if is_valid_location(board,c):
            valid_loc.append(c)
    return valid_loc        


def get_next_open_row(board,col):
    """A quelle hauteur la pièce va-t-elle se placer ?"""
    for r in range(NB_ROWS-1,-1,-1):
        if board[r][col]==0:
            return r
    return ("This column is not valid !")    

def winning_move(board,piece):
    """Défini un joueur a gagné"""
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
    """Dessine le board avec de beaux graphiques"""
    for r in range (NB_ROWS):
          for c in range(NB_COLS):
              #On définit un rectangle par la surface où il est dessiné, sa couleur 
              #et un tuple(x,y,width,height) avec (x,y) coordonnées du coin en haut à gauche comme dans Image.Draw
              pygame.draw.rect(screen,BLUE,(c*SQUARESIZE,(r+1)*SQUARESIZE,SQUARESIZE,SQUARESIZE))  
              if board[r][c]==0:
                  pygame.draw.circle(screen, BLACK,(int((c+0.5)*SQUARESIZE),int((r+1+0.5)*SQUARESIZE)),RADIUS)
              elif board[r][c]==PLAYER_PIECE:
                  pygame.draw.circle(screen, RED,(int((c+0.5)*SQUARESIZE),int((r+1+0.5)*SQUARESIZE)),RADIUS)
              else:
                  pygame.draw.circle(screen, YELLOW,(int((c+0.5)*SQUARESIZE),int((r+1+0.5)*SQUARESIZE)),RADIUS)
    pygame.display.update()
       
    
def evaluate_window(window,piece):
    """Défini le score de la fenêtre du board considérée"""
    score=0
    opp_piece=PLAYER_PIECE
    if piece==PLAYER_PIECE:
        opp_piece=AI_PIECE
    if window.count(piece)==4: #le joueur gagne
        score+=100
    elif window.count(piece)==3 and window.count(0)==1: #le joueur peut potentiellement gagner au prochain coup
        score+=5   
    elif window.count(piece)==2 and window.count(0)==2:
        score+=2 
    elif window.count(opp_piece)==3 and window.count(0)==1: #le joueur adverse peut potentiellement gagner au prochain coup
        score-=4      
    return score    

def score_position(board,piece):
    """Donne un score à l'ensemble d'une configuration du board"""
    score=0
    #Score centre
    centerarray=[int(i) for i in list(board[:,NB_COLS//2])] #On priorise le centre du board
    center_count=centerarray.count(piece)
    score+=center_count*3
    #Score horizontal
    for r in range(NB_ROWS):
        rowarray=[int(i)for i in list(board[r,:])]
        for c in range(NB_COLS-3):
            window=rowarray[c:c+4]
            score+=evaluate_window(window,piece)
    #Score vertical
    for c in range(NB_COLS):
        colarray=[int(i)for i in list(board[:,c])]
        for r in range(NB_ROWS-3):
            window=colarray[r:r+4]
            score+=evaluate_window(window,piece)
   
    #Score diagonal
    for r in range(NB_ROWS-3):
        for c in range(NB_COLS-3):
            diagpos=[]
            diagneg=[]
            for i in range(4):
                diagpos.append(board[NB_ROWS-1-r-i][c+i])
                diagneg.append(board[r+i][c+i])
                score+=evaluate_window(diagpos,piece) 
                score+=evaluate_window(diagneg,piece)
            
    return score

def terminal_node(board):
    """Renvoi un booléen qui indique si le jeu est terminé (un joueur gagne ou board plein)"""
    return(winning_move(board,PLAYER_PIECE) or winning_move(board,AI_PIECE) or len(get_valid_location(board))==0)

def minimax(board,depth,alpha,beta,maximizingPlayer): #Considère 7**depth configuration possible (complexté exponentielle)
    """Retourne la colonne qui produit le meilleur score après depth coups"""
    valid_loc=get_valid_location(board)
    if depth==0 or terminal_node(board):
        if depth==0:
            return (None,score_position(board,AI_PIECE))
        else:
            if winning_move(board,AI_PIECE):
                return (None,10000)
            elif winning_move(board,PLAYER_PIECE):
                return (None,-10000)
            else: #Le jeu est terminé car le board est plein
                return (None,0) #Même type que dans la récursion
    if maximizingPlayer:
        value= -np.inf
        best_col=rd.randint(0,6)
        #☻board1=board.copy()
        for col in valid_loc:
            row=get_next_open_row(board,col)
            board1=board.copy()
            drop_piece(board1,row,col,AI_PIECE)
            new_value=minimax(board1,depth-1,alpha,beta,False)[1] #On ne veut que le score
            if new_value>value:
                value=new_value
                best_col=col
            #board1[row][col]=0
            alpha=max(alpha,value)
            if alpha>=beta: #Pas besoin de regarder les autres possibilités car elles ne seront pas sélectionnées par le joueur
                break
        return best_col,new_value
    else: #Joueur qui veut minimiser le gain de l'IA (=joueur)
        value=np.inf
        best_col=rd.randint(0,6)
        for col in valid_loc:
            row=get_next_open_row(board,col)
            board2=board.copy()
            drop_piece(board2,row,col,PLAYER_PIECE)
            new_value=minimax(board2,depth-1,alpha,beta,True)[1]
            if new_value<value:
                value=new_value
                best_col=col   
            beta=min(beta,value)
            if alpha>=beta:
                break
        return best_col,new_value

def pick_best_move(board,piece):
    """Retourne la meilleure colonne à jouer"""
    valid_loc=get_valid_location(board)
    best_col=rd.randint(0,6)
    best_score=-np.inf
    board1=board.copy() #VRAIE copie du board
    for c in valid_loc:
        row=get_next_open_row(board1,c)
        drop_piece(board1,row,c,piece)
        score=score_position(board1,piece)
        if score>best_score:
            best_score=score
            best_col=c
        board1[row][c]=0
    print(best_col)    
    return (best_col)    
    
    
board=create_board()
draw_board(board)
game_over=False
turn=rd.randint(PLAYER,AI)


while not game_over:
    #On définit ce qu'il se passe lorsque pyagme détecte un event
    for event in pygame.event.get():
        
        if event.type==pygame.QUIT: #On quitte le jeu en appiyant sur la croix rouge
            sys.exit()
            
        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            posx=event.pos[0]
            if turn==PLAYER:
                pygame.draw.circle(screen,RED,(posx,SQUARESIZE//2),RADIUS)
            else:
                pygame.time.wait(500)
             #   pygame.draw.circle(screen,YELLOW,(posx,SQUARESIZE//2),RADIUS)
        pygame.display.update()  #Always update the display after changing something 
        
        if event.type==pygame.MOUSEBUTTONDOWN: #Si (et seulement si) on appuie avec la souris
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            #print(event.pos) #prints list of the 2 coordinates of the mouse click
            if turn==PLAYER:#Le Joueur 1 choisi sa colonne
                posx=event.pos[0]
                col = posx//SQUARESIZE
                piece=PLAYER_PIECE
                if is_valid_location(board, col):
                    row=get_next_open_row(board, col)
                    drop_piece(board, row, col, piece)
                    if winning_move(board,piece):
                        label=myfont.render("Player 1 wins !",1,RED)
                        screen.blit(label,(40,10)) #Only update this part of the screen
                        game_over=True
                    turn +=1  
                    turn=turn%2 #On alterne entre les tours pairs (joueur) et impairs (AI)
                    draw_board(board)    
                    print(board)    
                       
    while turn==AI and not game_over: #L'IA choisi sa colonne
        piece=AI_PIECE
        col,minimax_score = minimax(board,5,-np.inf,np.inf,True)#L'IA choisit une colonne
        print(col)
        if is_valid_location(board, col):
            #pygame.time.wait(500)
            row=get_next_open_row(board, col)
            drop_piece(board, row, col, piece)
            if winning_move(board,piece):
                label=myfont.render("Player 2 wins !",1,YELLOW)
                screen.blit(label,(40,10)) #Only update this part of the screen
                game_over=True
            draw_board(board)
    
            turn +=1  
            turn=turn%2 #On alterne entre les tours pairs (joueur) et impairs (AI)
            print(board)
            
    if game_over: #Wait 3 sec before closing
        pygame.time.wait(3000)
        sys.exit()            
