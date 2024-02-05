from ilchess.gui.board_view import BoardView
from ilchess.gui.gui_settings import tk_root
from ilchess.state import default_state
from ilchess.controller.board_controller import BoardController


def main():
    current_state = default_state[:]
    b_view = BoardView(current_state)
    b_controller = BoardController(current_state, [])
    b_controller.add_move_handler(b_view.update_state)
    print(b_controller.get_available_moves())
    tk_root.mainloop()



if __name__ == '__main__':
    main()
