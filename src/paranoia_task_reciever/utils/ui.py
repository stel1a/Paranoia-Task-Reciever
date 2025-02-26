import os
from .gather_files import gather_files
from .print import print_selected, test_printer_conditions
import rich.box
from escpos import * 
from readchar import readkey, key
from rich.align import Align
from rich.console import Console
from rich.style import Style 
from rich.table import Table
from rich.rule import Rule
from rich.padding import Padding
import usb
selected_style = Style(color="white", bgcolor="green", bold=True)

testing = False

def create_tasks_folder(console: Console):
    if len(os.listdir("./")) == 0: os.mkdir("./tasks/")
    else:
        console.clear()
        console.show_cursor(True)
        console.print(Rule("[bold red]the current directory is not empty !![/]", style=Style(color="red")))
        console.print("we need to make a 'tasks' folder to store our paranoia tasks that we will give out to our players.", justify="center")
        console.print("however, your directory is [bold]not empty !![/]", justify="center")
        console.print(Rule("", style=Style(color="red")))
        console.print("[yellow]if you would like to create a 'tasks' folder anyway, press [bold](y)[/bold], otherwise press any key to quit. [/]")
        try:
            if not readkey() == "y":
                close(console, testing=False)
            
            os.mkdir("./tasks/")
        except KeyboardInterrupt:
            close(console, testing=False)


def new_printer(console: Console) -> printer.Usb:
    p: printer.Usb

    console.clear()
    console.show_cursor(False)
    console.print(Rule("[bold yellow]set up the printer !! [/]", style=Style(color="yellow")))
    console.print("the printer settings file (.printer) has not been detected in your current directory.\npick the device that looks right to you, and we'll set it up !!\n", justify="center")
    console.print("press enter to continue.", justify="center")

    # wait until user presses enter or q to exit
    while True:
        try:
            read = readkey() 
            if read == key.ENTER: break
            elif read == "q": close(console, testing=False)
        except KeyboardInterrupt:
            close(console, testing=False)
    
    
    console.clear()
    console.show_cursor(True)

    # find all usb devices plugged in right now.
    all_devs = usb.core.find(find_all=True)
    usable_devs = []
    for dev in all_devs:
        try:
            # if these values can't be found, it errors out and the device is thrown as unusable.
            dev.idVendor
            dev.idProduct 
            usb.util.get_string(dev, dev.iProduct)
            usb.util.get_string(dev, dev.iManufacturer)
            usable_devs.append(dev)
        except:
            continue

    if usable_devs is None: close(console, err="[bold red]no usb devices found !! exiting.[/]", testing=False)
    
    selected_device = None
    # if there is only one option, choose that one.
    if len(usable_devs) == 1: 
        selected_device = {
            "idVendor": int(hex(usable_devs[0].idVendor), 16),
            "idProduct": int(hex(usable_devs[0].idProduct), 16)
        }
    else:
            
        # list the usable devices and prompt the user to choose a suitable device.
        for i, dev in enumerate(usable_devs, start=1):
            manufacturer = usb.util.get_string(dev, dev.iManufacturer)
            dev_name = usb.util.get_string(dev, dev.iProduct)
            console.print(f"{i}. Device: {manufacturer} - {dev_name} ")
        
        console.print(f"pick a device !! (1-{len(usable_devs)}) [rgb(150,150,150) s](or press q to quit)[/]")
        
        # wait until user has made a choice.
        while True:
            try: 
                read = readkey()
                if read == "q": close(console, testing=False)

                # convert into array index.
                read = int(read)
                if read - 1 > len(usable_devs) - 1 or read - 1 < 0: continue # index out of bounds

                # no errors !! save it as the selected device.
                selected_device = {
                    "idVendor": int(hex(usable_devs[read - 1].idVendor), 16), 
                    "idProduct": int(hex(usable_devs[read - 1].idProduct), 16)
                }

                break
            except ValueError or IndexError:
                console.print(Rule("", style=Style(color="red")))
                console.print("[bold red]the value you typed has an incorrect format. try again !! [/]")
                console.print(Rule("", style=Style(color="red")))
                continue
            except KeyboardInterrupt:
                close(console, testing=False)
    console.clear()

    # test the printer. 
    p = printer.Usb(selected_device.get("idVendor"), selected_device.get("idProduct"))
    test_printer_conditions(console, p)

    # yay, it hasn't exited after using the test_printer_conditions function. save it !!

    with open("./.printer", 'a') as f:
        f.write(f'{selected_device.get("idVendor")},{selected_device.get("idProduct")}')
        f.close()
    
    console.clear()
    console.print("[bold green]printer is detected !!\npress any key to start the program !!\n", justify="center")
    console.print("[rgb(150,150,150) s]or press q to quit.[/]", justify="center")
    if readkey() == "q": close(console, testing=False)
    return p

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

    console.print("\n[bold yellow]please setup the printer in the main.py file as well (reinstall the script if you change it !!)[/]", justify="center")
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


def summon_ui(p, console=Console(), is_testing=False):
    # init variables #
    items = gather_files()
    selected_opt = 0
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
