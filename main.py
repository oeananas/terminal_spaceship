import time
import curses
import asyncio
import random
from tools import (
    read_controls,
    get_frame_size,
    get_board_size
)
from animation import (
    blink,
    fire,
    spaceship
)

TIC_TIMEOUT = 0.1


def get_readed_files():
    """Return dict of readed files strings"""
    rocket_1 = ''
    rocket_2 = ''

    with open('./img/rocket_1.txt', 'r') as rocket_1_file:
        rocket_1 = rocket_1_file.read()
    with open('./img/rocket_2.txt', 'r') as rocket_2_file:
        rocket_2 = rocket_2_file.read()

    return {
        'rocket_1': rocket_1,
        'rocket_2': rocket_2
    }


def get_stars(canvas):
    """Return list of stars courutines"""
    board_rows, board_columns = get_board_size(canvas)
    cors = []
    for _ in range(100):
        cor = blink(
            canvas,
            random.randint(1, board_rows),
            random.randint(1, board_columns),
            random.choice('+*.:')
        )
        cors.append(cor)
    return cors


def get_spaceship(canvas, x, y):
    """Return spaceship courutine"""
    files = get_readed_files()

    rocket_1 = files.get('rocket_1')
    rocket_2 = files.get('rocket_2')

    return spaceship(canvas, x, y, rocket_1, rocket_2)


def draw(canvas):
    """Use courutines for drawing in terminal"""
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)

    coroutines = get_stars(canvas)

    board_rows, board_columns = get_board_size(canvas)
    spaceship_coord_x, spaceship_coord_y = board_rows // 2, board_columns // 2

    coroutines.append(get_spaceship(
        canvas, spaceship_coord_x, spaceship_coord_y))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
