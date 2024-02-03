from io import BytesIO
import tkinter as tk
from PIL import Image, ImageTk
from importlib_resources import files

import ilchess.gui.figs
from ilchess.gui.gui_settings import *

# small letters for whites, large letters for blacks
# 0 for empty squares
_default_state_ = [
    ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'],
]

_figures_map_ = {
    'b': 'Bishop',
    'k': 'King',
    'n': 'Knight',
    'p': 'Pawn',
    'q': 'Queen',
    'r': 'Rook'
}


def _load_fig_images():
    all_figs = files(ilchess.gui.figs)
    result = {}
    for prefix in ['w', 'b']:
        for figure in _figures_map_.values():
            img_bytes = all_figs.joinpath(prefix + figure + '.png').read_bytes()
            image = Image.open(BytesIO(img_bytes))
            image = ImageTk.PhotoImage(image)
            result[prefix + figure] = image
    return result


""" e.g. { bPawn: ImageTk.PhotoImage('figs/bPawn.png') } """
_all_figures_ = _load_fig_images()


def _draw_figure(canvas, figure_key):
    if figure_key != '0':
        figure = _figures_map_[figure_key.lower()]
        # blacks upper-case, whites lower-case
        prefix_letter = 'b' if figure_key.isupper() else 'w'
        img = _all_figures_[prefix_letter + figure]
        return canvas.create_image(figure_width, figure_height, image=img, anchor='se')


def _label_top():
    # putting letter labels at top of board
    top_labels = ["A", "B", "C", "D", "E", "F", "G", "H"][::-1]
    count = 1
    for letter in top_labels:
        letter = tk.Label(tk_root, text=letter)
        letter.grid(column=count, row=0, sticky="S")
        count += 1


def _label_side():
    # putting numbers in labels at side of board
    side_labels = [i for i in range(1, 9)]
    count = 1
    for num in side_labels:
        num = tk.Label(tk_root, text=num)
        num.grid(column=0, row=count, sticky="E")
        count += 1


class BoardView(object):
    """
    GameView is only used to represent graphical user interface
    of the game board.
    It only has two functions:
        `__init__` (initializes board and draws all figures)
        `update_state` (updates board state on figure selection and move)
    """
    def __init__(self, state):
        _label_top()
        _label_side()
        self._canvas = []
        self._images = []
        for row in range(8):
            self._images.append([])
            self._canvas.append([])
            for col in range(8):
                canvas = tk.Canvas(
                    tk_root,
                    width=square_width,
                    height=square_width,
                    border=0,
                    bg=black_bg if (row + col) % 2 else white_bg,
                    cursor="hand2"
                )
                canvas.grid(row=row+1, column=col+1)
                self._images[-1].append(None)
                self._canvas[-1].append(canvas)
        self.update_state(state)

    def update_state(self, state):
        for row in range(8):
            for col in range(8):
                fig_image = self._images[row][col]
                if fig_image is not None:
                    self._canvas[row][col].delete(fig_image)
                self._images[row][col] = _draw_figure(self._canvas[row][col], state[row][col])


def default_board_view():
    return BoardView(_default_state_)