import os
import time
from tkinter import filedialog, messagebox
import tkinter as tk
import json

# file to store the directory path
DIRECTORY_FILE = "saved_directory.json"

SAVE_DIRECTORY = None

def load_saved_directory():
    global SAVE_DIRECTORY
    if os.path.exists(DIRECTORY_FILE):
        with open(DIRECTORY_FILE, 'r') as file:
            data = json.load(file)
            SAVE_DIRECTORY = data.get("directory", None)
            if SAVE_DIRECTORY and os.path.exists(SAVE_DIRECTORY):
                return SAVE_DIRECTORY
            else:
                SAVE_DIRECTORY = None
                return None
    return None

def save_directory(directory):
    global SAVE_DIRECTORY
    SAVE_DIRECTORY = directory
    with open(DIRECTORY_FILE, 'w') as file:
        json.dump({"directory": directory}, file)

def set_save_directory():
    global SAVE_DIRECTORY
    selected_directory = filedialog.askdirectory(title="Select the folder to save images")
    if selected_directory:
        save_directory(selected_directory)  # Save the directory to the file and set SAVE_DIRECTORY
        return SAVE_DIRECTORY
    else:
        messagebox.showwarning("No Directory Selected", "Please select a directory to save images.")
        return None

def save_cropped_image(image, SAVE_DIRECTORY):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"cropped_image_{timestamp}.png"
    filepath = os.path.join(SAVE_DIRECTORY, filename)
    image.save(filepath)
    print(f"Cropped image saved as '{filepath}'")


def is_whitish_or_black(color):
    r, g, b = color
    return (r > 200 and g > 200 and b > 200) or (r < 50 and g < 50 and b < 50)  # Check for whitish or black color

def enter_ready_mode():
    if not SAVE_DIRECTORY:
        messagebox.showerror("Directory Not Set", "Please set a save directory first.")
        return
    
    print("Ready mode activated! Hover over the image and press ctrl + spacebar to capture.")
    from image_processing import detect_image_on_hover
    detect_image_on_hover(SAVE_DIRECTORY)

def notify_image_not_found():
    # Create a simple Tkinter window to notify the user
    root = tk.Tk()
    root.title("Notification")

    label = tk.Label(root, text="Image not found. Press any key or click the button to close and try again.", font=("Arial", 12))
    label.pack(pady=10, padx=20)

    # Add a button to close the notification
    button = tk.Button(root, text="Close", command=root.destroy, font=("Arial", 10))
    button.pack(pady=10)

    # Bind any key press to close the window
    root.bind('<Key>', lambda e: root.destroy())

    # Auto-select the popup window
    root.after(100, lambda: root.focus_force())
    root.after(200, lambda: root.focus())

    root.mainloop()
