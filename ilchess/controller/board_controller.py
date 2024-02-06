from collections import defaultdict


def _get_figures_positions(game_state):
    white_figures_pos = defaultdict(lambda: [])
    black_figures_pos = defaultdict(lambda: [])

    for row in range(0, 8):
        for col in range(0, 8):
            figure = game_state[row][col]
            print(str(row) + ' ' + str(col) + ' ' + figure)
            if figure == '0':
                continue
            elif figure.islower():
                positions = white_figures_pos[figure]
                positions.append((row, col))
                white_figures_pos[figure] = positions
            else:
                positions = black_figures_pos[figure]
                positions.append((row, col))
                black_figures_pos[figure] = positions

    return white_figures_pos, black_figures_pos


def _king_is_atacked(player_positions, opponent_positions):
    # Check if in this position any figure is attacking our king
    pass


def _is_opposing(my_color, field_figure):
    if field_figure == '0':
        return False
    field_color = 'b' if field_figure.isupper() else 'w'
    return field_color != my_color


def _is_mine(my_color, field_figure):
    if field_figure == '0':
        return False
    field_color = 'b' if field_figure.isupper() else 'w'
    return field_color == my_color


def _is_empty_field(field_figure):
    return field_figure == '0'

def _get_my_color(move_history):
    return 'b' if len(move_history) % 2 else 'w'

def _move_is_possible(move, game_state):
    # one of the most important, should be done ASAP
    pass

def _only_possible_moves(moves, game_state):
    print("only possible moves " + str(moves))
    return [move for move in moves] # TODO if _move_is_possible(move, game_state)]

def _get_pawn_moves(pos, game_state, move_history):
    my_color = 'b' if len(move_history) % 2 else 'w'
    (row, col) = pos
    moves = []
    if my_color == 'b':
        # E7E6
        if game_state[row - 1][col] == '0' and (row - 1) >= 0:
            moves.append((row - 1, col))
        # E7E5
        if row == 6 and game_state[row - 2][col] == '0' and game_state[row - 1][col] == '0' and (row - 2) >= 0:
            moves.append((row - 2, col))
        # E4D3 if white last was pawn D2D4
        if len(move_history):
            if row == 3 and game_state[row][col - 1] == 'p' and move_history[-1][0] == (row - 2, col - 1)\
                    and move_history[-1][1] == (row, col - 1):
                moves.append((row - 1, col - 1))
            # E4F3 if white last was pawn F2F4
            if row == 3 and game_state[row][col + 1] == 'p' and move_history[-1][0] == (row - 2, col + 1)\
                    and move_history[-1][1] == (row, col + 1):
                moves.append((row - 1, col + 1))
            if _is_opposing(my_color, game_state[row - 1][col - 1]):
                moves.append((row - 1, col - 1))
        if col < 7 and _is_opposing(my_color, game_state[row - 1][col + 1]):
            moves.append((row - 1, col + 1))
    else:
        # E3E4
        if game_state[row + 1][col] == '0' and row + 1 <= 7:
            moves.append((row + 1, col))
        # E2E4
        if row == 1 and game_state[row + 2][col] == '0' and game_state[row + 1][col] == '0' and row + 2 <= 7:
            moves.append((row + 2, col))
        # E4D5
        if len(move_history):
            if row == 4 and game_state[row][col - 1] == 'P' and move_history[-1][0] == (row + 2, col - 1) \
                    and move_history[-1][1] == (row, col - 1):
                moves.append((row + 1, col - 1))
            # E4F5
            if row == 4 and game_state[row][col + 1] == 'P' and move_history[-1][0] == (row + 2, col + 1) \
                    and move_history[-1][1] == (row, col + 1):
                moves.append((row + 1, col + 1))
            if _is_opposing(my_color, game_state[row + 1][col - 1]):
                moves.append((row + 1, col - 1))
        if col < 7 and _is_opposing(my_color, game_state[row + 1][col + 1]):
            moves.append((row + 1, col + 1))
        pass
    return moves


def _get_king_moves(pos, game_state, move_history):
    my_color = 'b' if len(move_history) % 2 else 'w'
    row, col = pos
    possible_moves = [
            (row + 1, col - 1),
            (row + 1, col),
            (row + 1, col + 1),
            (row, col + 1),
            (row - 1, col + 1),
            (row - 1, col),
            (row - 1, col - 1)
    ]
    return [
        (r, c) for (r, c) in possible_moves if 0 <= r < 8 and 0 <= c < 8 and not _is_mine(my_color, game_state[r][c])
    ]



def _get_bishop_moves(pos, game_state, move_history):
    my_color = 'b' if len(move_history) % 2 else 'w'
    (row, col) = pos
    moves = []
    # Upper right diagonal
    for i_row, j_col in zip(range(1, 8), range(1, 8)):
        if (i_row + row) > 7 or (j_col + col) > 7 or _is_mine(my_color, game_state[i_row + row][j_col + col]):
            break
        elif game_state[i_row + row][j_col + col] == '0':
            moves.append((i_row + row, j_col + col))
        elif _is_opposing(my_color, game_state[i_row + row][j_col + col]):
            moves.append((i_row + row, j_col + col))
            break

    # Lower right diagonal
    for i_row, j_col in zip(range(-1, -8, -1), range(1, 8)):
        if (i_row + row) < 0 or (j_col + col) > 7 or _is_mine(my_color, game_state[i_row + row][j_col + col]):
            break
        elif game_state[i_row + row][j_col + col] == '0':
            moves.append((i_row + row, j_col + col))
        elif _is_opposing(my_color, game_state[i_row + row][j_col + col]):
            moves.append((i_row + row, j_col + col))
            break

    # Upper left diagonal
    for i_row, j_col in zip(range(1, 8), range(-1, -8, -1)):
        if (i_row + row) > 7 or (j_col + col) < 0 or _is_mine(my_color, game_state[i_row + row][j_col + col]):
            break
        elif game_state[i_row + row][j_col + col] == '0':
            moves.append((i_row + row, j_col + col))
        elif _is_opposing(my_color, game_state[i_row + row][j_col + col]):
            moves.append((i_row + row, j_col + col))
            break

    # Lower left diagonal
    for i_row, j_col in zip(range(-1, -8, -1), range(-1, -8, -1)):
        if (i_row + row) < 0 or (j_col + col) < 0 or _is_mine(my_color, game_state[i_row + row][j_col + col]):
            break
        elif game_state[i_row + row][j_col + col] == '0':
            moves.append((i_row + row,j_col + col))
        elif _is_opposing(my_color, game_state[i_row + row][j_col + col]):
            moves.append((i_row + row, j_col + col))
            break
    return moves


def _get_rook_moves(pos, game_state, move_history):
    my_color = 'b' if len(move_history) % 2 else 'w'
    (row, col) = pos
    moves = []
    # change columns, e.g. B7H7
    for tar_col in range(col - 1, col - 8, -1):
        if tar_col < 0 or _is_mine(my_color, game_state[row][tar_col]):
            break
        elif game_state[row][tar_col] == '0':
            moves.append((row, tar_col))
        elif _is_opposing(my_color, game_state[row][tar_col]):
            moves.append((row, tar_col))
            break

    # e.g. H7B7
    for tar_col in range(col + 1, col + 8):
        if tar_col > 7 or _is_mine(my_color, game_state[row][tar_col]):
            break
        elif game_state[row][tar_col] == '0':
            moves.append((row, tar_col))
        elif _is_opposing(my_color, game_state[row][tar_col]):
            moves.append((row, tar_col))
            break

    for tar_row in range(row - 1, row - 8, -1):
        if tar_row < 0 or _is_mine(my_color, game_state[tar_row][col]):
            break
        elif game_state[tar_row][col] == '0':
            moves.append((tar_row, col))
        elif _is_opposing(my_color, game_state[tar_row][col]):
            moves.append((tar_row, col))
            break

    for tar_row in range(row + 1, row + 8):
        if tar_row > 7 or _is_mine(my_color, game_state[tar_row][col]):
            break
        elif game_state[tar_row][col] == '0':
            moves.append((tar_row, col))
        elif _is_opposing(my_color, game_state[tar_row][col]):
            moves.append((tar_row, col))
            break
    return moves


def _get_knight_moves(pos, game_state, move_history):
    my_color = 'b' if len(move_history) % 2 else 'w'
    (row, col) = pos
    return [(r, c) for (r, c) in [
        (row + 2, col + 1),
        (row - 2, col + 1),
        (row + 2, col - 1),
        (row - 2, col - 1),
        (row + 1, col + 2),
        (row + 1, col - 2),
        (row - 1, col + 2),
        (row - 1, col - 2)
    ] if 0 <= r < 8 and 0 <= c < 8
      and not _is_mine(my_color, game_state[r][c])
    ]


def _get_queen_moves(pos, game_state, move_history):
    # queen is rook + bishop, so it is trivial :)
    return _get_rook_moves(pos, game_state, move_history) + _get_bishop_moves(pos, game_state, move_history)


def _is_pawn_attack(pawn_start_pos, pawn_end_pos):
    start_row, start_col = pawn_start_pos
    end_row, end_col = pawn_end_pos
    if abs(end_row - start_row) == 2:
        return False
    is_attack = abs(end_row - start_row) + abs(end_col - start_col) == 2
    return is_attack


_figure_evaluators = {
    'p': _get_pawn_moves,
    'k': _get_king_moves,
    'q': _get_queen_moves,
    'b': _get_bishop_moves,
    'n': _get_knight_moves,
    'r': _get_rook_moves
}


def _evaluate_available_moves(fig_pos, game_state, moves_history):
    fig, pos = fig_pos
    print(str(fig) + ' ' + str(pos))
    all_moves = _figure_evaluators[fig](pos, game_state, moves_history)
    return _only_possible_moves(all_moves, game_state)


def _get_available_moves(player_positions, opponent_positions, game_state, moves_history):
    available_moves = []
    for fig, positions in player_positions.items():
        for pos in positions:
            available_moves.append((pos, _evaluate_available_moves(
                (fig.lower(), pos),
                # player_positions,
                # opponent_positions,
                game_state,
                moves_history
            )))
    return available_moves


def _get_available_moves_for_state(game_state, moves_history):
    w_pos, b_pos = _get_figures_positions(game_state)
    player_positions, opponent_positions = (b_pos, w_pos) if len(moves_history) % 2 else (w_pos, b_pos)
    return _get_available_moves(player_positions, opponent_positions, game_state, moves_history)


def to_standard_notation(moves_history):
    # TODO
    pass

def from_standard_notation(standard_notation_history):
    # TODO should return (game_state, moves_history)
    pass

def _validate_moves_history(moves_history):
    # TODO
    pass



class BoardController(object):
    """
    BoardController class handles game state. It does following:
    * evaluates available moves based on players position
    * evaluates checkmate, stallmate, etc.
    * performs moves and updates view state.
    Game state is stored as array of players positions and moves history.
    """
    def __init__(self, initial_board_state, moves_history):
        """

        :param initial_board_state:
                2D 8x8 array containing figure positions. A board from blacks perspective,
                board_state[0][0] is H8, board_state[0][7] is A8.
                Starting board for standard chess game:
                    [
                        ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r'],
                        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                        ['0', '0', '0', '0', '0', '0', '0', '0'],
                        ['0', '0', '0', '0', '0', '0', '0', '0'],
                        ['0', '0', '0', '0', '0', '0', '0', '0'],
                        ['0', '0', '0', '0', '0', '0', '0', '0'],
                        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                        ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'],
                    ]
        :param moves_history:
                Each move is a tuple of tuples. For example, E4 E5: [((3, 1), (3, 3)), ((3, 6), (3 ,5))]
        """
        self._move_handlers = []
        self._board_state = initial_board_state
        _validate_moves_history(moves_history)
        self._moves_history = moves_history

    def get_available_moves(self):
        return dict(_get_available_moves_for_state(self._board_state, self._moves_history))

    def perform_move(self, start_pos, end_pos):
        # TODO actually perform move and update state
        print("you want to move from " + str(start_pos) + " to " + str(end_pos))
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        is_pawn_attack = self._board_state[start_row][start_col].lower() == 'p' and _is_pawn_attack(start_pos, end_pos)
        is_pawn_cut = is_pawn_attack and _is_empty_field(self._board_state[end_row][end_col])
        if is_pawn_cut:
            self._board_state[start_row][end_col] = '0'
        self._board_state[end_row][end_col] = self._board_state[start_row][start_col]
        self._board_state[start_row][start_col] = '0'
        self._moves_history.append((start_pos, end_pos))
        for handler in self._move_handlers:
            handler(self._board_state, self._moves_history, self.get_available_moves())



    def add_move_handler(self, move_handler):
        self._move_handlers.append(move_handler)