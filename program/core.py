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
