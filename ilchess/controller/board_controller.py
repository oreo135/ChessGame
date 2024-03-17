import copy
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


def _is_check(board_state, move_history):
    his_color = 'b' if len(move_history) % 2 else 'w'
    w_pos, b_pos = _get_figures_positions(board_state)
    my_pos, his_pos = (w_pos, b_pos) if his_color == 'b' else (b_pos, w_pos)
    his_king_pos = w_pos['k'] if his_color == 'w' else b_pos['K']
    his_king_pos = his_king_pos[0]
    my_attacks = _get_available_moves(my_pos, board_state, move_history + [move_history[-1]], evaluate_checks=False)
    print('his king pos', his_king_pos)
    for _, my_attacks in my_attacks:
        print('i have moves ', my_attacks)
        for my_attack in my_attacks:
            if my_attack == his_king_pos:
                print('CHECK')
                return True
    return False


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


def _move_is_possible(move, game_state, move_history):
    updated_game_state = copy.deepcopy(game_state)
    updated_move_history = move_history[:] + [move]
    start_row, start_col = move[0]
    end_row, end_col = move[1]
    updated_game_state[start_row][start_col] = '0'
    updated_game_state[end_row][end_col] = game_state[start_row][start_col]
    w_pos, b_pos = _get_figures_positions(updated_game_state)
    enemy_possible_moves = _get_available_moves_for_state(updated_game_state, updated_move_history, evaluate_checks=False)
    our_king = w_pos['k'][0] if _get_my_color(move_history) == 'w' else b_pos['K'][0]
    is_king_castling = game_state[start_row][start_col].lower() == 'k' and abs(end_col - start_col) == 2
    for enemy_fig in enemy_possible_moves:
        for enemy_move in enemy_fig[1]:
            if our_king == enemy_move:
                return False
            if is_king_castling and (enemy_move == (start_row, (end_col + start_col) // 2) or enemy_move == (start_row, start_col)):
                return False
    return True


def _only_possible_moves(start_pos, moves, game_state, move_history):

    # Return a list like: [((start pos),(move_0)),((start_pos),(move_1))]

    print("only possible moves " + str(moves))
    return [(start_pos, move) for move in moves if _move_is_possible((start_pos, move), game_state, move_history)]


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
            if row == 3 and (col - 1) >= 0 and game_state[row][col - 1] == 'p' and move_history[-1][0] == (row - 2, col - 1)\
                    and move_history[-1][1] == (row, col - 1):
                moves.append((row - 1, col - 1))
            # E4F3 if white last was pawn F2F4
            if row == 3 and (col + 1) < 8 and game_state[row][col + 1] == 'p' and move_history[-1][0] == (row - 2, col + 1)\
                    and move_history[-1][1] == (row, col + 1):
                moves.append((row - 1, col + 1))
            if _is_opposing(my_color, game_state[row - 1][col - 1]):
                moves.append((row - 1, col - 1))
        if col < 7 and _is_opposing(my_color, game_state[row - 1][col + 1]):
            moves.append((row - 1, col + 1))
    else:
        # E3E4
        if row + 1 <= 7 and game_state[row + 1][col] == '0':
            moves.append((row + 1, col))
        # E2E4
        if row == 1 and game_state[row + 2][col] == '0' and game_state[row + 1][col] == '0' and row + 2 <= 7:
            moves.append((row + 2, col))
        # E4D5
        if len(move_history) and row < 7:
            if row == 4 and (col - 1) >= 0 and game_state[row][col - 1] == 'P' and move_history[-1][0] == (row + 2, col - 1) \
                    and move_history[-1][1] == (row, col - 1):
                moves.append((row + 1, col - 1))
            # E4F5
            if row == 4 and (col + 1) < 8 and game_state[row][col + 1] == 'P' and move_history[-1][0] == (row + 2, col + 1) \
                    and move_history[-1][1] == (row, col + 1):
                moves.append((row + 1, col + 1))
            if _is_opposing(my_color, game_state[row + 1][col - 1]):
                moves.append((row + 1, col - 1))
        if row < 7 and col < 7 and _is_opposing(my_color, game_state[row + 1][col + 1]):
            moves.append((row + 1, col + 1))
        pass
    return moves


def _get_possible_castlings(king_pos, game_state, move_history):
    possible_moves = []
    king_row, king_col = king_pos
    if figure_moved(king_pos, move_history):
        return []
    rook_positions = [
        (0, 0), (0, 7)
    ] if game_state[king_row][king_col] == 'k' else [
        (7, 0), (7, 7)
    ]
    for (rook_row, rook_col) in rook_positions:
        if not figure_moved((rook_row, rook_col), move_history):
            start_col, end_col = min(rook_col, king_col), max(rook_col, king_col)
            if all([f == '0' for f in game_state[king_row][start_col + 1:end_col]]):
                possible_moves.append((king_row, (start_col + end_col) // 2))
    return possible_moves


def figure_moved(fig_pos, move_history):
    for (_, end_pos) in move_history:
        if end_pos == fig_pos:
            return True
    return False


def _get_king_moves(pos, game_state, move_history):
    my_color = 'b' if len(move_history) % 2 else 'w'
    row, col = pos
    possible_moves = [
            (row + 1, col - 1),
            (row + 1, col),
            (row + 1, col + 1),
            (row, col + 1),
            (row, col - 1),
            (row - 1, col + 1),
            (row - 1, col),
            (row - 1, col - 1)
    ]
    if my_color == 'b':
        l_rook_pos = (0, 0)
        s_rook_pos = (0, 7)
    else:
        l_rook_pos = (7, 0)
        s_rook_pos = (7, 7)
    return [
        (r, c) for (r, c) in possible_moves if 0 <= r < 8 and 0 <= c < 8 and not _is_mine(my_color, game_state[r][c])
    ] + _get_possible_castlings(pos, game_state, move_history)


def _get_bishop_moves(pos, game_state, move_history):
    my_color = 'b' if len(move_history) % 2 else 'w'
    (row, col) = pos
    moves = []
    # Upper right diagonal
    for tar_row, tar_col in zip(range(row - 1, row - 8, - 1), range(col + 1, col + 8)):
        if tar_row < 0 or tar_col > 7 or _is_mine(my_color, game_state[tar_row][tar_col]):
            break
        elif game_state[tar_row][tar_col] == '0':
            moves.append((tar_row, tar_col))
        elif _is_opposing(my_color, game_state[tar_row][tar_col]):
            moves.append((tar_row, tar_col))
            break

    # Lower right diagonal
    for tar_row, tar_col in zip(range(row + 1, row + 8), range(col + 1, col + 8)):
        if tar_row > 7 or tar_col > 7 or _is_mine(my_color, game_state[tar_row][tar_col]):
            break
        elif game_state[tar_row][tar_col] == '0':
            moves.append((tar_row, tar_col))
        elif _is_opposing(my_color, game_state[tar_row][tar_col]):
            moves.append((tar_row, tar_col))
            break

    # Upper left diagonal
    for tar_row, tar_col in zip(range(row - 1, row - 8, -1), range(col - 1, col - 8, -1)):
        if tar_row < 0 or tar_col < 0 or _is_mine(my_color, game_state[tar_row][tar_col]):
            break
        elif game_state[tar_row][tar_col] == '0':
            moves.append((tar_row, tar_col))
        elif _is_opposing(my_color, game_state[tar_row][tar_col]):
            moves.append((tar_row, tar_col))
            break

    # Lower left diagonal
    for tar_row, tar_col in zip(range(row + 1, row + 8), range(col - 1, col - 8, -1)):
        if tar_row > 7 or tar_col < 0 or _is_mine(my_color, game_state[tar_row][tar_col]):
            break
        elif game_state[tar_row][tar_col] == '0':
            moves.append((tar_row, tar_col))
        elif _is_opposing(my_color, game_state[tar_row][tar_col]):
            moves.append((tar_row, tar_col))
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


def _evaluate_available_moves(fig_pos, game_state, moves_history, evaluate_checks=True):
    fig, pos = fig_pos
    print(str(fig) + ' ' + str(pos))
    all_moves = _figure_evaluators[fig](pos, game_state, moves_history)
    if evaluate_checks:
        return _only_possible_moves(pos, all_moves, game_state, moves_history)
    return all_moves


def _get_available_moves(player_positions, game_state, moves_history, evaluate_checks=True):
    available_moves = []
    for fig, positions in player_positions.items():
        for pos in positions:
            available_moves.append(
                (pos,
                 _evaluate_available_moves((fig.lower(), pos), game_state, moves_history, evaluate_checks))
            )
    # Example available_moves = [((6, 0), [((6, 0), (5, 0)), ((6, 0), (4, 0))]), ..., ((),[]), ((),[])]
    return available_moves


def _get_available_moves_for_state(game_state, moves_history, evaluate_checks=True):
    print('MOVE HISTORY: ', str(moves_history))
    w_pos, b_pos = _get_figures_positions(game_state)
    player_positions, opponent_positions = (b_pos, w_pos) if len(moves_history) % 2 else (w_pos, b_pos)
    return _get_available_moves(player_positions, game_state, moves_history, evaluate_checks)


def to_standard_notation(moves_history):
    # TODO
    pass


def has_no_moves(my_moves):
    for fig_moves in my_moves.values():
        if len(fig_moves) != 0:
            return False
    return True


def check_draw(start_pos, end_pos, board_state):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if (board_state[start_row][start_col] != board_state[end_row][end_col]
            or board_state[start_row][start_col].lower() == 'p'):
        return False

def pawn_promotion_check(pos):
    r, c = pos
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
        self._transformation_handler = []
        self._promotion_fig = None
        self._board_state = initial_board_state
        _validate_moves_history(moves_history)
        self._moves_history = moves_history
        self._move_number = 0


    def get_available_moves(self):
        return dict(_get_available_moves_for_state(self._board_state, self._moves_history))

    def perform_move(self, start_pos, end_pos, fig=None):
        # TODO actually perform move and update state
        if fig is None:
            print("you want to move from " + str(start_pos) + " to " + str(end_pos))
            start_row, start_col = start_pos
            end_row, end_col = end_pos

            is_pawn_attack = self._board_state[start_row][start_col].lower() == 'p' and _is_pawn_attack(start_pos, end_pos)
            is_pawn_cut = is_pawn_attack and _is_empty_field(self._board_state[end_row][end_col])
            if is_pawn_cut:
                self._board_state[start_row][end_col] = '0'

            is_king_castling = self._board_state[start_row][start_col].lower() == 'k' and abs(end_col - start_col) == 2
            if is_king_castling:
                if end_col == 5:
                    self._board_state[start_row][4] = self._board_state[start_row][7]
                    self._board_state[start_row][7] = '0'
                elif end_col == 1:
                    self._board_state[start_row][2] = self._board_state[start_row][0]
                    self._board_state[start_row][0] = '0'

            self._board_state[end_row][end_col] = self._board_state[start_row][start_col]
            self._board_state[start_row][start_col] = '0'
            self._moves_history.append((start_pos, end_pos))

            new_available_moves = self.get_available_moves()

            if has_no_moves(new_available_moves):
                print("CHECKMATE" if _is_check else "STALLMATE")
            if check_draw(start_pos, end_pos, self._board_state):
                self._move_number += 1
                if self._move_number == 50:
                    print("DRAW")
            else:
                self._move_number = 0

            for handler in self._move_handlers:
                # b_view.update_state
                handler(self._board_state, self._moves_history, new_available_moves)

            if (end_row == 0 or end_row == 7) and self._board_state[end_row][end_col].lower() == 'p':
                for handler in self._transformation_handler:
                    handler(self._moves_history)
        else:
            print("MOVE HISTORY: ", self._moves_history)
            last_pos = self._moves_history[-1][-1]
            row_last_pos, col_last_pos = last_pos[0], last_pos[1]
            self._board_state[row_last_pos][col_last_pos] = fig
            for handler in self._move_handlers:
                # b_view.update_state
                handler(self._board_state, self._moves_history, self.get_available_moves())


    def add_transformation_handler(self, transformation_handler):
        self._transformation_handler.append(transformation_handler)

    def add_move_handler(self, move_handler):
        self._move_handlers.append(move_handler)