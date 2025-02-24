import os
from escpos import * 

from utils.ui import summon_ui, show_tutorial
from rich.console import Console

testing = False
present_tutorial = False

p = printer.Usb(0x04b8,0x0202, profile="TM-T88IV")

""" Seiko Epson Corp. Reciept Printer (EPSON TM-T88IV) """
console = Console()

if testing: p = printer.Dummy()

if not os.path.exists("./tasks/.tutorial_shown"):
    show_tutorial(console)


while True:
    summon_ui(p, console, is_testing=testing)
