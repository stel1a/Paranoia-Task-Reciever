# enter virtual environment with 'source ~/.venvs/task_reciever/bin/activate' in bash before executing #
from escpos import * 
import utils.ui as ui
import os
import re

def test_printer_conditions(console, p):
    try:
        p.open()
    except Exception as e:
        if "Device not found" in str(e):
            ui.close(console, "[bold red]the printing device was not found !![/][rgb(80,80,80)]\n\nis it connected?\ndid ya change the 'p' (printer) variable accordingly in the main script?[/]")
        else:
            ui.close(console, "[bold red]an error has occured that isn't caught !![/]\n\n" + str(e))

def handle_text_modifiers(ln: str, p):
    # italics and strikethrough are not supported in python-escpos (to my knowledge),
    # so i replaced them with underline and invert, respectively.
    # ---------------------------------------------------------------------------------
    # counting asterisks is a tacky way to differentiate md "italics" 
    # (italics not supported in escpos python so i chose to underline instead) and bold, 
    # but it works for now.
    star_cnt = 0 

    op = ln
    for char in ln:
        match char:
            case "#": # header
                p.set(bold=True, underline=1, align='center')
                op = op[1:].strip()

            case "*": # "italics" or bold
                star_cnt += 1
                match star_cnt:
                    case 1: # reg "italics" 
                        p.set(underline=1) 
                    case 2: # reg bold
                        p.set(underline=0, bold=True)
                    case 3: # bold and "italic"
                        p.set(underline=1, bold=True)
                op = ln.replace("*", "").strip()
            case "~":
                p.set(invert=True)
                op = ln.replace("~~", "").strip()
            case _:
                # regular letter, so it just stops setting stuff. 
                # this is because i don't think inline setting changes are supported in python-escpos,
                # so i have to set the whole line as such. 
                break  
    
    p.text(op + "\n")
    p.set(bold=False, underline=0, align='left', invert=False) # return to default

def print_selected(console, filename: str, p, testing=False):
    try:
        f = open(filename, 'r')
    except FileNotFoundError:
        ui.close(console, "[bold red]file not found !! closing to prevent python error soup.[/]")
    
    for ln in f:
        handle_text_modifiers(ln, p)

    p.cut()

    if testing:
        ui.close(console, testing=testing, msg=str(p.output))
    
