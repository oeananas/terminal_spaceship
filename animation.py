import asyncio
import curses
import random
from tools import (
    draw_frame,
    read_controls,
    get_frame_size,
    get_board_size,
    get_spaceship_move
)


async def blink(canvas, row, column, symbol='*'):
    """Star blink animation."""
    
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
    """Spaceship animation."""

    while True:
        row, column = get_spaceship_move(canvas, frame1, row, column)
        draw_frame(canvas, row, column, frame1)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame1, negative=True)
        row, column = get_spaceship_move(canvas, frame2, row, column)
        draw_frame(canvas, row, column, frame2)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame2, negative=True)
        canvas.refresh()
