## Inspiration 1 - https://github.com/wong2/pick/
## Inspiration 2 - https://github.com/charmbracelet/lipgloss

import curses
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

__all__ = ["Picker", "pick"]


KEYS_ENTER = (curses.KEY_ENTER, ord("\n"), ord("\r"))
KEYS_UP = (curses.KEY_UP, ord("k"))
KEYS_DOWN = (curses.KEY_DOWN, ord("j"))
PICK_RETURN_T = Tuple[str, int]


@dataclass
class Picker:
    """The :class:`Picker <Picker>` object
    :param options: a list of options to choose from
    :param title: (optional) a title above options list
    :param indicator: (optional) custom the selection indicator
    """

    options: List[str]
    title: Optional[str] = None
    indicator: str = "*"
    selected_indexes: List[int] = field(init=False, default_factory=list)
    index: int = field(init=False, default=0)
    scroll_top: int = field(init=False, default=0)

    def move_up(self) -> None:
        self.index = (self.index + len(self.options) - 1) % len(self.options)

    def move_down(self) -> None:
        self.index = (self.index + 1) % len(self.options)

    def mark_index(self) -> None:
        if self.index in self.selected_indexes:
            self.selected_indexes.remove(self.index)
        else:
            self.selected_indexes.append(self.index)

    def get_selected(self) -> List[PICK_RETURN_T]:
        return_tuples = []
        for selected in self.selected_indexes:
            return_tuples.append((self.options[selected], selected))
        return return_tuples

    def get_title_lines(self):
        if self.title:
            return self.title.split("\n") + [""]
        return []

    def get_option_lines(self):
        lines = []
        for index, option in enumerate(self.options):
            if index == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * " "
            line = ("{0} {1}".format(prefix, option), curses.color_pair(1))
            lines.append(line)  # type: ignore[arg-type]
        return lines

    def get_lines(self) -> Tuple[List, int]:
        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines  # type: ignore[operator]
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def draw(self, screen) -> None:
        """draw the curses ui on the screen, handle scroll if needed"""
        screen.clear()

        x, y = 1, 1  # start point
        max_y, max_x = screen.getmaxyx()
        max_rows = max_y - y  # the max rows we can draw

        lines, current_line = self.get_lines()

        # calculate how many lines we should scroll, relative to the top
        if current_line <= self.scroll_top:
            self.scroll_top = 0
        elif current_line - self.scroll_top > max_rows:
            self.scroll_top = current_line - max_rows

        lines_to_draw = lines[self.scroll_top : self.scroll_top + max_rows]

        for line in lines_to_draw:
            if type(line) is tuple:
                screen.addnstr(y, x, line[0], max_x - 2, line[1])
            else:
                screen.addnstr(y, x, line, max_x - 2)
            y += 1

        screen.refresh()

    def run_loop(self, screen) -> List[PICK_RETURN_T]:
        while True:
            self.draw(screen)
            c = screen.getch()
            if c in KEYS_UP:
                self.move_up()
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in KEYS_ENTER:
                return self.get_selected()

    def config_curses(self) -> None:
        try:
            # use the default colors of the terminal
            curses.use_default_colors()
            # hide the cursor
            curses.curs_set(0)
            curses.init_pair(1, curses.COLOR_RED, -1) #-1 is default color
        except:
            # Curses failed to initialize color support, eg. when TERM=vt100
            curses.initscr()

    def _start(self, screen) -> List[PICK_RETURN_T]:
        self.config_curses()
        return self.run_loop(screen)

    def start(self) -> List[PICK_RETURN_T]:
        return curses.wrapper(self._start)


def pick(
    options: List[str], title: Optional[str] = None, indicator: str = ">"
) -> List[PICK_RETURN_T]:
    picker = Picker(options, title, indicator)
    return picker.start()
