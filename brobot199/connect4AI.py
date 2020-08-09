import random
import gamemanager as gm
import copy
import time
def fullBoard(board):
    for i in range(6):
        for j in range(7):
            if board[i][j] == 0:
                return False
    return True

def playedStones(board):
    count = 0
    for i in range(6):
        for j in range(7):
            if board[i][j] != 0:
                count += 1
    return count

def checkChains(board, x, y, player):
    score = 0
    for i in range(1,3,1):
        if y + i < 6:
            if board[y+i][y] == player:
                score += 1
            if i + x < 7:
                if board[y+i][x+i] == player:
                    score += 1
            if x - i > -1:
                if board[y+i][x-i] == player:
                    score += 1
        if y - i > -1:
            if board[y-i][x] == player:
                score += 1
            if x + i < 7:
                if board[y-i][x+i] == player:
                    score += 1
            if x - i > -1:
                if board[y-i][x-i] == player:
                    score += 1
        if x + i < 7:
            if board[y][x+i] == player:
                score += 1
        if x - i > -1:
            if board[y][x-i] == player:
                score+=1
    return score

def evalBoard(board):
    score = 0
    for i in range(6):
        for j in range(7):
            if board[i][j] == 1:
               score += 1
               score += checkChains(board, j,i, 1)
            elif board[i][j] == 2:
                score -= 1
                score -= checkChains(board, j, i, 2)
    return score
            

def move(board, col, yPos, player):
    board[yPos][col] = player
    return board

def minmax(board, depth, maximizing, alpha, beta):
    if depth == 0:
        return (None, evalBoard(board))
    if fullBoard(board):
        return (None, 0)
    if gm.gameWonConnect4AI(board, 1):
        return (None, 999999999)
    if gm.gameWonConnect4AI(board, 2):
        return (None, -999999999)
    colBest = 0
    if maximizing:
        playerWin = False
        maxScore = float('-inf')
        for i in range(7):
            yPos = gm.canMoveConnect4(board, i)
            if yPos != -1:
                col, score = minmax(move(copy.deepcopy(board),i,yPos,1),depth-1,False, alpha, beta)
                if depth == 7:
                    print(f'Col: {i}, score:{score}')
                if score == -999999999:
                    playerWin = True
                if playerWin and score > -999999999:
                    return (i, score)
                if score > maxScore:
                    colBest = i
                    maxScore = score
                elif score == maxScore:
                    colBest = random.choice([colBest, i])
                alpha = max(alpha,maxScore)
                if alpha >= beta:
                    return (colBest, maxScore)
        return (colBest, maxScore)
    else:
        minScore = float('inf')
        for i in range(7):
            yPos = gm.canMoveConnect4(board, i)
            if yPos != -1:
                col, score = minmax(move(copy.deepcopy(board),i,yPos,2),depth-1,True, alpha, beta)
                if score < minScore:
                    colBest = i
                    minScore = score
                beta = min(beta, minScore)
                if alpha >= beta:
                    return (colBest, minScore)
        return (colBest, minScore)



def playMove(board):
    col = minmax(board, 7, True, float('-inf'), float('inf'))[0]
    return col


    
