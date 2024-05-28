import curses
from curses import wrapper
import time
import random


def text_sel():  #make a better selector
    with open('txt.txt', 'r') as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def screen_module(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome")
    stdscr.addstr("\npress any key to continue")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, test, curr, cpm=0):
    stdscr.clear()
    stdscr.addstr(test)
    stdscr.addstr(1, 0, f'cpm = {cpm}')

    for i, char in enumerate(curr):
        color_now = curses.color_pair(2)
        if test[i] != curr[i]:
            color_now = curses.color_pair(3)
        stdscr.addstr(0, i, char, color_now)


def typing_module(stdscr):
    test_text = text_sel()
    current_text = []
    cpm = 0
    start_time = time.time()
    stdscr.nodelay(True)  # framerate issue persists

    while True:
        time_now = max(time.time() - start_time, 1)
        cpm = round((len(current_text) / (time_now / 60)) / 5)
        display_text(stdscr, test_text, current_text, cpm)

        stdscr.refresh()
        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ('KEY_BACKSPACE', '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(test_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    screen_module(stdscr)
    typing_module(stdscr)


wrapper(main)
