from functools import partial
from io import BytesIO
from PIL import Image, ImageTk
from importlib_resources import files

import ilchess.gui.figs
from ilchess.gui.gui_settings import *
from ilchess.state import default_state

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


def _get_color(row, col, highlight=False):
    if (row + col) % 2:
        return black_bg_hl if highlight else black_bg
    else:
        return white_bg_hl if highlight else white_bg


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
    of the controller board.
    It only has two functions:
        `__init__` (initializes board and draws all figures)
        `update_state` (updates board state on figure selection and move)
    """
    def __init__(self, state, available_moves, history=None):
        self._transformation_handler = []
        self._reverted = False
        if history is None:
            history = []
        self._selected_square = None
        self._available_moves = available_moves
        self._history = history
        self._move_handlers = []
        _label_top()
        _label_side()
        self._canvas = []
        self._images = []
        self._state = None
        self._promotion_canvas = []
        self._fig_for_promotion = {11: 'q', 12: 'b', 13: 'n', 14: 'r'}
        self._fig_promotion = None
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
                self._add_canvas_click_handler(row, col)
        self._rotate_btn = tk.Button(tk_root, text='Coup', width=10, height=5, bd='10', command=self._rotate)
        self._rotate_btn.place(x=1150, y=905)
        self._hl_list = []
        self.update_state(state, history, available_moves)

    def _get_state_pos(self, row, col):
        return (7 - row, 7 - col) if self._reverted else (row, col)

    def update_state(self, state, history, available_moves):
        self._state = state
        self._history = history
        self._available_moves = available_moves
        print("self._images ", self._images)

        for row in range(8):
            for col in range(8):
                fig_image = self._images[row][col]
                if fig_image is not None:
                    self._canvas[row][col].delete(fig_image)
                state_row, state_col = self._get_state_pos(row, col)

                self._images[row][col] = _draw_figure(self._canvas[row][col], self._state[state_row][state_col])

    def _handle_move(self, pos_from, pos_to):
        for handler in self._move_handlers:
            # b_controller.perform_move
            handler(pos_from, pos_to)

    def _on_square_click(self, row, col, _):
        selected_square = self._selected_square
        print("row col = ", row, col)
        state_row_col = self._get_state_pos(row, col)
        print("selected square: ", selected_square)
        if selected_square is not None:
            print("SELECTED SQUARE" + str(selected_square))
            square_moves = self._available_moves.get(selected_square)
            if square_moves is not None and (selected_square, state_row_col) in square_moves:
                self._handle_move(pos_from=selected_square, pos_to=state_row_col)
            for _, (r, c) in square_moves:
                r, c = self._get_state_pos(r, c)
                self._canvas[r][c].configure(bg=_get_color(r, c, highlight=False))
            self._selected_square = None
            self._hl_list = []

        else:
            avail_moves = self._available_moves.get(state_row_col)
            for r in range(0, 8, 7):
                for c in range(0, 8):
                    if self._state[r][c] == 'p':
                        avail_moves = None
                        break
            # TODO: elaborated logic here, on square select, on square deselect, premove, etc
            # For now only highlight available squares

            if avail_moves is not None:
                # add self._hl_list logic here
                self._hl_list = []
                for _, (r, c) in avail_moves:
                    print("debugging r c", r, c)
                    r, c = self._get_state_pos(r, c)
                    self._hl_list.append((r, c))
                    self._canvas[r][c].configure(bg=_get_color(r, c, highlight=True))
                self._selected_square = state_row_col

    def promoting_pawn(self, move_history):
        list_fig_promotion = ["q", "b", "n", "r"] if len(move_history) % 2 != 0 else ["Q", "B", "N", "R"]
        for num, figure in enumerate(list_fig_promotion):
            r = 2 + num
            c = 9
            promotion_canvas = tk.Canvas(
                tk_root,
                width=square_width,
                height=square_width,
                border=0,
                bg="white",
                cursor="hand2"
            )
            promotion_canvas.grid(row=r + 1, column=c)
            promotion_canvas.bind('<Button-1>', partial(self._on_promotion_canvas_click, r, c))
            self._promotion_canvas.append(promotion_canvas)
            _draw_figure(promotion_canvas, figure)
        tk_root.update_idletasks()

    def _delete_promotion_canvases(self):
        for promotion_canvas in self._promotion_canvas:
            promotion_canvas.destroy()
        self._promotion_canvas = []

    def _on_promotion_canvas_click(self, row, col, _):
        if len(self._history) % 2 == 0:
            self._transformation_move(row, col, self._fig_for_promotion[row + col].upper())
        else:
            self._transformation_move(row, col, self._fig_for_promotion[row + col])
        for c in range(4):
            self._promotion_canvas[c].destroy()
        self._promotion_canvas = []


    def _transformation_move(self, row, col, fig):
        for handler in self._move_handlers:
            handler(row, col, fig)

    def _add_canvas_click_handler(self, row, col):
        self._canvas[row][col].bind('<Button-1>', partial(self._on_square_click, row, col))

    def _rotate(self):
        self._reverted = not self._reverted

        self.update_state(self._state, self._history, self._available_moves)
        new_hl_list = []
        for (r, c) in self._hl_list:
            self._canvas[r][c].configure(bg=_get_color(r, c, highlight=False))
            r, c = 7 - r, 7 - c
            new_hl_list.append((r, c))
            self._canvas[r][c].configure(bg=_get_color(r, c, highlight=True))
        self._hl_list = new_hl_list

    def add_transformation_handler(self, transformation_handler):
        self._transformation_handler.append(transformation_handler)

    def add_move_handler(self, move_handler):
        self._move_handlers.append(move_handler) #added b_controller.perform_move