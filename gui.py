import customtkinter as ctk
from utils import set_save_directory, load_saved_directory, SAVE_DIRECTORY

def create_gui():
    ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

    root = ctk.CTk()  # Use CTk instead of Tk
    root.title("Auto Image Crop")

    # Set window size and position
    root.geometry("400x150")

    # Load the last saved directory
    last_directory = load_saved_directory()
    if last_directory:
        custom_info_dialog(root, "Directory Loaded", f"Last used directory:\n{last_directory}")

    # Create the main frame
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True)

    # Create and place the "Save Location" button
    save_button = ctk.CTkButton(main_frame, text="Save Location", command=lambda: handle_save_directory(root))
    save_button.pack(pady=20, padx=20, side="left")

    # Create and place the description label
    desc_label = ctk.CTkLabel(main_frame, text="Select the folder to save images")
    desc_label.pack(pady=20, padx=20, side="left")

    root.mainloop()

def handle_save_directory(root):
    save_dir = set_save_directory()
    if save_dir:
        custom_info_dialog(root, "Directory Selected", f"Images will be saved to:\n{save_dir}")

def custom_info_dialog(root, title, message):
    dialog = ctk.CTkToplevel(root)  # Use CTkToplevel to avoid blocking the main window
    dialog.title(title)

    # Set window size and center it
    dialog.geometry("350x150")
    position_right = int(dialog.winfo_screenwidth() / 2 - 175)
    position_down = int(dialog.winfo_screenheight() / 2 - 75)
    dialog.geometry(f"+{position_right}+{position_down}")

    # Add a label to display the message
    label = ctk.CTkLabel(dialog, text=message, font=("Arial", 12))
    label.pack(pady=(20, 10), padx=20)

    # Add an OK button to close the dialog
    button = ctk.CTkButton(dialog, text="OK", command=dialog.destroy, font=("Arial", 10))
    button.pack(pady=(10, 20))

    dialog.after(100, lambda: dialog.focus_force())
    dialog.after(200, lambda: dialog.focus())

    dialog.transient(root)  # Ensure the dialog stays on top of the root window
    dialog.grab_set()  # Ensure all focus is on the dialog until it is closed

    root.wait_window(dialog)  # Wait for the dialog to be closed before continuing
