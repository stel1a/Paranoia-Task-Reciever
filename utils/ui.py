import os
from utils.gather_files import gather_files
from utils.print import print_selected, test_printer_conditions
import rich.box
from escpos import * 
from readchar import readkey, key
from rich.align import Align
from rich.console import Console
from rich.style import Style 
from rich.table import Table
from rich.rule import Rule
from rich.padding import Padding
selected_style = Style(color="white", bgcolor="green", bold=True)

testing = False

def show_tutorial(console: Console):
    console.clear()
    console.show_cursor(True)
    bulletpoints = [
        "strikethrough (~~) isn't supported in python-escpos, so it inverts the text instead.",
        "italics (*) are not supported either, so i set them to underline text instead.",
        
        "inline text changes are not supported, so you have to declare them in the beginning of each line.\n\n" + 
        "example: '#* test' sets the text as an underlined header\n" + 
        "[rgb(150,150,150)]you can also end each line with the modifiers you set too, like [/][green]'#*test*'[/][rgb(150,150,150)] but it's not required. [/]"
    ]

    console.print(Rule("[bold green]a quick note !![/]"))
    console.print("this app mainly encourages the use of .md (markdown) files, [s rgb(150,150,150)](but .txt is also supported)[/]", justify="center")
    console.print(Padding("the library i am using to print these out to thermal printers (python-escpos), does not support a few common things (to my knowledge) that you use in vanilla markdown, so i've had to make some remedies.\n",(2,0,2,0)), justify="center")
    for point in bulletpoints:
        console.print(" • " + point)
    console.print("\n")
    console.print(Rule("[bold green]^^ please read the message above before we begin !! ^^ [/]"))
    console.print("\n[yellow]if you would like to see this message again, press [bold](y)[/]")
    console.print("[s rgb(150,150,150)](or delete the .tutorial_shown file in the tasks folder)[/]")
    console.print("otherwise, you can press any other key to continue.")
    try:
        if not readkey() == "y": # if they don't want to see the message again
            with open('./tasks/.tutorial_shown', 'a') as f:
                pass # create empty file
    except KeyboardInterrupt: # in case they control + c, don't give python error soup.
        close(console, testing=False)
    # initial run #
def summon_ui(p, console=Console(), present_tutorial=False, is_testing=False):
    # init variables #
    items = gather_files()
    selected_opt = 0

    if present_tutorial: show_tutorial(console)
    # init console #
    console.clear()
    console.show_cursor(False)
    draw_print_options(console, make_print_options(), items, selected_opt)

    test_printer_conditions(console, p)
    # read input & update index # 
    try:
        while True:
            items = gather_files()

            nav_char = readkey()
            match nav_char:
                case key.UP | "w":
                    selected_opt = max(0, selected_opt - 1)
                case key.DOWN | "s":
                    selected_opt = min(len(items) - 1, selected_opt + 1)
                case key.ENTER | key.SPACE:
                    break
                case "q":
                    close(console, testing=False)
            # update options table at the end of the input check
            console.clear()
            draw_print_options(console, make_print_options(), items, selected_opt)

        # choice made, so do the thing !! :3c # 
        console.clear()
        print_selected(console, "./tasks/" + items[selected_opt], p, is_testing)

        console.print("[bold green]print job seems to have succeeded !![/]")
        console.print("\n[s rgb(150,150,150)]if ya wanna exit, press q.[/]")
        console.print("[bold blue]press any other key to print something else !![/]")
        
        if readkey() == "q": close(console)

    except KeyboardInterrupt:
        close(console, testing=False)


def make_print_options():
    table = Table(box=rich.box.MINIMAL, title_justify="center")
    table.add_column("select file to print !!")
    # new table moment ,,.
    return table


def draw_print_options(console, table, rows=[], selected=0):
    console.clear()
    for i, row in enumerate(rows):
        if i == selected:
            table.add_row(row, style=selected_style)
        else:
            table.add_row(row)
    
    console.print(Align(table, align="center"))
    
def close(console: Console, err=None, testing=testing, msg=None):
    console.clear()
    console.show_cursor(True)
    if err:
        console.print(err)
        os._exit(1)
    
    if testing:
        console.print("[green]task was successful !![/]")
        if msg: print("\n" + msg)
        console.print("\n[yellow]close function called with testing enabled.\npress any key to continue.[/]")
        readkey()
        # dont exit, so that prg can loop. #
    else:
        # not testing, so exit.
        os._exit(0)
