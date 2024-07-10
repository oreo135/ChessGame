from unittest import TestCase, main
from ilchess.controller.board_controller import validate_moves_history, to_standard_notation, treatment

path = '/home/vladi/Downloads/lichess_db_standard_rated_2013-01.pgn'


def read_chess_moves(filename, max_lines=1000):
    history_matches = []

    with open(filename, 'r') as file:
        for _ in range(max_lines):
            line = file.readline()
            if '[' in line or line == '\n':
                continue
            print(line.strip())
            history_matches.append(line.strip())
    return history_matches


test_kit = read_chess_moves(path, 10000)


class ControllerTest(TestCase):
    def setUp(self):
        self.maxDiff = None

    @staticmethod
    def generate_test(match_moves, ind):
        def tests(self):
            print(f'Test for index {ind}')
            print('current_game_moves', match_moves)
            algebraic_notation, pawn_promotion = validate_moves_history(match_moves)
            print('algebraic', algebraic_notation)
            standard_notation = treatment(to_standard_notation(algebraic_notation, pawn_promotion))
            print('standard_notation', standard_notation)
            history = match_moves.split()
            if len(history) % 3 == 0:
                expected_moves = treatment([move for count, move in enumerate(history) if count % 3 != 0])
                expected_moves[-1] = expected_moves[-1][:-4]
            else:
                expected_moves = treatment([move for count, move in enumerate(history) if count % 3 != 0])
            print('expected_moves', expected_moves)
            for my_move, standard_move in zip(standard_notation, expected_moves):
                print(my_move, standard_move)
                self.assertEqual(my_move, standard_move, f'my_move {my_move} st_move{standard_move}')
        return tests


# for index, game_moves in enumerate(test_kit):
#     print('number_test', index)
#     print('game_moves', game_moves)
#     test_name = f'test_game_moves_{index}'
#     test = ControllerTest.generate_test(game_moves, index)
#     setattr(ControllerTest, test_name, test)


one_game_match = ('1. e4 d5 2. exd5 Qxd5 3. c4 Qd8 4. Nc3 e6 5. Nf3 Bb4 6. d4 Be7 7. d5 exd5 8. cxd5 Nf6 9'
                  '. Qa4+ Bd7 10. Bb5 Bxb5 11. Qxb5+ c6 12. dxc6 Nxc6 13. Ne5 O-O 14. Nxc6 bxc6 15. Qxc6 Rc8 '
                  '16. Qf3 Re8 17. O-O Bb4 18. Rd1 Qc7 19. Bf4 Qc5 20. Rac1 Qf8 21. Nd5 Nxd5 22. Qxd5 Rxc1 '
                  '23. Rxc1 Re1+ 24. Rxe1 Bxe1 25. Bd2 Bxd2 26. Qxd2 Qb8 27. h3 h6 28. b3 Qb6 29. Qd3 Qa5 '
                  '30. a4 Qe1+ 31. Kh2 Qe5+ 32. g3 Qb2 33. Kg2 Qf6 34. Qe3 Qa6 35. h4 Qb7+ 36. Qf3 Qb6 '
                  '37. Qe3 Qb7+ 38. f3 Qd7 39. g4 Qc7 40. g5 hxg5 41. hxg5 Qc2+ 42. Kg3 Qc7+ 43. f4 g6 '
                  '44. Kf3 Qb7+ 45. Kg4 Qd7+ 46. Kg3 Qb7 47. Qd3 Qb6 48. Qf3 Qg1+ 49. Qg2 Qe3+ 50. Kg4 Qxb3 '
                  '51. Qa8+ Kg7 52. Qxa7 Qe6+ 53. Kf3 Qd5+ 54. Ke3 Qe6+ 55. Kd3 Qf5+ 56. Ke3 Qh3+ 57. Ke4 Qf5+ '
                  '58. Ke3 Qh3+ 59. Kd4 Qf5 60. Ke3 1/2-1/2')
test1 = ControllerTest.generate_test(one_game_match, 1)
setattr(ControllerTest, 'test_my_games', test1)
if __name__ == '__main__':
    main()
