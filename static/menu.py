import logging
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
        f_del_path = tk.Frame(f_main, height=100, width=800, border=10, highlightbackground=self.border_color, highlightthickness=1)
        f_del_path.grid(column=0, row=0)
        f_del_path.grid_propagate(False)
        ttk.Label(f_del_path, text="Lokalizacja pliku ze zgonami:").grid(column=0, row=0, sticky="W")
        s_del_path = tk.StringVar(value=self.config.get_val("path_del_file"))
        e_del_path = ttk.Entry(f_del_path, width=100, state="readonly", textvariable=s_del_path).grid(column=0, row=1)
        ttk.Button(f_del_path, text="Przeglądaj...", command=lambda: GUI.get_open_path(self.root, s_del_path)).grid(column=1,row=1)

        # Source Path Frame
        f_raport_path = tk.Frame(f_main, height=100, width=800, border=10, highlightbackground=self.border_color, highlightthickness=1)
        f_raport_path.grid(column=0, row=1)
        f_raport_path.grid_propagate(False)
        ttk.Label(f_raport_path, text="Lokalizacja raportu KS-Somed:").grid(column=0, row=0, sticky="W")
        s_raport_path = tk.StringVar(value=self.config.get_val("path_last_load", quiet=True))
        e_raport_path = ttk.Entry(f_raport_path, width=100, textvariable=s_raport_path).grid(column=0, row=1)
        ttk.Button(f_raport_path, text="Przeglądaj...", command=lambda: GUI.get_open_path(self.root, s_raport_path)).grid(column=1,row=1)

        # Date Selectors Frame and Subframes
        f_dates = tk.Frame(f_main, height=100, width=800)
        f_dates.grid(column=0, row=2)
        f_dates.grid_propagate(False)

        # Delete date subframe - incomplete
        f_dates_b1 = tk.Frame(f_dates, height=100, width=400, highlightbackground=self.border_color, highlightthickness=1)
        f_dates_b1.grid(column=0, row=0)
        f_dates_b1.grid_propagate(False)

        del_date_val = tk.StringVar(f_dates_b1, value=self.config.get_val("year_cutoff"))
        ttk.Label(f_dates_b1, text="Rok usuwanych danych: ").grid(column=0, row=0)
        ttk.Label(f_dates_b1,textvariable=del_date_val).grid(column=1, row=0)
        del_date_entry = ttk.Spinbox(f_dates_b1, from_=2000, to=2100, width=15)
        del_date_entry.grid(column=0, row=1)
        del_date_entry.insert(0, del_date_val.get())
        ttk.Button(f_dates_b1, width=15, text="Ustaw", command=lambda: GUI.set_date_var(self.root, del_date_entry, del_date_val)).grid(column=1, row=1)

        # Source date subframe - testing selector functionality
        f_dates_b2 = tk.Frame(f_dates, height=100, width=400, highlightbackground=self.border_color, highlightthickness=1)
        f_dates_b2.grid(column=1, row=0)
        f_dates_b2.grid_propagate(False)
        
        src_date_val = tk.StringVar(f_dates_b2, value=self.config.get_val("year_print"))
        ttk.Label(f_dates_b2,text="Rok wykonania raportu: ").grid(column=0, row=0)
        ttk.Label(f_dates_b2,textvariable=src_date_val).grid(column=1, row=0)
        src_date_entry = ttk.Spinbox(f_dates_b2, from_=2000, to=2100, width=15)
        src_date_entry.grid(column=0, row=1)
        src_date_entry.insert(0, src_date_val.get())
        # ttk.Button(f_main_3_b2, width=10, text="Ustaw", command=lambda: src_date_val.set(src_date_entry.get())).grid(column=0, row=2)
        ttk.Button(f_dates_b2, width=15, text="Ustaw", command=lambda: GUI.set_date_var(self.root, src_date_entry, src_date_val)).grid(sticky="W", column=1, row=1)

        # Form handling buttons
        f_main_4 = tk.Frame(f_main, height=100, width=800)
        f_main_4.grid(column=0, row=3)
        f_main_4.grid_propagate(False)

        ttk.Button(f_main_4, text="Uruchom", command=self.run_main_compute).grid(column=0, row=0)

        self.del_path_var = s_del_path
        self.raport_path_var = s_raport_path
        self.src_date_val = src_date_val
        self.del_date_val = del_date_val

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
            self.bot.main_compute(
                raport_path=self.raport_path_var.get(),
                del_list_path=self.del_path_var.get(),
                print_year=self.src_date_val.get(),
                cutoff_year=self.del_date_val.get()
            )