from tkinter import filedialog, Tk
from config import Config
from MainMenu import MainMenu

def main():
    conf = Config()
    menu = MainMenu(conf)
    menu.start_window()

main()


 