import os
from escpos import * 

from .utils.ui import summon_ui, show_tutorial, create_tasks_folder
from rich.console import Console

def main() -> None:
    testing = True

    # ----------------------------------------------------------------------------------------------------------------------- 
    # either lookup the idVendor and idProduct for your esc-pos printer online
    # or run dmesg rq to get that info.
    # -------------------------------------------------------------------------------
    # if ya need any help, https://python-escpos.readthedocs.io/en/latest/ may help.
    #
    # [if you have a different mark version of the same printer (like TM-T88III), you can just change the profile option 
    # accordingly without further modification.]
    # ----------------------------------------------------------------------------------------------------------------------- 
    """ Seiko Epson Corp. Reciept Printer (EPSON TM-T88IV) """
    p = printer.Usb(0x04b8,0x0202, profile="TM-T88IV") # idVendor, idProduct, profile
    # ----------------------------------------------------------------------------------------------------------------------- 
    console = Console()

    if testing: p = printer.Dummy()
    
    if not os.path.exists("./tasks/"):
        create_tasks_folder(console)

    if not os.path.exists("./tasks/.tutorial_shown"):
        show_tutorial(console)

    while True:
        summon_ui(p, console, is_testing=testing)


if __name__ == "__main__":
    main()