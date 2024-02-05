import tkinter as tk

tk_root = tk.Tk()
tk_root.title('ilChess')
tk_root.geometry("1300x1000")

header = tk.Label(tk_root, text="2D Chess")
header.config(font=("courier", 20))
header.grid(column=0, row=0)

square_width = 120
figure_width = 111
figure_height = 120
white_bg = "white"
black_bg = "grey"
white_bg_hl = "cyan"
black_bg_hl = "red"
