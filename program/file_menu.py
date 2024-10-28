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
        # Clear the current image
        self.image = None
        self.modified_image = None
        self.filepath = None

        # Reset canvas size to initial dimensions
        initial_width, initial_height = 500, 400  # Set initial dimensions here
        self.canvas.config(width=initial_width, height=initial_height)
        
        # Clear the canvas and recreate the checkerboard pattern
        self.canvas.delete("all")
        create_checkerboard(self.canvas, initial_width, initial_height, 20)  # Checkerboard

        # Reset the canvas image ID
        self.canvas_image_id = None
        
    def saveAs(self):
        # Prompt for a new file path and save the modified image if available
        if self.modified_image is not None:
            self.filepath = filedialog.asksaveasfilename(defaultextension=".jpg")
            if self.filepath:
                cv.imwrite(self.filepath, self.modified_image)
        elif self.image is not None:
            self.filepath = filedialog.asksaveasfilename(defaultextension=".jpg")
            if self.filepath:
                cv.imwrite(self.filepath, self.image)

    def saveFile(self):
        # Save to the last used filepath, or prompt if it's the first save
        if self.modified_image is not None:
            if self.filepath is None:
                self.saveAs()  # Prompt for a file path if one isn't set
            else:
                cv.imwrite(self.filepath, self.modified_image)  # Save modified image to existing filepath
        elif self.image is not None:
            if self.filepath is None:
                self.saveAs()
            else:
                cv.imwrite(self.filepath, self.image)
            


    def openFile(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.image = cv.imread(filepath)
            self.modified_image = self.image.copy()
            
            # Resize canvas to match the image's dimensions
            img_height, img_width = self.image.shape[:2]
            self.canvas.config(width=img_width, height=img_height)

            # Update canvas with the loaded image
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
        # Same as before, but image resizes to fit the canvas
        image_to_display = display_image if display_image is not None else self.modified_image
        if image_to_display is not None:
            # Get current canvas dimensions
            canvas_width, canvas_height = int(self.canvas['width']), int(self.canvas['height'])
            
            # Resize image to fit the current canvas size
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

    def open_crop_window(self):
        if self.image is None:
            showerror("Error", "No image loaded to crop.")
            return

        # Create a new window for cropping
        self.crop_window = Toplevel(self.root)
        self.crop_window.title("Crop Image")
        self.crop_window.geometry("600x550")

        # Instruction label
        instruction_label = Label(self.crop_window, text="Use the mouse to select the crop area. Left-click and drag to draw.", font=("Arial", 10))
        instruction_label.pack(pady=5)

        # Set up variables for drawing the rectangle
        self.crop_start_x = self.crop_start_y = None
        self.crop_rect = None

        # Resize image to fit the crop window
        img_resized = cv.resize(self.image, (600, 400))
        img_rgb = cv.cvtColor(img_resized, cv.COLOR_BGR2RGB)
        img_ppm = cv.imencode(".ppm", img_rgb)[1].tobytes()
        self.crop_image_tk = PhotoImage(data=img_ppm)

        # Set up canvas in the crop window
        self.crop_canvas = Canvas(self.crop_window, width=600, height=400)
        self.crop_canvas.pack()
        self.crop_canvas.create_image(0, 0, anchor=NW, image=self.crop_image_tk)

        # Bind mouse events for drawing rectangle
        self.crop_canvas.bind("<Button-1>", self.start_crop)
        self.crop_canvas.bind("<B1-Motion>", self.draw_crop_rectangle)

        # Add "Apply Crop" and "Cancel" buttons
        button_frame = Frame(self.crop_window)
        button_frame.pack(pady=10)

        apply_button = Button(button_frame, text="Apply Crop", command=self.apply_crop)
        apply_button.grid(row=0, column=0, padx=10)

        cancel_button = Button(button_frame, text="Cancel", command=self.crop_window.destroy)
        cancel_button.grid(row=0, column=1, padx=10)

    def start_crop(self, event):
        # Record the start position for cropping
        self.crop_start_x, self.crop_start_y = event.x, event.y
        if self.crop_rect:
            self.crop_canvas.delete(self.crop_rect)
            self.crop_rect = None

    def draw_crop_rectangle(self, event):
        # Draw a rectangle on the crop canvas as the user drags the mouse
        if self.crop_rect:
            self.crop_canvas.delete(self.crop_rect)
        self.crop_rect = self.crop_canvas.create_rectangle(
            self.crop_start_x, self.crop_start_y, event.x, event.y,
            outline="blue", width=2, stipple="gray25"
        )

    def apply_crop(self):
        if self.crop_start_x is not None and self.crop_start_y is not None and self.crop_rect:
            # Calculate the crop area
            x0, y0 = min(self.crop_start_x, self.crop_canvas.winfo_pointerx() - self.crop_canvas.winfo_rootx()), min(self.crop_start_y, self.crop_canvas.winfo_pointery() - self.crop_canvas.winfo_rooty())
            x1, y1 = max(self.crop_start_x, self.crop_canvas.winfo_pointerx() - self.crop_canvas.winfo_rootx()), max(self.crop_start_y, self.crop_canvas.winfo_pointery() - self.crop_canvas.winfo_rooty())

            # Map coordinates to original image size
            img_width, img_height = self.image.shape[1], self.image.shape[0]
            x0 = int(x0 * img_width / 600)
            x1 = int(x1 * img_width / 600)
            y0 = int(y0 * img_height / 400)
            y1 = int(y1 * img_height / 400)

            # Apply the crop and update the main canvas
            self.image = self.image[y0:y1, x0:x1]
            self.update_canvas()
            self.crop_window.destroy()
            
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
