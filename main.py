from tkinter import filedialog, Tk
from config import Config
from menu import MainMenu

def main():
    conf = Config()
    menu = MainMenu(conf)
    menu.start_window()

main()


 