# CRPN, a Curses based RPN calculator
# Copyright (C) 2016 Bart de Waal
# This program is licenced under the GPL version three, see Licence file for details
import curses


class EchoOn:
    """ helper class, so you can say "with EchoOn:" """
    def __enter__(self):
        curses.echo()

    def __exit__(self, type, value, traceback):
        curses.noecho()


class NoDelay:
    """ Alows you to do a getch() that times out as soon as possible """
    # Todo: find out why this is so slow
    def __init__(self, window):
        self.window = window

    def __enter__(self):
        self.window.nodelay(True)
        self.window.timeout(1)

    def __exit__(self, type, value, traceback):
        self.window.nodelay(False)
        self.window.timeout(-1)


def getKeyAlt(window):
    """ getKey, but adding ! in front of keys pressed with alt """
    key = window.getch()
    # If alt+ something is pressed, getch returns 27 and will return the next
    # character on the next round
    if key == 27:
        with NoDelay(window):
            key = window.getch()
        # If the second character doesn't come (getch times out with -1) this
        # is an escape
        if key == -1:
            return '^['
        else:
            return '!' + curses.unctrl(key).decode('ascii')
    return curses.unctrl(key).decode('ascii')


def getEntry(window, key):
    """ Enter an entry, using the window to display the entry
        It handles key (a string) as the start of the entry
        Returns a tuple: (string entered, key pressed to abort entry) """
    window.refresh()

    # '_' means '-' in this context, to allow users to enter negative numbers
    if key[0] == '_':
        key = '-' + key[1:]

    # display the first character(s) the user already entered
    window.addstr(0, 0, key)
    window.refresh()

    c = window.getkey()
    while c in "1234567890.e":
        key = key + c
        window.clear()
        window.addstr(0, 0, key)
        window.refresh()
        c = window.getkey()

    window.clear()
    window.refresh()

    return key, c