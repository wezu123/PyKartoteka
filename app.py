from tkinter import filedialog, Tk
from handlers.config import Config
from static.menu import MainMenu

def main():
    conf = Config()
    menu = MainMenu(conf)
    menu.start_window()

main() 