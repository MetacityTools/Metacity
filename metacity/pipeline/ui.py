## Inspiration 1 - https://github.com/wong2/pick/
## Inspiration 2 - https://github.com/charmbracelet/lipgloss
## Inspiration 3 - https://github.com/bczsalba/pytermgui

import time
import pytermgui as ptg

def macro_time(fmt: str) -> str:
    return time.strftime(fmt)

def ui():
    ptg.tim.define("!time", macro_time)

    with ptg.WindowManager() as manager:
        manager.layout.add_slot("Body")
        manager.add(
            ptg.Window("[bold]The current time is:[/]\n\n[!time 75]%c", box="EMPTY")
        )