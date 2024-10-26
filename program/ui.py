import tkinter as tk
from tkinter import filedialog
from core import * # this imports all functions from 
import file_menu
import edit_menu
import format_menu
import help_menu

# ============================ Create the main window ============================
root = tk.Tk()
root.title("imag3")
root.minsize(640, 480) # Set the minimum window size
root.geometry("800x600") # Set the window size
root.resizable(True, True)  # Allow resizing
root.configure(bg='#2d2d30') # Change the background color using configure (black gray background)
#======menu bar
menubar = tk.Menu(root)
text = 0

file_menu.main(root, text, menubar)
#edit_menu.main(root, text, menubar)
#format_menu.main(root, text, menubar)
#help_menu.main(root, text, menubar)
#============================ Define the canvas size ============================
canvas_width = 400
canvas_height = 300
square_size = 20  # Size of each square in the checkerboard

# Create a Canvas widget
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Create the checkerboard pattern
create_checkerboard(canvas, canvas_width, canvas_height, square_size) # this function is in the core.py

# ============================  widgets ============================

button_exit = tk.Button(menubar, text = "Exit", command = exit)
button_exit.pack()
# ============================  window size ============================
get_window_size(root)  # Call this initially to print the size

# Bind the resize event to the on_resize function
root.bind("<Configure>", lambda event: on_resize(event, root))
# ============================ Run the application ============================
root.mainloop()
