import pics
import os
from PIL import Image

gamesInProgress = []

def initGame(name):
    game = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
    ]

    img = pics.paintConnect4Board(game)
    img.save(name+".png")
    gamesInProgress.append(name)

def getGameFile(name = ''):
    try:
        img = Image.open(name+".png")
        return True
    except IOError:
        return False

def removeGame(name):
    try:
        os.remove(name+'.png')
        gamesInProgress.remove(name)
        return True
    except OSError:
        return False

def moveConnect4(name, col, player):
    board = pics.getBoard(Image.open(name+".png"))
    yPos = canMoveConnect4(board, col)
    if yPos != -1:
        board[yPos][col] = player
        img = pics.paintConnect4Board(board)
        img.save(name + ".png")
        return True
    else:
        return False

def canMoveConnect4(board, col):
    for i in range(5,-1,-1):
        if board[i][col] == 0:
            return i
    return -1

def checkWinConnect4(board, x, y, player):
    if x+3 < 7:
        if board[y][x+1] == board[y][x+2] == board[y][x+3] == player:
            return True
        if y +3 < 6:
            if board[y+1][x+1] == board[y+2][x+2] == board[y+3][x+3] == player:
                return True
        if y-3 > -1:
            if board[y-1][x+1] == board[y-2][x+2] == board[y-3][x+3] == player:
                return True
    if x-7 > -1:
        if board[y][x-1] == board[y][x-2] == board[y][x-3] == player:
            return True
        if y +3 < 6:
            if board[y+1][x-1] == board[y+2][x-2] == board[y+3][x-3] == player:
                return True
        if y-3 > -1:
            if board[y-1][x-1] == board[y-2][x-2] == board[y-3][x-3] == player:
                return True
    if y+3 < 6:
        if board[y+1][x] == board[y+2][x] == board[y+3][x] == player:
            return True
    if y - 3 > -1:
        if board[y-1][x] == board[y-2][x] == board[y-3][x] == player:
            return True
    return False


def gameWonConnect4(name, player):
    board = pics.getBoard(Image.open(name+'.png'))
    for i in range(6):
        for j in range(7):
            if board[i][j] == player:
                if checkWinConnect4(board, j, i, player):
                    return True
    return False


def gameWonConnect4AI(board, player):
    for i in range(6):
        for j in range(7):
            if board[i][j] == player:
                if checkWinConnect4(board, j, i, player):
                    return True
    return False

def getBoard(name):
    img = Image.open(name+'.png')
    return pics.getBoard(img)
