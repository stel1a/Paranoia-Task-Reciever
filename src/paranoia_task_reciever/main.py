import os
from escpos import *

from .utils.ui import summon_ui, show_tutorial, create_tasks_folder, new_printer
from rich.console import Console

def main() -> None:
    testing = True

    console = Console()

    if not os.path.exists("./tasks/"):
        create_tasks_folder(console)

    if testing: p = printer.Dummy()
    else:
        if not os.path.exists("./.printer"):
            p = new_printer(console)
        else:
            f = open("./.printer", "r").read().split(",")
            opt = list(map(int, f))
            p = printer.Usb(opt[0], opt[1])

    if not os.path.exists("./tasks/.tutorial_shown"):
        show_tutorial(console)

    while True:
        summon_ui(p, console, is_testing=testing)


if __name__ == "__main__":
    main()
