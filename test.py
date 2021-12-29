valid_loc = [0,1,5]

def col_order(valid_loc):
    loc = [abs(x-3) for x in valid_loc]
    print(loc)
    loc_opti = [0]*len(loc)
    for i in range(len(loc)):
        idx = loc.index(min(loc))
        loc_opti[i]=(valid_loc[idx])
        loc[idx]=10
    return loc_opti

import numpy as np
board = np.zeros((6,7))
board[1,3]=1

def convert(board):
    key=''
    for i in range(6):
        for j in range(7):
            key+=str(int(board[i][j]))
    return key

print(convert(board))