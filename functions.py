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
            key: int(value)
            for key, value in players[section].items()
        }
    saves = ConfigParser()
    saves.read(saves_file, encoding='utf-8')
    for section in saves.sections():
        player = tuple(section.split(';'))
        turn = [i for i in saves[section]['turns'].split(',')]
        SAVES[player] = turn




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
        saves[section]['turns'] = ','.join([i for i in SAVES[save]])
    with open(saves_file, 'w', encoding='utf-8') as ini_file:
        saves.write(ini_file)



def draw_board(align_right: bool = False) -> str:
    """Формирует и возвращает строку, содержащую псевдографическое изображение игрового поля со сделанными ходами."""
    max_width = len(max(BOARD, key=lambda elem: len(elem)))

    h_line = '—' * (DIM * (max_width + 2) ) + '\n'
    result = ''
    if align_right:
        align = get_terminal_size()[0] - 2
    else:
        align = len(h_line)
    for i in RANGE:
        row = ' | '.join(BOARD[i * DIM: (i + 1) * DIM])
        result += f"{row.rjust(align)}\n"
        if i != (DIM - 1):
            result += h_line.rjust(align + 1)

    return result

print(write_ini())
print(load_ini())
print(draw_board(False))



