a = ('1. e4 e6 2. d4 b6 3. a3 Bb7 4. Nc3 Nh6 5. Bxh6 gxh6 6. Be2 Qg5 7. '
     'Bg4 h5 8. Nf3 Qg6 9. Nh4 Qg5 10. Bxh5 Qxh4 11. Qf3 Kd8 12. Qxf7 Nc6 13. Qe8# 1-0')


def _from_standard_notation(portable_notation):
    # TODO should return (game_state, moves_history)
    portable_notation = portable_notation.split()[:-1]
    print(portable_notation)
    moves = [move for index, move in enumerate(portable_notation) if index % 3 != 0]
    return moves


print(_from_standard_notation(a))

""" is_king_castling = self._board_state[start_row][start_col].lower() == 'k' and abs(end_col - start_col) == 2
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

            # TODO need to make one function to checks events
            if has_no_moves(new_available_moves):
                if _check:
                    print("CHECKMATE")
                    self._check_event[self._count_move] = '#'
                else:
                    print("STALEMATE")
                    self._check_event[self._count_move] = '1/2-1/2'

            if _check_draw(start_pos, end_pos, self._board_state):
                self._move_number += 1
                if self._move_number == 50:
                    print("DRAW")
                    self._check_event[self._count_move] = '1/2-1/2'
            else:
                self._move_number = 0"""


"""    def to_standard_notation(self, moves_history):
        start_state = copy.deepcopy(self._copy_default_state)
        end_state = copy.deepcopy(start_state)
        standard_notation = []
        top_labels = ["a", "b", "c", "d", "e", "f", "g", "h"][::-1]
        number = 0

        current_move_history = []

        for count, move in enumerate(moves_history):
            print(count, move)
            start_pos, end_pos = move
            start_row, start_col = start_pos
            end_row, end_col = end_pos
            end_state[end_row][end_col] = end_state[start_row][start_col]
            end_state[start_row][start_col] = '0'
            available_moves = dict(_get_available_moves_for_state(start_state, current_move_history))
            current_move_history.append(move)
            print("available_moves", available_moves)
            event = self._check_event.setdefault(count + 1)

            if _check_remove_piece(move, start_state):
                if end_state[start_row][start_col].lower() != 'p':
                    if start_state[start_row][start_col].lower() == 'n':
                        attribute = _identical_move_two_fig(available_moves,
                                                            current_move_history,
                                                            start_state,
                                                            move)
                        if attribute == 'col':
                            move_in_notation = (f'{end_state[end_row][end_col].upper()}{top_labels[start_col]}x'
                                                f'{top_labels[end_col]}{end_row + 1}')
                        elif attribute == 'row':
                            move_in_notation = (f'{end_state[end_row][end_col].upper()}{start_row + 1}x'
                                                f'{top_labels[end_col]}{end_row + 1}')
                        elif attribute:
                            move_in_notation = (f'{end_state[end_row][end_col].upper}{top_labels[start_col]}'
                                                f'{top_labels[end_col]}{end_row + 1}')
                        else:
                            move_in_notation = (f'{end_state[end_row][end_col].upper()}x'
                                                f'{top_labels[end_col]}{end_row + 1}')
                    elif start_state[start_row][start_col].lower() == 'r':
                        attribute = _identical_move_two_fig(available_moves,
                                                            current_move_history,
                                                            start_state,
                                                            move)
                        if attribute == 'col':
                            move_in_notation = (f'{end_state[end_row][end_col].upper()}{top_labels[start_col]}x'
                                                f'{top_labels[end_col]}{end_row + 1}')
                        elif attribute == 'row':
                            move_in_notation = (f'{end_state[end_row][end_col].upper()}{start_row + 1}x'
                                                f'{top_labels[end_col]}{end_row + 1}')
                        elif attribute:
                            move_in_notation = (f'{end_state[end_row][end_col].upper}{top_labels[start_col]}'
                                                f'{top_labels[end_col]}{end_row + 1}')
                        else:
                            move_in_notation = (f'{end_state[end_row][end_col].upper()}x'
                                                f'{top_labels[end_col]}{end_row + 1}')
                    else:
                        move_in_notation = (f'{top_labels[start_col]}x'
                                            f'{top_labels[end_col]}{end_row + 1}')

                else:
                    move_in_notation = f'ex{top_labels[end_col]}{end_row + 1}'
            else:
                if end_state[end_row][end_col].lower() != 'p':
                    if start_state[start_row][start_col].lower() == 'n':
                        attribute = _identical_move_two_fig(available_moves,
                                                            current_move_history,
                                                            start_state,
                                                            move)
                        if attribute == 'col':
                            move_in_notation = (f'{end_state[end_row][end_col].upper()}{top_labels[start_col]}'
                                                f'{top_labels[end_col]}{end_row + 1}')
                        elif attribute == 'row':
                            move_in_notation = (f'{end_state[end_row][end_col].upper()}{start_row + 1}'
                                                f'{top_labels[end_col]}{end_row + 1}')
                        else:
                            move_in_notation = (f'{end_state[end_row][end_col].upper()}{top_labels[start_col]}'
                                                f'{top_labels[end_col]}{end_row + 1}')
                    elif start_state[start_row][start_col].lower() == 'r':
                        attribute = _identical_move_two_fig(available_moves,
                                                            current_move_history,
                                                            start_state,
                                                            move)
                        if attribute == 'col':
                            move_in_notation = (f'{end_state[end_row][end_col].upper()}{top_labels[start_col]}x'
                                                f'{top_labels[end_col]}{end_row + 1}')
                        elif attribute == 'row':
                            move_in_notation = (f'{end_state[end_row][end_col].upper()}{start_row + 1}x'
                                                f'{top_labels[end_col]}{end_row + 1}')
                        else:
                            move_in_notation = (f'{end_state[end_row][end_col].upper()}x'
                                                f'{top_labels[end_col]}{end_row + 1}')

                    else:
                        move_in_notation = (f'{end_state[end_row][end_col].upper()}'
                                            f'{top_labels[end_col]}{end_row + 1}')
                else:
                    move_in_notation = f'{top_labels[end_col]}{end_row + 1}'
            if event in {'+', '#', '=Q', '=B', '=N', '=R', '1/2-1/2', '=Q+'}:
                move_in_notation += event
            elif event in {'O-O-O', 'O-O'}:
                move_in_notation = event
                print('move_in_notation = ', move_in_notation)"""




"""a = '1. Nf3 Nf6 2. Nc3 Nc6 3. Ng5 b5 4. Nge4'
        # print('_validate_moves_history', _validate_moves_history(a))"""


"""def _identical_move_two_fig(available_moves, move_history, start_state, move):
    color = 'w' if len(move_history) % 2 else 'b'
    w_pos, b_pos = _get_figures_positions(start_state)
    start_pos, end_pos = move
    start_row, end_row = start_pos
    fig = start_state[start_row][end_row].lower()
    if fig == 'n':
        one_knight, two_knight = w_pos['n'] if color == 'w' else b_pos['N']
        if ((one_knight, end_pos) in available_moves[one_knight]) and ((two_knight, end_pos) in
                                                                       available_moves[two_knight]):
            if one_knight[0] == two_knight[0]:
                return 'col'
            elif one_knight[1] == two_knight[1]:
                return 'row'
            else:
                return True
        else:
            return False
    elif fig == 'r':
        one_rook, two_rook = w_pos['r'] if color == 'w' else b_pos['R']
        if (end_pos in available_moves[one_rook]) and (end_pos in available_moves[two_rook]):
            if one_rook[0] == two_rook[0]:
                return 'col'
            else:
                return 'row'
        else:
            return False
"""