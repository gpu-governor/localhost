def update_canvas(self, display_image=None):
    image_to_display = display_image if display_image is not None else self.modified_image
    if image_to_display is not None:
        # Get dimensions of both canvas and image
        img_height, img_width = image_to_display.shape[:2]
        canvas_width, canvas_height = int(self.canvas['width']), int(self.canvas['height'])

        # Calculate the scale factor to fit the image within the canvas
        scale_factor = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)

        # Resize the image to fit within the canvas while maintaining aspect ratio
        img_resized = cv.resize(image_to_display, (new_width, new_height))

        # Convert the resized image to RGB and then to a PhotoImage-compatible format
        img_rgb = cv.cvtColor(img_resized, cv.COLOR_BGR2RGB)
        img_ppm = cv.imencode(".ppm", img_rgb)[1].tobytes()
        img_tk = PhotoImage(data=img_ppm)

        # Calculate position to center the image on the canvas
        x_pos = (canvas_width - new_width) // 2
        y_pos = (canvas_height - new_height) // 2

        # Clear previous image and display new one on the canvas
        if self.canvas_image_id is not None:
            self.canvas.delete(self.canvas_image_id)
        self.canvas_image_id = self.canvas.create_image(x_pos, y_pos, anchor=NW, image=img_tk)
        self.canvas.image = img_tk  # Keep a reference to avoid garbage collection
