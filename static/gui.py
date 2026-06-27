from tkinter import ttk
import tkinter as tk
import os.path
import logging

logger = logging.getLogger(__name__)

class GUI:
    border_color = "lightgrey"

    def get_open_path(root, stringvar=None):
        open_path = tk.filedialog.askopenfilename(filetypes=[("Plik CSV", "*.csv")])
        if os.path.isfile(open_path):
            if stringvar:
                stringvar.set(open_path)
            return open_path
        GUI.logger.error("Specified path does not point to a file!")
        return False

    # Example function for displaying messages in windows
    def draw_info_box(root, msg="This is a debug window... what are you doing here?"):
        info_box = tk.Toplevel(root, takefocus=1)
        x, y = root.winfo_x(), root.winfo_y()
        info_box.geometry("+%d+%d" % (x+300, y+150))
        info_box.resizable(False, False)
        info_box.grab_set()

        ttk.Label(info_box, text=msg).grid(column=0, row=0, padx=20, pady=20)
        f_info_button = tk.Frame(info_box)
        f_info_button.grid(column=0, row=1)
        ttk.Button(f_info_button, text="OK", command=info_box.destroy).grid(column=0, row=0)

    def draw_path_subframe(root, col, row, label_text="Ścieżka:", stringvar=None, path="", readonly=False):
        frame = tk.Frame(root, height=100, width=800, border=10, highlightbackground=GUI.border_color, highlightthickness=1)
        frame.grid(column=col, row=row)
        frame.grid_propagate(False)

        ttk.Label(frame, text=label_text).grid(column=0, row=0, sticky="W")
        stringvar = tk.StringVar(value=path)
        entry = ttk.Entry(frame, width=100, textvariable=stringvar)
        entry.grid(column=0, row=1)
        entry.config(state="readonly" if readonly else "normal")

        ttk.Button(frame, text="Przeglądaj...", command=lambda: GUI.get_open_path(root, stringvar)).grid(column=1,row=1)

        return stringvar

    def draw_date_subframe(root, col, row,label_text="Rok:", stringvar=None, year=""):
        frame = tk.Frame(root, height=100, width=400, borderwidth=10,)
        frame.grid(column=col, row=row)
        frame.grid_propagate(False)

        stringvar = tk.StringVar(frame, value=year)
        ttk.Label(frame, text=label_text).grid(column=0, row=0)
        ttk.Label(frame,textvariable=stringvar).grid(column=1, row=0)

        entry = ttk.Spinbox(frame, from_=2000, to=2100, width=15)
        entry.grid(column=0, row=1)
        entry.insert(0, stringvar.get())

        ttk.Button(frame, width=15, text="Ustaw", command=lambda: GUI.set_date_var(entry, stringvar)).grid(column=1, row=1)

        return stringvar

    def draw_loading(root, msg="Ładowanie..."):
        pass #TODO: Implement loading screen

    def infobox_log(self, record):
        GUI.draw_info_box(self.root, f'[{record.levelname}] {record.getMessage()}')
        return True

    def destroy_children(frame, nr=-1):
        if nr > -1:
            children = frame.winfo_children()
            if nr < len(children):
                children[nr].destroy()
            return
        for child in frame.winfo_children():
            child.destroy()

    def set_date_var(entry, var, year_low=2000, year_high=2100):
        entry_val = entry.get()
        
        try:
            entry_val = int(entry_val)
            if(not(year_low <= entry_val <= year_high)):
                entry.delete(0, tk.END)
                entry.insert(0, var.get())
                GUI.logger.error("Date value not in range for entry " + entry._name + "!")
                return 0
        except ValueError:
            entry.delete(0, tk.END)
            entry.insert(0, var.get())
            GUI.logger.error("Incorrect value for entry " + entry._name + "! Integer expected.")
            return 0
        
        var.set(entry_val)
        print(var.get())