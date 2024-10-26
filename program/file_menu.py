from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import filedialog  # Import filedialog explicitly
import sys
import cv2 as cv
import numpy as np



class File():

    def newFile(self):
        # Placeholder function for "New" file action
        self.image = None
        self.update_canvas()
        
    def saveAs(self):
        # Prompt for a new file path and save the image
        if self.image is not None:
            self.filepath = filedialog.asksaveasfilename(defaultextension=".jpg")
            if self.filepath:
                cv.imwrite(self.filepath, self.image)
                
    def saveFile(self):
        # Save to the last used filepath, or prompt if it's the first save
        if self.image is not None:
            if self.filepath is None:
                self.saveAs()  # Prompt for a file path if one isn't set
            else:
                cv.imwrite(self.filepath, self.image)  # Save to existing filepath

    def openFile(self):
        # Open a file dialog to select an image
        filepath = filedialog.askopenfilename()
        if filepath:
            self.image = cv.imread(filepath)
            self.update_canvas()

    def quit(self):
        entry = askyesno(title="Quit", message="Are you sure you want to quit?")
        if entry:
            self.root.destroy()

    def __init__(self, root, canvas):
        self.image = None  # Placeholder for the OpenCV image
        self.root = root
        self.canvas = canvas  # Reference to the main canvas widget
        self.canvas_image_id = None  # Store the image ID on the canvas
        self.filepath = None  # Track the file path for saving

    def update_canvas(self):
        if self.image is not None:
            # Resize the image to fit the canvas dimensions
            canvas_width, canvas_height = int(self.canvas['width']), int(self.canvas['height'])
            img_resized = cv.resize(self.image, (canvas_width, canvas_height))

            # Convert OpenCV image (BGR) to RGB
            img_rgb = cv.cvtColor(img_resized, cv.COLOR_BGR2RGB)

            # Encode the RGB image as a PPM image to create a PhotoImage
            img_ppm = cv.imencode(".ppm", img_rgb)[1].tobytes()
            img_tk = PhotoImage(data=img_ppm)

            # Clear any previous image on the canvas and display the new one
            if self.canvas_image_id is not None:
                self.canvas.delete(self.canvas_image_id)
            self.canvas_image_id = self.canvas.create_image(0, 0, anchor=NW, image=img_tk)
            self.canvas.image = img_tk  # Keep a reference to avoid garbage collection
        else:
            # If no image, clear any existing image and revert to checkerboard
            if self.canvas_image_id is not None:
                self.canvas.delete(self.canvas_image_id)
            create_checkerboard(self.canvas, int(self.canvas['width']), int(self.canvas['height']), 20)

            
def main(root, image, menubar):
    filemenu = Menu(menubar)
    filemenu.add_command(label="New", command=image.newFile)
    filemenu.add_command(label="Open", command=image.openFile)
    filemenu.add_command(label="Save", command=image.saveFile)
    filemenu.add_command(label="Save As...", command=image.saveAs)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=image.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)


if __name__ == "__main__":
    print("Please run 'main.py'")
