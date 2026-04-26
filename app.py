from tkinter import filedialog, Tk
from handlers.config import Config
from static.menu import Menu

def main():
    conf = Config()
    menu = Menu(conf)
    menu.draw_menu()

main() 