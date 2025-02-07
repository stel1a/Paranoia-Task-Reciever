import os
from escpos import * 

from utils.ui import summon_ui
from rich.console import Console

p = printer.Usb(0x04b8,0x0202, profile="TM-T88IV")

""" Seiko Epson Corp. Reciept Printer (EPSON TM-T88IV) """
console = Console()
testing = False

if testing: p = printer.Dummy()

while True:
    summon_ui(p, is_testing=testing)
