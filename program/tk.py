import cv2
import tkinter as tk
from PIL import Image, ImageTk

def show_image_in_tkinter():
    # OpenCV part: Load an image
    image_path = 'Untitled.jpeg'  # Replace with your image path
    cv_image = cv2.imread(image_path)

    # Convert from BGR to RGB format
    cv_image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    
    # Convert to PIL Image and then to ImageTk PhotoImage
    pil_image = Image.fromarray(cv_image_rgb)
    tk_image = ImageTk.PhotoImage(pil_image)

    # Tkinter part: Display the image
    root = tk.Tk()
    label = tk.Label(root, image=tk_image)
    label.pack()

    # Keep a reference to avoid garbage collection
    label.image = tk_image

    root.mainloop()

show_image_in_tkinter()
