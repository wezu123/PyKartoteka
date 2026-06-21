import logging
from tkinter import filedialog, Tk
from handlers.config import Config
from handlers.log import Log
from static.menu import Menu

def main():
    conf = Config()

    Log.setup_logger()
    logging.getLogger(__name__).info(
        f"============== Program {conf.get_val('app_name')} {conf.get_val('app_version')} uruchomiony =============="
        )

    menu = Menu(conf)
    menu.draw_menu()

main() 