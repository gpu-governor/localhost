import tkinter as tk
from tkinter import filedialog
from core import * # this imports all functions from
from cv import * 
import file_menu
import edit_menu
import format_menu
import help_menu

# ============================ Create the main window ============================
root = tk.Tk()
root.title("shrimp")
root.minsize(640, 480) # Set the minimum window size
root.geometry("800x600") # Set the window size
root.resizable(True, True)  # Allow resizing
root.configure(bg='#2d2d30') # Change the background color using configure (black gray background)
#=============================menu bar=============================
menubar = tk.Menu(root)
image = None

file_menu.main(root, image, menubar) # 50%
edit_menu.main(root, image, menubar) #10%
format_menu.main(root, image, menubar) #10%
help_menu.main(root, menubar) # 100%
#============================ Define the canvas size ============================
canvas_width = 500
canvas_height = 400
square_size = 20  # Size of each square in the checkerboard

# Create a Canvas widget
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.place(x=10,y=10)

# Create the checkerboard pattern
create_checkerboard(canvas, canvas_width, canvas_height, square_size) # this function is in the core.py

# ============================  slide panel ============================
# Create a sidebar frame
sidebar = tk.Frame(root, width=150, bg="lightgray", relief="sunken", borderwidth=2)
sidebar.pack(side="right", fill="y")

# Add widgets to the sidebar
label = tk.Label(sidebar, text="image properties", bg="lightgray", font=("Arial", 13))
label.pack(pady=10)
# Use a frame inside the sidebar for grid layout widgets
grid_frame = tk.Frame(sidebar, bg="lightgray")
grid_frame.place(x=1, y=30)

# Add labels in grid layout within the grid_frame
image_rex_label = tk.Label(grid_frame, text="Image Rex:", bg="lightgray")
image_rex_label.grid(row=0, column=0, sticky="w")
image_rex_data = tk.Entry(grid_frame, text="600x399")
image_rex_data.grid(row=1, column=0,sticky="w")


# Add more widgets as needed
# additional_label = tk.Label(sidebar, text="More Options", bg="lightgray")
# additional_label.pack(pady=(20, 5))
# ============================  window size ============================
get_window_size(root)  # Call this initially to print the size

# Bind the resize event to the on_resize function
root.bind("<Configure>", lambda event: on_resize(event, root))
# ============================ Run the application ============================
root.mainloop()
