import tkinter as tkin
from PIL import ImageTk, Image
import random
import os.path

root = tkin.Tk()
root.title('Chess')
root.geometry("1300x1000")

# define absolute OS path
script_dir = os.path.dirname(os.path.abspath(__file__))

# title
header = tkin.Label(root, text="2D Chess")
header.config(font=("courier", 20))
header.grid(column=0, row=0)

def roundLabel(moveNo):
    roundText = tkin.Label(root, text="MOVE")
    roundNo = tkin.Label(root, text=moveNo)
    roundText.grid(column=0, row=9, sticky="w")
    roundNo = roundNo.grid(column=0, row=9)

def playerLabel(playerGo):
    pass

def labelTop():
    # putting letter labels at top of board
    topLabels = ["A", "B", "C", "D", "E", "F", "G", "H"]
    count = 1
    for letter in topLabels:
        letter = tkin.Label(root, text=letter)
        letter.grid(column=count, row=0, sticky="S")
        count += 1

def labelSide():
    # putting numbers in labels at side of board
    sideLabels = [i for i in range(8, 0, -1)]
    count = 1
    for num in sideLabels:
        num = tkin.Label(root, text=num)
        num.grid(column=0, row=count, sticky="E")
        count += 1

def padding():
    lLabel = tkin.Label(root)
    lLabel.grid(column=0, ipadx=50)

def MakeBoardCanvases():
    '''Gets and stores the square images needed to make the board'''
    global blackSquares
    global whiteSquares

    blackSquares = []
    blackSquares += range(0, 32)

    whiteSquares = []
    whiteSquares += range(0, 32)

    for var in blackSquares:
        ind = blackSquares.index(var)
        blackSquares[ind] = tkin.Canvas(root, width=100, height=100, border=0, bg="black", cursor="hand2")

    for var in whiteSquares:
        ind = whiteSquares.index(var)
        whiteSquares[ind] = tkin.Canvas(root, width=100, height=100, border=0, bg="white", cursor="hand2")

    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                # Для черных клеток
                canvas = blackSquares.pop()  # Извлекаем холст из списка черных клеток
            else:
                # Для белых клеток
                canvas = whiteSquares.pop()  # Извлекаем холст из списка белых клеток
            canvas.grid(row=row + 1, column=col + 1)

    return blackSquares, whiteSquares

labelTop()
labelSide()
MakeBoardCanvases()
root.mainloop()