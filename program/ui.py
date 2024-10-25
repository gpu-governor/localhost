import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Tkinter Window Background Color")

# Set the window size
root.geometry("400x300")

# Change the background color using configure
root.configure(bg='lightblue')

# Run the application
root.mainloop()
