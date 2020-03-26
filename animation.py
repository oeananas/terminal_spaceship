import asyncio
import curses
import random
from tools import (
    draw_frame,
    read_controls,
    get_frame_size,
    get_board_size
)


async def blink(canvas, row, column, symbol='*'):
    """Star blink animation"""
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(random.randint(1, 10)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(random.randint(1, 10)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(random.randint(1, 10)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(random.randint(1, 10)):
            await asyncio.sleep(0)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def spaceship(canvas, row, column, frame1, frame2):
    """Spaceship animation"""
    while True:
        rows_direction, columns_direction, _ = read_controls(canvas)
        spaceship_rows, spaceship_columns = get_frame_size(frame1)
        board_rows, board_columns = get_board_size(canvas)

        max_ship_row_pos = board_rows - spaceship_rows
        max_ship_column_pos = board_columns -spaceship_columns

        row = row + rows_direction
        if row == max_ship_row_pos:
            row = row - 1
        elif row == 1:
            row = row + 1

        column = column + columns_direction
        if column == max_ship_column_pos:
            column = column - 1
        elif column == 1:
            column = column + 1

        draw_frame(canvas, row, column, frame1)
        
        canvas.refresh()
        await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame1, negative=True)
        draw_frame(canvas, row, column, frame2)
        
        canvas.refresh()
        await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame2, negative=True)
