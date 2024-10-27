import tkinter as tk
from tkinter import filedialog, ttk
from file_menu import *
from file_menu import File
import file_menu
import edit_menu
import help_menu

# ============================ Create the main window ============================
root = tk.Tk()
root.title("shrimp")
root.minsize(640, 480)  # Set the minimum window size
root.geometry("800x600")  # Set the window size
root.resizable(True, True)  # Allow resizing
root.configure(bg='#2d2d30')  # Change the background color using configure (black gray background)

# ============================ Define the canvas size ============================
canvas_width = 500
canvas_height = 400
square_size = 20  # Size of each square in the checkerboard

# Create a Canvas widget
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.place(x=10, y=10)

# Create the checkerboard pattern
create_checkerboard(canvas, canvas_width, canvas_height, square_size)  # this function is in the core.py

# ============================= Menu bar =============================
menubar = tk.Menu(root)
image = File(root, canvas)

file_menu.main(root, image, menubar)  # 50%
edit_menu.main(root, image, menubar)  # 10%
help_menu.main(root, menubar)  # 100%

# ============================ Scrollable Sidebar ============================
# Create a frame for the sidebar with a scrollbar
sidebar_canvas = tk.Canvas(root, width=230, bg="lightgray")
sidebar_canvas.pack(side="right", fill="y")

# Add a scrollbar to the sidebar canvas
scrollbar = tk.Scrollbar(root, orient="vertical", command=sidebar_canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure the canvas to scroll with the scrollbar
sidebar_canvas.configure(yscrollcommand=scrollbar.set)
sidebar_canvas.bind('<Configure>', lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all")))

# Create a frame inside the canvas to hold the sidebar widgets
sidebar_frame = tk.Frame(sidebar_canvas, bg="lightgray")
sidebar_canvas.create_window((0, 0), window=sidebar_frame, anchor="nw")

# Add widgets to the sidebar frame
label = tk.Label(sidebar_frame, text="Image Panel", bg="lightgray", font=("Arial", 13))
label.pack(pady=10)

# ============================ Sidebar Widgets ============================
# Blur Controls

# Blur Controls
blur_frame = tk.LabelFrame(sidebar_frame, text="Blur", bg="lightgray", padx=10, pady=10)
blur_frame.pack(pady=10, fill="x")

blur_label = tk.Label(blur_frame, text="Blur Intensity", bg="lightgray")
blur_label.pack(anchor="w")
blur_slider = tk.Scale(blur_frame, from_=0, to=100, orient="horizontal", bg="lightgray")
blur_slider.config(command=lambda value: image.apply_blur(int(value)))
blur_slider.pack(fill="x")

# Add Apply button for blur
apply_blur_button = tk.Button(blur_frame, text="Apply Blur", command=lambda: image.apply_blur_changes(blur_slider.get()))
apply_blur_button.pack(fill="x", pady=(5, 0))

# Rotate Controls
rotate_frame = tk.LabelFrame(sidebar_frame, text="Rotate", bg="lightgray", padx=10, pady=10)
rotate_frame.pack(pady=10, fill="x")

rotate_label = tk.Label(rotate_frame, text="Rotation Angle", bg="lightgray")
rotate_label.pack(anchor="w")
rotate_slider = tk.Scale(rotate_frame, from_=0, to=360, orient="horizontal", bg="lightgray")
rotate_slider.config(command=lambda value: image.rotate_image(int(value)))
rotate_slider.pack(fill="x")

# Add Apply button for rotate
apply_rotate_button = tk.Button(rotate_frame, text="Apply Rotation", command=lambda: image.apply_rotation_changes(rotate_slider.get()))
apply_rotate_button.pack(fill="x", pady=(5, 0))

# Crop Controls
crop_frame = tk.LabelFrame(sidebar_frame, text="Crop", bg="lightgray", padx=10, pady=10)
crop_frame.pack(pady=10, fill="x")

crop_button = tk.Button(crop_frame, text="Select Crop Area")
crop_button.pack(fill="x", pady=(0, 5))
# Brightness and Contrast Controls
adjust_frame = tk.LabelFrame(sidebar_frame, text="Adjustments", bg="lightgray", padx=10, pady=10)
adjust_frame.pack(pady=10, fill="x")

brightness_label = tk.Label(adjust_frame, text="Brightness", bg="lightgray")
brightness_label.pack(anchor="w")
brightness_slider = tk.Scale(adjust_frame, from_=-100, to=100, orient="horizontal", bg="lightgray")
brightness_slider.pack(fill="x")

contrast_label = tk.Label(adjust_frame, text="Contrast", bg="lightgray")
contrast_label.pack(anchor="w")
contrast_slider = tk.Scale(adjust_frame, from_=-100, to=100, orient="horizontal", bg="lightgray")
contrast_slider.pack(fill="x")

brightness_slider.config(command=lambda value: image.adjust_brightness_contrast(brightness=int(brightness_slider.get()), contrast=int(contrast_slider.get())))
contrast_slider.config(command=lambda value: image.adjust_brightness_contrast(brightness=int(brightness_slider.get()), contrast=int(contrast_slider.get())))

apply_adjust_button = tk.Button(adjust_frame, text="Apply Adjustments", command=lambda: image.apply_brightness_contrast_changes(int(brightness_slider.get()), int(contrast_slider.get())))
apply_adjust_button.pack(fill="x", pady=(5, 0))

# Filter Controls
filter_frame = tk.LabelFrame(sidebar_frame, text="Filters", bg="lightgray", padx=10, pady=10)
filter_frame.pack(pady=10, fill="x")

filter_label = tk.Label(filter_frame, text="Select Filter", bg="lightgray")
filter_label.pack(anchor="w")
filter_var = tk.StringVar(value="None")
filter_dropdown = ttk.Combobox(filter_frame, textvariable=filter_var)
filter_dropdown['values'] = ("None", "Sepia", "Grayscale", "Negative", "Edge Detection")
filter_dropdown.pack(fill="x")

filter_dropdown.bind("<<ComboboxSelected>>", lambda e: image.apply_filter(filter_var.get()))

apply_filter_button = tk.Button(filter_frame, text="Apply Filter", command=lambda: image.apply_filter_changes(filter_var.get()))
apply_filter_button.pack(fill="x", pady=(5, 0))


# Apply Button
apply_button = tk.Button(sidebar_frame, text="Apply Changes", bg="black", fg="white")
apply_button.pack(pady=20, fill="x")

# ============================ Window size ============================
get_window_size(root)  # Call this initially to print the size

# Bind the resize event to the on_resize function
root.bind("<Configure>", lambda event: on_resize(event, root))

# Run the application
root.mainloop()
