#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# key_press_checker.py: handles checking for a key being pressed without blocking on Windows and Linux

from xtlib import pc_utils

if pc_utils.is_windows():
    import msvcrt
else:
    import sys, select, tty, termios

class KeyPressChecker:
    def __init__(self):
        self.is_windows = pc_utils.is_windows()

    def __enter__(self):
        if not self.is_windows:
            # save off current stdin settings (LINE mode)
            self.old_settings = termios.tcgetattr(sys.stdin)

            # put stdin into CHAR mode
            tty.setcbreak(sys.stdin.fileno())

        return self

    def getch_wait(self):
        ch = None
        if self.is_windows:
            import msvcrt
            ch = msvcrt.getch()
        else:
            # linux
            ch = sys.stdin.read(1)
            # convert to byte
            ch = ch.encode()
        return ch

    def getch_nowait(self):
        ch = None
        if self.is_windows:
            import msvcrt
            if msvcrt.kbhit():
                ch = ord(msvcrt.getch())
        else:
            # linux
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                ch = ord(sys.stdin.read(1))
        return ch

    def __exit__(self, type, value, traceback):
        if not self.is_windows:
            # restore stdin to LINE mode
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
