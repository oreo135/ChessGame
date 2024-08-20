from unittest import TestCase, main
from ilchess.controller.board_controller import validate_moves_history, to_standard_notation, treatment

path = '/home/vladi/Downloads/lichess_db_standard_rated_2013-01.pgn'


def read_chess_moves(filename, max_lines=1000):
    history_matches = []
    way = []
    with open(filename, 'r') as file:
        for _ in range(max_lines):
            line = file.readline()
            if '[Termination' in line:
                lst = list(line.split())
                way.append(lst[1])
            if '[' in line or line == '\n':
                continue
            print(line.strip())
            history_matches.append(line.strip())
    return history_matches, way


test_kit, ways = read_chess_moves(path, 100000)
print('ways', ways)

class ControllerTest(TestCase):
    def setUp(self):
        self.maxDiff = None

    @staticmethod
    def generate_test(match_moves, ind):
        def tests(self):
            print(f'Test for index {ind}')
            print('current_game_moves', match_moves)
            algebraic_notation, pawn_promotion, exodus = validate_moves_history(match_moves)
            standard_notation = treatment(to_standard_notation(algebraic_notation, pawn_promotion, exodus))
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

for index, game_moves in enumerate(test_kit):
    print('number_test', index)
    print('game_moves', game_moves)
    test_name = f'test_game_moves_{index}'
    test = ControllerTest.generate_test(game_moves, index)
    setattr(ControllerTest, test_name, test)

# one_game_match = ('1. d4 d5 2. c4 e6 3. Nf3 Bb4+ 4. Bd2 Bxd2+ 5. Qxd2 dxc4 6. e4 Nf6 7. e5 Nd5 8. Bxc4 c6 9. O-O O-O 10. a3 b5 11. Bd3 Bb7 12. Ng5 Nd7 13. Bxh7+ Kh8 14. Qd3 Qxg5 15. Qh3 Qh6 16. Qxh6 gxh6 17. Bc2 a5 18. f4 Ne3 19. Rf2 Nxc2 20. Rxc2 Nb6 21. Rc3 Nc4 22. Rh3 Kh7 23. b3 Nb6 24. Nc3 Nd5 25. Ne4 Nxf4 26. Nf6+ Kg7 27. Rg3+ Kh8 28. Rf1 Ne2+ 29. Kh1 Nxg3+ 30. hxg3 Rg8 31. Kh2 Rad8 32. Rf4 Rd5 33. Nxg8 Kxg8 34. Rf6 Kg7 35. Rf4 a4 36. b4 Rd8 37. Kh3 Rg8 38. Kh4 Kf8 39. Kh5 Rxg3 40. Kxh6 Rxg2 41. Kh5 Rg3 42. Rh4 Rxa3 43. Kg5 Rb3 44. Kf6 Rf3+ 45. Kg5 a3 46. Kg4 Rf2 47. Kg3 Rf1 48. Rh2 Ke7 49. Ra2 Rd1 50. Rxa3 Rxd4 51. Ra7 Rd7 52. Kf4 Rd4+ 53. Ke3 Rd7 54. Ke4 Bc8 55. Ra8 Rc7 56. Rb8 Bd7 57. Rb6 c5 58. bxc5 Rxc5 59. Kd4 Rc4+ 60. Kd3 Rc5 61. Kd4 Rd5+ 62. Ke4 f5+ 63. exf6+ Kxf6 64. Rb7 Re5+ 65. Kd4 Rd5+ 66. Ke3 Bc6 67. Rh7 Rf5 68. Rh6+ Ke5 69. Rh2 Bd5 70. Re2 Bc4 71. Re1 Kd6 72. Rd1+ Rd5 73. Rb1 e5 74. Rc1 Rd4 0-1')
# test1 = ControllerTest.generate_test(one_game_match, 1)
# setattr(ControllerTest, 'test_my_games', test1)

if __name__ == '__main__':
    main()
