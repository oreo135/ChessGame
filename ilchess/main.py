from ilchess.gui.board_view import BoardView
from ilchess.gui.gui_settings import tk_root
from ilchess.state import default_state
from ilchess.controller.board_controller import BoardController
from ilchess.gui.gui_settings import *
from tkinter import *



def main():

    current_state = default_state[:]
    b_controller = BoardController(current_state, [])
    available_moves = b_controller.get_available_moves()
    b_view = BoardView(current_state, available_moves)
    b_view.add_move_handler(b_controller.perform_move)
    b_controller.add_move_handler(b_view.update_state)
    b_controller.add_transformation_handler(b_view.promoting_pawn)
    b_view.add_transformation_handler(b_controller.to_standard_notation)
    # Implement function which prints available moves instead of board state in onClick of BoardView.
    tk_root.mainloop()



if __name__ == '__main__':
    main()
