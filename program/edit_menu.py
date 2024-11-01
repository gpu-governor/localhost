from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
from tkinter.messagebox import *


class Edit():

    def popup(self, event):
        self.rightClick.post(event.x_root, event.y_root)

    def undo(self, *args):
        self.text.edit_undo()

    def redo(self, *args):
        self.text.edit_redo()

    def find(self, *args):
        self.text.tag_remove('found', '1.0', END)
        target = askstring('Find', 'Search String:')

        if target:
            idx = '1.0'
            while 1:
                idx = self.text.search(target, idx, nocase=1, stopindex=END)
                if not idx: break
                lastidx = '%s+%dc' % (idx, len(target))
                self.text.tag_add('found', idx, lastidx)
                idx = lastidx
            self.text.tag_config('found', foreground='white', background='blue')

    def __init__(self, text, root):
        self.clipboard = None
        self.text = text
        self.rightClick = Menu(root)


def main(root, text, menubar):

    objEdit = Edit(text, root)

    editmenu = Menu(menubar)
    editmenu.add_command(label="Undo",  accelerator="Ctrl+Z")
    editmenu.add_command(label="Redo",  accelerator="Ctrl+Y")
    menubar.add_cascade(label="Edit", menu=editmenu)

    root.bind_all("<Control-z>", objEdit.undo)
    root.bind_all("<Control-y>", objEdit.redo)


    root.config(menu=menubar)


if __name__ == "__main__":
    print("Please run ui.py'")
