from gui import create_gui
import keyboard
from utils import enter_ready_mode

def main():
    # GUI setup
    create_gui()

    # Set the hotkey to start capturing
    keyboard.add_hotkey('ctrl+space', enter_ready_mode)

    print("Press ctrl + Spacebar to activate ready mode.")
    keyboard.wait('esc')

if __name__ == "__main__":
    main()
