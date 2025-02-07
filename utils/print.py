# enter virtual environment with 'source ~/.venvs/task_reciever/bin/activate' in bash before executing #
from escpos import * 
import utils.ui as ui
import os
import re

md_patterns = {
    "header": "^(#{1,6})\s+(.+)$",
    "bold": "\*\*(.+?)\*\*|__(.+?)__",
    "underline": "\*(.+?)\*|_(.+?)_", # italics are not supported in python-escpos, so i opted to use this as underlines.
    "strikethrough": "~~(.+?)~~",
}
#md_regex = re.compile(r'\b(' + '|'.join(md_patterns) + r')\b')

def test_printer_conditions(console, p):
    try:
        p.open()
    except Exception as e:
        if "Device not found" in str(e):
            ui.close(console, "[bold red]the printing device was not found !![/][rgb(80,80,80)]\n\nis it connected?\ndid ya change the 'p' (printer) variable accordingly in the main script?[/]")
        else:
            ui.close(console, "[bold red]an error has occured that isn't caught !![/]\n\n" + str(e))
def handle_md(ln, p):
    for pat, ex in md_patterns.items():
        matches = re.findall(ex, ln)
        if matches:
            match pat:
                case "header":
                    p.set(bold=True, underline=1, align='center')
                    p.text(matches[0][1])
                    p.set(bold=False, underline=0, align='left')
                    break
                case "bold":
                    p.set(bold=True)
                    p.text(matches[0][0])
                    p.set(bold=False)
                    break
                case "underline":
                    p.set(underline=1)
                    p.text(matches[0][0])
                    p.set(underline=0)
                    break
                case "strikethrough":
                    p.set(invert=True)
                    p.text(matches[0])
                    p.set(invert=False)
                    break
                    ''' if inline text changes are supported '''
                    '''
                    for m in matches: 
                        match pat:
                            case "bold":
                                p.set(bold=True)
                                p.text(ln)
                                p.set(bold=False)
                            case "underline":
                    '''
def print_selected(console, filename: str, p, testing=False):
    tm = []
    try:
        f = open(filename, 'r')
    except FileNotFoundError:
        ui.close(console, "[bold red]file not found !! closing to prevent python error soup.[/]")
    if filename.endswith(".md"):
        for ln in f:
            handle_md(ln, p)
    else:
        # plain text #
        for ln in f:
            p.text(ln.strip())
        p.cut()
    
