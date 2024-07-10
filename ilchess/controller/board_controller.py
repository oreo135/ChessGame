import copy
from ilchess.state import default_state
from collections import defaultdict


def _get_figures_positions(game_state):
    white_figures_pos = defaultdict(lambda: [])
    black_figures_pos = defaultdict(lambda: [])

    for row in range(0, 8):
        for col in range(0, 8):
            figure = game_state[row][col]
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
    for _, my_attacks in my_attacks:
        for my_attack in my_attacks:
            if my_attack == his_king_pos:
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
            if is_king_castling and (enemy_move == (start_row, (end_col + start_col) // 2)
                                     or enemy_move == (start_row, start_col)):
                return False
    return True


def _only_possible_moves(start_pos, moves, game_state, move_history):

    # Return a list like: [((start pos),(move_0)),((start_pos),(move_1))]

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
            if _is_opposing(my_color, game_state[row + 1][col - 1]) and col > 0:
                moves.append((row + 1, col - 1))
        if row < 7 and col < 7 and _is_opposing(my_color, game_state[row + 1][col + 1]):
            moves.append((row + 1, col + 1))

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
    w_pos, b_pos = _get_figures_positions(game_state)
    player_positions, opponent_positions = (b_pos, w_pos) if len(moves_history) % 2 else (w_pos, b_pos)
    return _get_available_moves(player_positions, game_state, moves_history, evaluate_checks)


def _check_remove_piece(move, state):
    start_pos, end_pos = move
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    if state[start_row][start_col] != state[end_row][end_col] and state[end_row][end_col] != '0':
        return True
    else:
        return False


def _check_pawn_promotion(end_pos, state):
    end_row, end_col = end_pos
    if (end_row == 0 or end_row == 7) and state[end_row][end_col].lower() == 'p':
        return True
    else:
        return False


def has_no_moves(my_moves):
    for fig_moves in my_moves.values():
        if len(fig_moves) != 0:
            return False
    return True


def _check_draw(start_pos, end_pos, board_state):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if (board_state[start_row][start_col] != board_state[end_row][end_col]
            or board_state[start_row][start_col].lower() == 'p'):
        return False


def _evaluate_move_from_portable_notation(move, game_state, move_history, color):
    labels = {'a': 7, 'b': 6, 'c': 5, 'd': 4, 'e': 3, 'f': 2, 'g': 1, 'h': 0}
    length = len(move_history)
    print(length)
    print('current move: ', move)
    commons_move = []
    fig = 'p' if move[0].islower() else move[0]
    fig = fig.lower() if color == 'w' else fig.upper()
    w_pos, b_pos = _get_figures_positions(game_state)
    player_positions = w_pos if color == 'w' else b_pos
    end_pos = (int(move[-1]) - 1, labels[move[-2]])
    for pos in player_positions[fig]:
        moves = _evaluate_available_moves((fig.lower(), pos), game_state, move_history)
        for shift in moves:
            if (pos, end_pos) == shift:
                commons_move.append((pos, end_pos))
    if len(commons_move) == 1:
        start_pos = commons_move[0][0]
    else:
        for next_symbol in move[0:3]:
            if next_symbol not in labels.keys() and not next_symbol.isdigit():
                continue
            elif next_symbol.isdigit():
                start_row = int(next_symbol) - 1
                start_col = None
            else:
                start_col = labels[next_symbol]
                start_row = None
            # for index, move_fig in enumerate(commons_move[:]):
            #     if (start_row is not None) and move_fig[0][0] != start_row:
            #         commons_move.pop(index)
            #     if (start_col is not None) and (move_fig[0][1] != start_col):
            #         commons_move.pop(index)
            commons_move = [move_fig for move_fig in commons_move if
                            (start_row is None or move_fig[0][0] == start_row) and
                            (start_col is None or move_fig[0][1] == start_col)]
            if len(commons_move) == 1:
                break
        start_pos = commons_move[0][0]
    return start_pos, end_pos


def validate_moves_history(portable_moves_history):
    # translation from normal notation to algebraic,
    # where each move is in an array portable_moves_history
    portable_moves_history = portable_moves_history.split()
    moves = [move for index, move in enumerate(portable_moves_history[:-1]) if index % 3 != 0]
    algebraic_notation = []
    game_state = copy.deepcopy(default_state)
    pawn_promotion = {}

    for index, port_move in enumerate(moves):
        fig = ''
        color = 'w' if index % 2 == 0 else 'b'
        if any(char in port_move for char in {'+', '#'}):
            port_move = port_move.rstrip('+#')
        if '=' in port_move:
            fig = port_move[-1].upper() if color == 'b' else port_move[-1].lower()
            pawn_promotion[index + 1] = fig
            port_move = port_move.split('=')[0]
        if index % 2 == 0:
            if port_move == 'O-O':
                game_state[0][2], game_state[0][1] = game_state[0][0], game_state[0][3]
                game_state[0][3], game_state[0][0] = '0', '0'
                algebraic_notation.append(((0, 3), (0, 1)))
                continue
            elif port_move == 'O-O-O':
                game_state[0][5], game_state[0][4] = game_state[0][3], game_state[0][7]
                game_state[0][3], game_state[0][7] = '0', '0'
                algebraic_notation.append(((0, 3), (0, 5)))
                continue
            algebraic_move = _evaluate_move_from_portable_notation(port_move,
                                                                   game_state,
                                                                   algebraic_notation,
                                                                   color)
        else:
            if port_move == 'O-O':
                game_state[7][1], game_state[7][2] = game_state[7][3], game_state[7][0]
                game_state[7][3], game_state[7][0] = '0', '0'
                algebraic_notation.append(((7, 3), (7, 1)))
                continue
            elif port_move == 'O-O-O':
                game_state[7][5], game_state[7][4] = game_state[7][3], game_state[7][7]
                game_state[7][3], game_state[7][7] = '0', '0'
                algebraic_notation.append(((7, 3), (7, 5)))
                continue
            algebraic_move = _evaluate_move_from_portable_notation(port_move,
                                                                   game_state,
                                                                   algebraic_notation,
                                                                   color)
        algebraic_notation.append(algebraic_move)
        start_pos, end_pos = algebraic_move[0], algebraic_move[1]
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        is_pawn_attack = game_state[start_row][start_col].lower() == 'p' and _is_pawn_attack(start_pos, end_pos)
        is_pawn_cut = is_pawn_attack and _is_empty_field(game_state[end_row][end_col])
        if is_pawn_cut:
            game_state[start_row][end_col] = '0'
        if fig:
            game_state[end_row][end_col] = fig
        else:
            game_state[end_row][end_col] = game_state[start_row][start_col]
        game_state[start_row][start_col] = '0'
    print(algebraic_notation)
    print('length algebraic notation: ', len(algebraic_notation))
    return algebraic_notation, pawn_promotion


def _event_check(index, start_pos, end_pos, board_state, move_history, draw_move_50, draw_move_3, check_promo=True):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    is_king_castling = board_state[start_row][start_col].lower() == 'k' and abs(end_col - start_col) == 2
    current_moves_history = move_history[:]
    _check = False
    event = ''
    if is_king_castling:
        if end_col == 5:
            board_state[start_row][5] = board_state[start_row][3]
            board_state[start_row][4] = board_state[start_row][7]
            board_state[start_row][3], board_state[start_row][7] = '0', '0'
            event = 'O-O-O'
        elif end_col == 1:
            board_state[start_row][1] = board_state[start_row][3]
            board_state[start_row][2] = board_state[start_row][0]
            board_state[start_row][0], board_state[start_row][3] = '0', '0'
            event = 'O-O'
    if check_promo and not is_king_castling:
        board_state[end_row][end_col] = board_state[start_row][start_col]
        board_state[start_row][start_col] = '0'

    new_available_moves = dict(_get_available_moves_for_state(board_state, current_moves_history))
    w_pos, b_pos = _get_figures_positions(board_state)

    if _is_check(board_state, current_moves_history):
        event += '+'
        _check = True
    if len(w_pos) == 1 and len(b_pos) == 1:
        event = '1/2-1/2'
    # Function to checks events
    if has_no_moves(new_available_moves):
        if _check:
            print("CHECKMATE")
            if event in {'O-O', 'O-O-O'}:
                event += '#'
            else:
                event = '#'
        else:
            print("STALEMATE")
            event = '1/2-1/2'
    if _check_draw(start_pos, end_pos, board_state):
        draw_move_50 += 1
        if draw_move_50 == 50:
            print("DRAW")
            event = '1/2-1/2'
    else:
        draw_move_50 = 0
    if len(move_history) > 4 and (index + 5) <= len(move_history):
        if move_history[index] == move_history[index + 4]:
            last_b_fig_pos = move_history[index + 2][1]
            last_w_fig_pos = move_history[index + 1][0]
            if len(move_history) % 2:
                b_fig_pos = move_history[index + 4][1]
                w_fig_pos = move_history[index + 5][0]
                if w_fig_pos == last_w_fig_pos or b_fig_pos == last_b_fig_pos:
                    event = '1/2-1/2'
        else:
            draw_move_3 = 0
    return board_state, event, draw_move_3, draw_move_50, new_available_moves


def treatment(standard_notation):
    result = []
    first = ''
    count = 1
    for index, move in enumerate(standard_notation):
        if (index + 1) % 2:
            first = f'{count}. {move}'
            count += 1
        else:
            first += ' ' + move
            result.append(first)
            first = ''
    if first:
        result.append(first)
    return result


def to_standard_notation(moves_history, pawn_promotion):
    current_state = copy.deepcopy(default_state)
    next_state = copy.deepcopy(default_state)
    standard_notation = []
    top_labels = ["a", "b", "c", "d", "e", "f", "g", "h"][::-1]
    count_promo = 1
    current_move_history = []
    draw_move_50 = 0
    draw_move_3 = 0

    for index, (start_pos, end_pos) in enumerate(moves_history):
        end_row, end_col = end_pos
        start_row, start_col = start_pos
        fig = current_state[start_row][start_col]
        color = 'w' if index % 2 == 0 else 'b'
        commons_moves_algebraic = []
        w_pos, b_pos = _get_figures_positions(current_state)
        player_positions = w_pos if color == 'w' else b_pos
        move_in_standard = ''
        check_promo = True
        print('number_move:', index)
        is_pawn_attack = current_state[start_row][start_col].lower() == 'p' and _is_pawn_attack(start_pos, end_pos)
        is_pawn_cut = is_pawn_attack and _is_empty_field(current_state[end_row][end_col])
        if (end_row == 7 or end_row == 0) and fig.lower() == 'p':
            if current_state[end_row][end_col] != '0':
                move_in_standard = f'{top_labels[start_col]}x{top_labels[end_col]}{end_row + 1}'
                current_state[end_row][end_col] = pawn_promotion[index + 1]
                current_state[start_row][start_col] = '0'
                check_promo = False
            else:
                move_in_standard = f'{top_labels[start_col]}{end_row + 1}'
                current_state[end_row][end_col] = pawn_promotion[index + 1]
                current_state[start_row][start_col] = '0'
                check_promo = False
        if is_pawn_cut:
            move_in_standard = f'{top_labels[start_col]}x{top_labels[end_col]}{end_row + 1}'
            current_state[start_row][end_col] = '0'
        if not move_in_standard:
            for pos in player_positions[fig]:
                moves = _evaluate_available_moves((fig.lower(), pos), current_state, current_move_history)
                for move in moves:
                    if end_pos == move[1] and move[0] != start_pos:  # only the end position is needed move[1]
                        commons_moves_algebraic.append(move[0])
            if current_state[end_row][end_col] == '0':
                if len(commons_moves_algebraic) == 0:
                    move_in_standard = f'{top_labels[end_col]}{end_row + 1}'
                else:
                    check_row, check_col = False, False
                    for row, col in commons_moves_algebraic:
                        if row == start_row:
                            check_row = True
                        if col == start_col:
                            check_col = True
                    if check_row and not check_col:
                        move_in_standard = f'{top_labels[start_col]}{top_labels[end_col]}{end_row + 1}'
                    elif not check_row and check_col:
                        move_in_standard = f'{top_labels[start_col]}{start_row + 1}{top_labels[end_col]}{end_row + 1}'
                    elif not check_row and not check_col and len(commons_moves_algebraic) > 0:
                        move_in_standard = f'{top_labels[start_col]}{top_labels[end_col]}{end_row + 1}'
                    else:
                        move_in_standard = (f'{top_labels[start_col]}'
                                            f'{start_row + 1}{top_labels[end_col]}{end_row + 1}')
            else:
                if len(commons_moves_algebraic) == 0 and fig.lower() != 'p':
                    move_in_standard = f'x{top_labels[end_col]}{end_row + 1}'
                elif len(commons_moves_algebraic) == 0 and fig.lower() == 'p':
                    move_in_standard = f'{top_labels[start_col]}x{top_labels[end_col]}{end_row + 1}'
                else:
                    check_row, check_col = False, False
                    for row, col in commons_moves_algebraic:
                        if row == start_row:
                            check_row = True
                        if col == start_col:
                            check_col = True
                    if check_row and not check_col:
                        move_in_standard = f'{top_labels[start_col]}x{top_labels[end_col]}{end_row + 1}'
                    elif not check_row and check_col:
                        move_in_standard = f'{start_row + 1}{top_labels[end_col]}x{end_row + 1}'
                    elif not check_row and not check_col and len(commons_moves_algebraic) >= 1:
                        move_in_standard = f'{top_labels[start_col]}x{top_labels[end_col]}{end_row + 1}'
                    else:
                        move_in_standard = (f'{top_labels[start_col]}'
                                            f'{start_row + 1}x{top_labels[end_col]}{end_row + 1}')

        current_move_history.append((start_pos, end_pos))
        current_state, event, draw_move_3, draw_move_50, new_available_moves = _event_check(index,
                                                                                            start_pos,
                                                                                            end_pos,
                                                                                            current_state,
                                                                                            current_move_history,
                                                                                            draw_move_50,
                                                                                            draw_move_3,
                                                                                            check_promo)

        if event in {'O-O', 'O-O-O'}:
            move_in_standard = event
        else:
            if (index + 1) in pawn_promotion:
                fig = f'={pawn_promotion[index + 1].upper()}'
                move_in_standard = move_in_standard + fig + event
            elif fig.lower() != 'p' and not any(x in event for x in {'O-O', '1/2'}):
                move_in_standard = fig.upper() + move_in_standard + event
            elif fig.lower() != 'p' and '1/2' in event and color == 'w':
                move_in_standard = fig.upper() + move_in_standard + ' ' + '1/2'
            elif fig.lower() != 'p' and '1/2' in event and color == 'b':
                move_in_standard = fig.upper() + move_in_standard
            elif 'O-O' in event:
                move_in_standard = event
            else:
                move_in_standard += event
        print('move_in_standard', move_in_standard)
        standard_notation.append(move_in_standard)
    print('standard_notation:', standard_notation)
    return standard_notation


class BoardController(object):
    """
    BoardController class handles game state. It does following:
    * evaluates available moves based on players position
    * evaluates checkmate, stalemate, etc.
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
        self._pawn_promotion = {}
        self._board_state = initial_board_state
        self._moves_history = moves_history
        self._move_number_50 = 0
        self._move_number_3 = 0
        self.trans_fig_number = 1
        self._copy_default_state = copy.deepcopy(default_state)
        self._count_move = 0
        self._check_event = {}
        self._standard_notation = []

    def get_available_moves(self):
        return dict(_get_available_moves_for_state(self._board_state, self._moves_history))

    def perform_move(self, start_pos, end_pos, fig=None):
        if fig is None:
            _check = False
            self._count_move += 1
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
                    self._check_event[self._count_move] = 'O-O-O'
                elif end_col == 1:
                    self._board_state[start_row][2] = self._board_state[start_row][0]
                    self._board_state[start_row][0] = '0'
                    self._check_event[self._count_move] = 'O-O'

            self._board_state[end_row][end_col] = self._board_state[start_row][start_col]
            self._board_state[start_row][start_col] = '0'
            self._moves_history.append((start_pos, end_pos))

            new_available_moves = self.get_available_moves()

            if _is_check(self._board_state, self._moves_history):
                self._check_event[self._count_move] = '+'
                _check = True

            if has_no_moves(new_available_moves):
                if _check:
                    print("CHECKMATE")
                    self._check_event[self._count_move] = '#'
                else:
                    print("STALEMATE")
                    self._check_event[self._count_move] = '1/2-1/2'

            if _check_draw(start_pos, end_pos, self._board_state):
                self._move_number_50 += 1
                if self._move_number_50 == 50:
                    print("DRAW")
                    self._check_event[self._count_move] = '1/2-1/2'
                elif len(self._moves_history) > 4:
                    if self._moves_history[0] == self._moves_history[2] and \
                            self._moves_history[1] == self._moves_history[3]:
                        self._move_number_3 += 1
                        if self._move_number_3 == 3:
                            print('DRAW')
                            self._check_event[self._count_move] = '1/2-1/2'
                    else:
                        self._move_number_3 = 0
            else:
                self._move_number_50 = 0

            for handler in self._move_handlers:
                # b_view.update_state
                handler(self._board_state, self._moves_history, new_available_moves)

            if _check_pawn_promotion(end_pos, self._board_state):
                for handler in self._transformation_handler:
                    handler(self._moves_history)
        else:
            last_pos = self._moves_history[-1][-1]
            row_last_pos, col_last_pos = last_pos[0], last_pos[1]
            self._board_state[row_last_pos][col_last_pos] = fig
            self._pawn_promotion[self._count_move] = fig
            self.trans_fig_number += 1
            self._check_event[self._count_move] = fig
            for handler in self._move_handlers:
                # b_view.update_state
                handler(self._board_state, self._moves_history, self.get_available_moves())
        print('move_history', self._moves_history)

    def write_moves_history(self):
        standard_notation = to_standard_notation(self._moves_history, self._pawn_promotion)
        with open('history.txt', 'w') as f:
            f.write(str(standard_notation))

    def add_transformation_handler(self, transformation_handler):
        self._transformation_handler.append(transformation_handler)

    def add_move_handler(self, move_handler):
        self._move_handlers.append(move_handler)