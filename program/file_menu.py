from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import filedialog  # Import filedialog explicitly
import sys
import cv2 as cv
import numpy as np

# ============================ window update ============================

def get_window_size(root):
    # Get current width and height of the window
    current_width = root.winfo_width()
    current_height = root.winfo_height()

    print(f"window width={current_width}: window height={current_height}")

def on_resize(event, root):
    # Update window size on resize
    get_window_size(root)

    
# ============================ transparent background (checker board) ============================

def create_checkerboard(canvas, width, height, square_size):
    # Loop through the grid based on the square size
    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            # Alternate between light and dark colors for the checkerboard
            color = "#D3D3D3" if (x // square_size + y // square_size) % 2 == 0 else "#FFFFFF"
            canvas.create_rectangle(x, y, x + square_size, y + square_size, fill=color, outline="")

# ============================ FILE SYSTEM  ============================


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
        filepath = filedialog.askopenfilename()
        if filepath:
            self.image = cv.imread(filepath)
            self.modified_image = self.image.copy()
            self.update_canvas(self.modified_image)

    def quit(self):
        entry = askyesno(title="Quit", message="Are you sure you want to quit?")
        if entry:
            self.root.destroy()

    def __init__(self, root, canvas):
        self.image = None  # Original image
        self.modified_image = None  # The currently modified image
        self.root = root
        self.canvas = canvas  # Reference to the main canvas widget
        self.canvas_image_id = None  # Store the image ID on the canvas
        self.filepath = None  # Track the file path for saving
        self.current_blur_intensity = 0  # Track current blur intensity
        self.current_rotation_angle = 0  # Track current rotation angle


    def update_canvas(self, display_image=None):
        image_to_display = display_image if display_image is not None else self.modified_image
        if image_to_display is not None:
            canvas_width, canvas_height = int(self.canvas['width']), int(self.canvas['height'])
            img_resized = cv.resize(image_to_display, (canvas_width, canvas_height))

            img_rgb = cv.cvtColor(img_resized, cv.COLOR_BGR2RGB)
            img_ppm = cv.imencode(".ppm", img_rgb)[1].tobytes()
            img_tk = PhotoImage(data=img_ppm)

            if self.canvas_image_id is not None:
                self.canvas.delete(self.canvas_image_id)
            self.canvas_image_id = self.canvas.create_image(0, 0, anchor=NW, image=img_tk)
            self.canvas.image = img_tk
            
    def apply_blur(self, intensity):
        if self.modified_image is None:
            return
        # Reset to modified image and apply blur
        blurred_image = cv.GaussianBlur(self.modified_image, (intensity * 2 + 1, intensity * 2 + 1), 0)
        self.update_canvas(blurred_image)
        
    def apply_blur_changes(self, intensity):
        # Save changes permanently to modified image
        self.current_blur_intensity = intensity
        self.modified_image = cv.GaussianBlur(self.modified_image, (intensity * 2 + 1, intensity * 2 + 1), 0)
        self.update_canvas(self.modified_image)

    def rotate_image(self, angle):
        if self.modified_image is None:
            return
        # Reset to modified image and apply rotation
        (h, w) = self.modified_image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv.getRotationMatrix2D(center, angle, 1.0)
        rotated_image = cv.warpAffine(self.modified_image, rotation_matrix, (w, h))
        self.update_canvas(rotated_image)

    def apply_rotation_changes(self, angle):
        # Save changes permanently to modified image
        self.current_rotation_angle = angle
        (h, w) = self.modified_image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv.getRotationMatrix2D(center, angle, 1.0)
        self.modified_image = cv.warpAffine(self.modified_image, rotation_matrix, (w, h))
        self.update_canvas(self.modified_image)

    # Adjustment: Brightness and Contrast
    def adjust_brightness_contrast(self, brightness=0, contrast=0):
        if self.modified_image is None:
            return
        # Calculate brightness and contrast adjustments
        adjusted_image = cv.convertScaleAbs(self.modified_image, alpha=1 + (contrast / 100), beta=brightness)
        self.update_canvas(adjusted_image)

    def apply_brightness_contrast_changes(self, brightness, contrast):
        # Save brightness and contrast adjustments permanently to modified_image
        self.modified_image = cv.convertScaleAbs(self.modified_image, alpha=1 + (contrast / 100), beta=brightness)
        self.update_canvas(self.modified_image)

    # Filters
    def apply_filter(self, filter_type):
        if self.modified_image is None:
            return
        
        if filter_type == "Sepia":
            kernel = np.array([[0.272, 0.534, 0.131],
                               [0.349, 0.686, 0.168],
                               [0.393, 0.769, 0.189]])
            filtered_image = cv.transform(self.modified_image, kernel)
            filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)

        elif filter_type == "Grayscale":
            filtered_image = cv.cvtColor(self.modified_image, cv.COLOR_BGR2GRAY)
            filtered_image = cv.cvtColor(filtered_image, cv.COLOR_GRAY2BGR)  # Convert back to 3 channels for consistent display

        elif filter_type == "Negative":
            filtered_image = cv.bitwise_not(self.modified_image)

        elif filter_type == "Edge Detection":
            gray = cv.cvtColor(self.modified_image, cv.COLOR_BGR2GRAY)
            edges = cv.Canny(gray, 100, 200)
            filtered_image = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)  # Convert to 3 channels for display

        else:
            filtered_image = self.modified_image.copy()

        self.update_canvas(filtered_image)

    def apply_filter_changes(self, filter_type):
        # Apply selected filter permanently
        if filter_type == "Sepia":
            kernel = np.array([[0.272, 0.534, 0.131],
                               [0.349, 0.686, 0.168],
                               [0.393, 0.769, 0.189]])
            self.modified_image = cv.transform(self.modified_image, kernel)
            self.modified_image = np.clip(self.modified_image, 0, 255).astype(np.uint8)

        elif filter_type == "Grayscale":
            gray = cv.cvtColor(self.modified_image, cv.COLOR_BGR2GRAY)
            self.modified_image = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

        elif filter_type == "Negative":
            self.modified_image = cv.bitwise_not(self.modified_image)

        elif filter_type == "Edge Detection":
            gray = cv.cvtColor(self.modified_image, cv.COLOR_BGR2GRAY)
            edges = cv.Canny(gray, 100, 200)
            self.modified_image = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
        
        self.update_canvas(self.modified_image)

            
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

#=========

if __name__ == "__main__":
    print("Please run 'main.py'")
