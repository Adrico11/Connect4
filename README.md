## Connect4 Game

1. Implement different versions of the Connect4 game with increasing complexity
2. Add the possibility to play against an AI which uses the minimax algorithm to make its moves

## Details on the Minimax algorithm
Recursive algorithm allowing the AI to make moves based on the score of the different boards each of his possible moves might lead up to 
(to predict the next moves following a potential one of his own, the AI supposes that both players will always play their best possible move)

This process is done until the board following the Nth next move (= depth of the algorithm) is reached and a score is then attributed to the resulting board.

### Contents of the files in this repo :
- Connect4.py : basic game where two players can compete
- Connect4pygame.py : same game format but with an additional realistic graphical interface implemented with pygame
- Connect4_RadomAI : allows a player to play against the computer that plays randomly with this same graphical interface
- Connect4_AI : implements a more advanced artificial intelligence (defines a score for each of its possible moves based on the following board configuration : it is a minimax of depth equal to 1)
- Connect4_AIMinimax : added a full implementation of the minimax algorithm 
- Connect4_AIMinimaxAlphaBeta : added implementation of the minimax algorithm with an alpha-beta pruning which speeds up the execution time at each turn of the AI

### Instructions :
Do not hesitate to change the depth of the minimax algorithm (the calculation time becomes however rather long beyond 6 (exponential complexity...)) 
There is sometimes a small bug when closing the game (just force the program to close)
