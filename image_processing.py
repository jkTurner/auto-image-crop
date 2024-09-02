import pyautogui
from PIL import Image, ImageDraw, ImageTk
from utils import is_whitish_or_black, save_cropped_image, notify_image_not_found
import tkinter as tk

def detect_left_border(image, mouse_x, height):
    for x in range(mouse_x, -1, -1):
        if all(is_whitish_or_black(image.getpixel((x, y))) for y in range(height) if x >= 0):
            continuous_white_or_black = all(is_whitish_or_black(image.getpixel((x-i, y))) for i in range(3) for y in range(height) if x-i >= 0)
            if continuous_white_or_black:
                return x + 3
    return 0

def detect_right_border(image, mouse_x, width, height):
    for x in range(mouse_x, width):
        if all(is_whitish_or_black(image.getpixel((x, y))) for y in range(height) if x < width):
            continuous_white_or_black = all(is_whitish_or_black(image.getpixel((x+i, y))) for i in range(3) for y in range(height) if x+i < width)
            if continuous_white_or_black:
                return x - 3
    return width

def detect_top_border(image, mouse_y, width):
    for y in range(mouse_y, -1, -1):
        if all(is_whitish_or_black(image.getpixel((x, y))) for x in range(width)):
            continuous_white_or_black = all(is_whitish_or_black(image.getpixel((x, y-i))) for i in range(10) for x in range(width) if y-i >= 0)
            if continuous_white_or_black:
                return y + 3
    return 0

def detect_bottom_border(image, mouse_y, width, height):
    for y in range(mouse_y, height):
        if all(is_whitish_or_black(image.getpixel((x, y))) for x in range(width) if y < height):
            continuous_white_or_black = all(is_whitish_or_black(image.getpixel((x, y+i))) for i in range(10) for x in range(width) if y+i < height)
            if continuous_white_or_black:
                return y - 3
    return height

def detect_image_on_hover(SAVE_DIRECTORY):
    screen_width, screen_height = pyautogui.size()

    try:
        x, y = pyautogui.position()

        region_width = int(screen_height * 0.75)
        region_height = screen_height
        region_x = max(0, x - region_width // 2)
        region_y = 0

        region = (region_x, region_y, region_x + region_width, region_y + region_height)
        screenshot = pyautogui.screenshot(region=region)

        img = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())

        left_bound = detect_left_border(img, x - region_x, region_height)
        right_bound = detect_right_border(img, x - region_x, region_width, region_height)
        top_bound = detect_top_border(img, y, region_width)
        bottom_bound = detect_bottom_border(img, y, region_width, region_height)

        # Validate the bounds before drawing
        if left_bound < right_bound and top_bound < bottom_bound:
            # Draw the blue border on the detected image for preview only
            img_with_border = img.copy()
            draw = ImageDraw.Draw(img_with_border)
            draw.rectangle([(left_bound, top_bound), (right_bound, bottom_bound)], outline="blue", width=3)

            # Crop the image to only include the detected area (no additional padding)
            cropped_img = img.crop((left_bound, top_bound, right_bound, bottom_bound))

            padding = 50
            mockup_img = img_with_border.crop((left_bound - padding, top_bound - padding, right_bound + padding, bottom_bound + padding))

            # Show the preview and wait for confirmation
            preview_and_confirm(cropped_img, mockup_img, SAVE_DIRECTORY)
        else:
            print("Invalid image bounds detected. Showing notification.")
            notify_image_not_found()

    except Exception as e:
        print(f"An error occurred: {e}")
        notify_image_not_found()


def preview_and_confirm(cropped_img, mockup_img, SAVE_DIRECTORY):
    # Create a Tkinter window to show the preview
    root = tk.Tk()
    root.title("Image Preview")

    # Convert the cropped image to Tkinter-compatible format
    mockup_image = ImageTk.PhotoImage(mockup_img)

    # Create a Canvas to allow scrolling
    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a vertical scrollbar
    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Display the image inside the frame
    label = tk.Label(frame, image=mockup_image)
    label.pack()

    # Limit the height of the popup window
    screen_height = root.winfo_screenheight()
    max_height = int(screen_height * 0.7)
    window_width = mockup_image.width()
    window_height = min(mockup_image.height(), max_height)
    root.geometry(f"{window_width}x{window_height}")

    # Update the scroll region to include the entire frame
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Bind mouse wheel event to the canvas for scrolling
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    def confirm(event=None):
        save_cropped_image(cropped_img, SAVE_DIRECTORY)
        root.destroy()

    def cancel(event=None):
        root.destroy()

    # Bind hotkeys for save ('s') and cancel ('f')
    root.bind('s', confirm)
    root.bind('S', confirm)
    root.bind('f', cancel)
    root.bind('F', cancel)

    # Center the window on the screen
    root.update_idletasks()
    position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
    root.geometry(f"+{position_right}+{position_down}")

    # Auto-select the popup window, using focus methods with a small delay
    root.after(100, lambda: root.focus_force())
    root.after(200, lambda: root.focus())

    root.mainloop()