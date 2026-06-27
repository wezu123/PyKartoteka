import logging
from os import path
import tkinter as tk
from tkinter import ttk
from handlers.bot import Bot
from static.gui import GUI

class Menu:
    def __init__(self, config):
        self.config = config    # Get running config from main
        self.name = self.config.get_val("app_name")
        self.version = self.config.get_val("app_version")
        self.root = tk.Tk()

        self.logger = logging.getLogger(__name__)
        self.logger.addFilter(self.infobox_log)

        self.border_color = "lightgrey"
        self.year_low = 2000
        self.year_high = 2100

    def infobox_log(self, record):
        GUI.draw_info_box(self.root, f'[{record.levelname}] {record.getMessage()}')
        return True

    def draw_menu(self):
        self.root.title(self.name + " " + self.version)
        self.root.resizable(False, False)
        #Declare all frames and grid them
        f_menu = tk.Frame(self.root, height=400, width=150, highlightbackground=self.border_color, highlightthickness=1)
        f_menu.grid(column=0, row=0, sticky="n")
        f_menu.pack_propagate(False)

        ttk.Label(f_menu, text=self.name).pack(pady=10)
        menu_buttons = [
            ttk.Button(f_menu, text="Start", command=self.draw_main_frame),
            ttk.Button(f_menu, text="Ustawienia", command=self.draw_settings),
            ttk.Button(f_menu, text="dev.run_default", command=lambda: self.run_main_compute(from_config=True)),
            ttk.Button(f_menu, text="dev.run_info", command=lambda: GUI.draw_info_box(self.root)),
            ttk.Button(f_menu, text="Pomoc", command=self.draw_help)
        ]
        for button in menu_buttons:
            button.pack()
            button.config(width=25) 
        exit_btn = ttk.Button(f_menu, text="Wyjdź", command=exit)
        exit_btn.pack(side="bottom")
        exit_btn.config(width=20) 

        self.draw_main_frame() 
        self.root.mainloop()

    def draw_main_frame(self):
        # Main Parent frame
        f_main = tk.Frame(self.root, height=400, width=800, bg="red")
        f_main.grid(column=1, row=0)
        f_main.grid_propagate(False)

        # Delete Path Frame
        self.del_path_var = GUI.draw_path_subframe(f_main, 0, 0, "Lokalizacja pliku ze zgonami:", path=self.config.get_val("path_del_file"), readonly=True)
        self.raport_path_var = GUI.draw_path_subframe(f_main, 0, 1, "Lokalizacja raportu KS-Somed:", path=self.config.get_val("path_last_load"))

        # Date Selectors Frame and Subframes
        f_dates = tk.Frame(f_main, height=100, width=800)
        f_dates.grid(column=0, row=2)
        f_dates.grid_propagate(False)

        self.del_date_val = GUI.draw_date_subframe(f_dates, 0, 0, "Rok usuwanych danych: ", year=self.config.get_val("year_cutoff"))
        self.raport_date_val = GUI.draw_date_subframe(f_dates, 1, 0, "Rok wykonania raportu: ", year=self.config.get_val("year_print"))

        # Form handling buttons
        f_submit = tk.Frame(f_main, height=100, width=800)
        f_submit.grid(column=0, row=3)
        f_submit.grid_propagate(False)

        ttk.Button(f_submit, text="Uruchom", command=self.run_main_compute).grid(column=0, row=0)


    # Example Function to showcase inplace frame changes
    def draw_help(self):
        f_main = tk.Frame(self.root, height=400, width=800, bg="red")
        f_main.grid(column=1, row=0)
    def draw_settings(self):
        f_main = tk.Frame(self.root, height=400, width=800, bg="green")
        f_main.grid(column=1, row=0)

    # Placeholder for future function, will be used to run main_compute with default params when UI is functional
    def run_default(self):
        pass


    def run_main_compute(self, from_config=False):
        self.bot = Bot(self.config, self) # Start Run with running config and menu instances
        if from_config:
            self.bot.main_compute()
        else:
            raport_path=self.raport_path_var.get()
            self.config.set_val("path_last_load", raport_path)
            del_list_path=self.del_path_var.get()
            self.config.set_val("path_del_file", del_list_path)
            print_year=self.raport_date_val.get()
            self.config.set_val("year_print", print_year)
            cutoff_year=self.del_date_val.get()
            self.config.set_val("year_cutoff", cutoff_year)

            self.bot.main_compute(
                raport_path,
                del_list_path,
                print_year,
                cutoff_year
            )