"""Дополнительный модуль: вспомогательные функции."""

from configparser import ConfigParser

from data import STATS, SAVES, DIM, RANGE, BOARD
from shutil import get_terminal_size

players_file = 'players.ini'
saves_file = 'saves.ini'


def load_ini() -> bool:
    """Читает данные из ini-файла в глобальную переменную данных."""
    players = ConfigParser()
    players.read(players_file, encoding='utf-8')
    for section in players.sections():
        STATS[section] = {
            # ИСПРАВИТЬ: не все значения являются числами
            key: value
            for key, value in players[section].items()
        }
    saves = ConfigParser()
    saves.read(saves_file, encoding='utf-8')
    for section in saves.sections():
        players = tuple(section.split(';'))
        # ИСПРАВИТЬ: а здесь все значения как раз являются числами и необходимо преобразование
        turn = [i for i in saves[section]['turns'].split(',')]
        SAVES[players] = turn
    if STATS:
        return False
    else:
        return True


def write_ini() -> None:
    """Записывает данные из глобальной переменной данных в ini-файл."""
    config = ConfigParser()
    config.read_dict(STATS)
    with open(players_file, 'w', encoding='utf-8') as ini_file:
        config.write(ini_file)
    saves = ConfigParser()
    for save in SAVES:
        player_a, player_b = list(save)
        section = f"{player_a};{player_b}"
        # ИСПРАВИТЬ: метод join() принимает на вход последовательности, содержащие только строки, поэтому необходимо обратное преобразование в строку для каждого элемента
        saves[section]['turns'] = ','.join([i for i in SAVES[save]])
    with open(saves_file, 'w', encoding='utf-8') as ini_file:
        saves.write(ini_file)


def draw_board(align_right: bool = False) -> str:
    """Формирует и возвращает строку, содержащую псевдографическое изображение игрового поля со сделанными ходами."""
    max_width = len(max(BOARD, key=lambda elem: len(elem)))
    # КОММЕНТАРИЙ: при такой длине горизонтального разделителя у крайних ячеек не будет внешнего отступа от предполагаемого края
    h_line = '—'*(DIM*(max_width + 2)) + '\n'
    result = ''
    if align_right:
        align = get_terminal_size()[0] - 2
    else:
        align = len(h_line)
    for i in RANGE:
        # КОММЕНТАРИЙ: максимальная ширина ячейки вычисляется для того, чтобы ячейки нашего поля были одинаковой ширины и могли вместить не только односимвольные значения (см. тест ниже)
        row = ' | '.join(BOARD[i*DIM:(i+1)*DIM])
        result += f"{row.rjust(align)}\n"
        if i != DIM - 1:
            result += h_line.rjust(align + 1)
    return result


# ИСПОЛЬЗОВАТЬ: все тесты отдельных модулей убираются под проверку импорта
if __name__ == '__main__':
    # print(load_ini())
    # print(write_ini())
    DIM = 5
    RANGE = range(DIM)
    BOARD = [str(i) for i in range(1, 26)]
    print(draw_board(False))


#     1 | 2 | 3 | 4 | 5
#  ————————————————————
#    6 | 7 | 8 | 9 | 10
#  ————————————————————
# 11 | 12 | 13 | 14 | 15
#  ————————————————————
# 16 | 17 | 18 | 19 | 20
#  ————————————————————
# 21 | 22 | 23 | 24 | 25
