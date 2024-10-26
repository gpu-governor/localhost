from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import sys


class File():

    def newFile(self):
        # Placeholder function for "New" file action
        self.image = None
        self.update_canvas()

    def saveFile(self):
        # Save the modified image to a file
        if self.image is not None:
            filepath = filedialog.asksaveasfilename(defaultextension=".jpg")
            if filepath:
                cv2.imwrite(filepath, self.image)

    def saveAs(self):
        # Save the modified image to a file
        if self.image is not None:
            filepath = filedialog.asksaveasfile(defaultextension=".jpg")
            if filepath:
                cv2.imwrite(filepath, self.image)

    def openFile(self):
        # Open a file dialog to select an image
        filepath = filedialog.askopenfilename()
        if filepath:
            self.image = cv2.imread(filepath)
            self.update_canvas()

    def quit(self):
        entry = askyesno(title="Quit", message="Are you sure you want to quit?")
        if entry:
            self.root.destroy()

    def __init__(self, root):
        self.image = None  # Placeholder for the OpenCV image
        self.root = root

    def update_canvas(self):
        if self.image is not None:
            # Convert the OpenCV image (BGR) to RGB
            img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(img_pil)

            # Update the Tkinter label with the new image
            self.canvas.configure(image=img_tk)
            self.canvas.image = img_tk  # Keep a reference to avoid garbage collection


def main(root, image, menubar):
    filemenu = Menu(menubar)
    objFile = image
    filemenu.add_command(label="New", command=objFile.newFile)
    filemenu.add_command(label="Open", command=objFile.openFile)
    filemenu.add_command(label="Save", command=objFile.saveFile)
    filemenu.add_command(label="Save As...", command=objFile.saveAs)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=objFile.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)


if __name__ == "__main__":
    print("Please run 'main.py'")