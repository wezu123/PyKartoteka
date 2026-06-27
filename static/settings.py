#TODO
import logging
from tkinter import ttk
import tkinter as tk
from static.gui import GUI

class Settings:
    def __init__(self, root, config):
        self.config = config
        self.root = root
        self.logger = logging.getLogger(__name__)

    def draw_settings(self):
        # Create a frame for the settings
        #GUI.destroy_children(self.root, 1)

        f_settings = tk.Frame(self.root, height=400, width=800, highlightbackground="lightgrey", highlightthickness=1, bg="lightblue")
        f_settings.grid(column=1, row=0)
        f_settings.grid_propagate(False)

        # Add settings options here (e.g., entries, checkboxes, etc.)
        ttk.Label(f_settings, text="Ustawienia aplikacji").grid(column=0, row=0, pady=10)
        self.example = GUI.draw_path_subframe(f_settings, col=0, row=1, label_text="Ścieżka do raportu:", path=self.config.get_val("path_last_load"))
        self.year_print = GUI.draw_date_subframe(f_settings, col=0, row=3, label_text="Rok do wydruku:", year=self.config.get_val("year_print"))

        v_scrollbar = ttk.Scrollbar(f_settings, orient="vertical")
        v_scrollbar.grid(column=1, row=0, sticky="ens")

 