import tkinter as tk
from tkinter import filedialog, ttk
from file_menu import *
from file_menu import File
import file_menu
import edit_menu
import help_menu

# ============================ Create the main window ============================
root = tk.Tk()
root.title("Shrimp")
root.minsize(640, 480)
root.geometry("800x600")
root.resizable(True, True)
root.configure(bg='#2b2b2b')  # Darker background color for main window

# ============================ Define the canvas size ============================
canvas_width = 500
canvas_height = 400
square_size = 20

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='#2b2b2b', highlightthickness=0)
canvas.place(x=10, y=10)
create_checkerboard(canvas, canvas_width, canvas_height, square_size)

# ============================= Menu bar =============================
menubar = tk.Menu(root, bg='#333333', fg='white', activebackground='#00a8cc', activeforeground='white', tearoff=0)

image = File(root, canvas)

file_menu.main(root, image, menubar)
edit_menu.main(root, image, menubar)
help_menu.main(root, menubar)

# ============================ Scrollable Sidebar ============================
sidebar_canvas = tk.Canvas(root, width=230, bg="#343434", highlightthickness=0)
sidebar_canvas.pack(side="right", fill="y")

scrollbar = tk.Scrollbar(root, orient="vertical", command=sidebar_canvas.yview)
scrollbar.pack(side="right", fill="y")

sidebar_canvas.configure(yscrollcommand=scrollbar.set)
sidebar_canvas.bind('<Configure>', lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all")))

sidebar_frame = tk.Frame(sidebar_canvas, bg="#343434")
sidebar_canvas.create_window((0, 0), window=sidebar_frame, anchor="nw")

label = tk.Label(sidebar_frame, text="Image Panel", bg="#343434", fg="white", font=("Arial", 13, "bold"))
label.pack(pady=10)

# ============================ Sidebar Widgets ============================

# Blur Controls
blur_frame = tk.LabelFrame(sidebar_frame, text="Blur", bg="#343434", fg="white", padx=10, pady=10)
blur_frame.pack(pady=10, fill="x")

blur_label = tk.Label(blur_frame, text="Blur Intensity", bg="#343434", fg="lightgray")
blur_label.pack(anchor="w")
blur_slider = tk.Scale(blur_frame, from_=0, to=100, orient="horizontal", bg="#4a4a4a", fg="white",
                       troughcolor="#3e3e3e", activebackground="#00a8cc", highlightthickness=0)
blur_slider.config(command=lambda value: image.apply_blur(int(value)))
blur_slider.pack(fill="x")

apply_blur_button = tk.Button(blur_frame, text="Apply Blur", bg="#00a8cc", fg="white", command=lambda: image.apply_blur_changes(blur_slider.get()))
apply_blur_button.pack(fill="x", pady=(5, 0))

# Rotate Controls
rotate_frame = tk.LabelFrame(sidebar_frame, text="Rotate", bg="#343434", fg="white", padx=10, pady=10)
rotate_frame.pack(pady=10, fill="x")

rotate_label = tk.Label(rotate_frame, text="Rotation Angle", bg="#343434", fg="lightgray")
rotate_label.pack(anchor="w")
rotate_slider = tk.Scale(rotate_frame, from_=0, to=360, orient="horizontal", bg="#4a4a4a", fg="white",
                         troughcolor="#3e3e3e", activebackground="#00a8cc", highlightthickness=0)
rotate_slider.config(command=lambda value: image.rotate_image(int(value)))
rotate_slider.pack(fill="x")

apply_rotate_button = tk.Button(rotate_frame, text="Apply Rotation", bg="#00a8cc", fg="white", command=lambda: image.apply_rotation_changes(rotate_slider.get()))
apply_rotate_button.pack(fill="x", pady=(5, 0))

# Brightness and Contrast Controls
adjust_frame = tk.LabelFrame(sidebar_frame, text="Adjustments", bg="#343434", fg="white", padx=10, pady=10)
adjust_frame.pack(pady=10, fill="x")

brightness_label = tk.Label(adjust_frame, text="Brightness", bg="#343434", fg="lightgray")
brightness_label.pack(anchor="w")
brightness_slider = tk.Scale(adjust_frame, from_=-100, to=100, orient="horizontal", bg="#4a4a4a", fg="white",
                             troughcolor="#3e3e3e", activebackground="#00a8cc", highlightthickness=0)
brightness_slider.pack(fill="x")

contrast_label = tk.Label(adjust_frame, text="Contrast", bg="#343434", fg="lightgray")
contrast_label.pack(anchor="w")
contrast_slider = tk.Scale(adjust_frame, from_=-100, to=100, orient="horizontal", bg="#4a4a4a", fg="white",
                           troughcolor="#3e3e3e", activebackground="#00a8cc", highlightthickness=0)
contrast_slider.pack(fill="x")

brightness_slider.config(command=lambda value: image.adjust_brightness_contrast(brightness=int(brightness_slider.get()), contrast=int(contrast_slider.get())))
contrast_slider.config(command=lambda value: image.adjust_brightness_contrast(brightness=int(brightness_slider.get()), contrast=int(contrast_slider.get())))

apply_adjust_button = tk.Button(adjust_frame, text="Apply Adjustments", bg="#00a8cc", fg="white", command=lambda: image.apply_brightness_contrast_changes(int(brightness_slider.get()), int(contrast_slider.get())))
apply_adjust_button.pack(fill="x", pady=(5, 0))

# Filter Controls
filter_frame = tk.LabelFrame(sidebar_frame, text="Filters", bg="#343434", fg="white", padx=10, pady=10)
filter_frame.pack(pady=10, fill="x")

filter_label = tk.Label(filter_frame, text="Select Filter", bg="#343434", fg="lightgray")
filter_label.pack(anchor="w")
filter_var = tk.StringVar(value="None")
filter_dropdown = ttk.Combobox(filter_frame, textvariable=filter_var)
filter_dropdown['values'] = ("None", "Sepia", "Grayscale", "Negative", "Edge Detection")
filter_dropdown.pack(fill="x")

filter_dropdown.bind("<<ComboboxSelected>>", lambda e: image.apply_filter(filter_var.get()))

apply_filter_button = tk.Button(filter_frame, text="Apply Filter", bg="#00a8cc", fg="white", command=lambda: image.apply_filter_changes(filter_var.get()))
apply_filter_button.pack(fill="x", pady=(5, 0))

# Crop Controls
crop_frame = tk.LabelFrame(sidebar_frame, text="Crop", bg="#343434", fg="white", padx=10, pady=10)
crop_frame.pack(pady=10, fill="x")
crop_button = tk.Button(crop_frame, text="Select Crop Area", bg="#00a8cc", fg="white")
crop_button.config(command=image.open_crop_window)

crop_button.pack(fill="x", pady=(0, 5))

# ============================ Window size ============================
get_window_size(root)

root.bind("<Configure>", lambda event: on_resize(event, root))

# Run the application
root.mainloop()
