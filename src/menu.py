import sys
import termios
import tty

class Menu:
    def __init__(self, options: list[str]) -> None:
        self.options = options
        self._selected_index = 0
        pass

    def start_menu(self):
        self._create_space()
        selection = None
        while selection is None:
            self._print_menu()
            selection = self._get_user_input()
        return selection, self._selected_index

    def _get_user_input(self) -> str | None:
        key = ord(self._getch())
        choice = None
        if key == 65 and self._selected_index > 0:  # Up arrow
                self._selected_index -= 1
        elif key == 66 and self._selected_index < len(self.options) - 1:  # Down arrow
                self._selected_index += 1
        elif key == 13:  # Enter key
            if self.options[self._selected_index].lower() == "exit":
                sys.exit()
            choice = self.options[self._selected_index]
            
        return choice

    def _create_space(self):
        for _ in self.options:
            print()

    def _get_longest(self):
        longest = 0
        for option in self.options:
            if len(option) > longest:
                longest = len(option)
        return longest

    def _print_menu(self, padding = 2):
        for _ in self.options:
            sys.stdout.write("\033[F")

        longest = self._get_longest()
        pad = ' ' * padding

        for index, item in enumerate(self.options):
            sys.stdout.write("\033[K" + ("\033[44m" if index == self._selected_index else "") + f"{pad}{item.ljust(longest)}{pad}" + "\033[0m\n")

    def _getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch