from PIL import Image, ImageDraw
import os

def paintConnect4Board(playerPos):
    img = Image.new("RGB", (791,677), "blue")
    draw = ImageDraw.Draw(img)
    for i in range(6):
        for j in range(7):
            if playerPos[i][j] == 0:
                draw.ellipse((115*j, 115*i, 115*j+100, 115*i+100),fill='white',outline='black')
            elif playerPos[i][j] == 1:
                draw.ellipse((115*j, 115*i, 115*j+100, 115*i+100),fill='yellow',outline='black')
            else:
                draw.ellipse((115*j, 115*i, 115*j+100, 115*i+100),fill='red',outline='black')
    return img

def getBoard(img : Image):
    board = [[],[],[],[],[],[]]
    for i in range(6):
        for j in range(7):
            coordX = (50+(115*j))
            coordY = (50+(115*i))
            if tuple(img.getpixel((coordX,coordY))) == tuple((255,255,255)):
                board[i].append(0)
            elif tuple(img.getpixel((coordX, coordY))) == tuple((255,0,0)):
                board[i].append(2)
            else:
                board[i].append(1)
    return board
