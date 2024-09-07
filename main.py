from tkinter import filedialog, Tk
from config import Config
from menu import MainMenu

def main():
    conf = Config()
    running_config = conf.read_config()
    menu = MainMenu(running_config)
    menu.start_window()

main()


 