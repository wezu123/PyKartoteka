import tkinter.filedialog
import tkinter as tk
from tkinter import ttk
from run import Run

class MainMenu:
    def __init__(self, config):
        self.config = config    # Get running config from main
        # self.name = self.config["app_name"]
        self.name = self.config.get_val("app_name")
        self.version = self.config.get_val("app_version")
        self.root = tk.Tk()
        self.run = Run(self.config, self) # Start Run with running config and menu instances

        self.border_color = "lightgrey"
        self.year_low = 2000
        self.year_high = 2100

    def get_open_path(self, stringvar=None):
        path = tkinter.filedialog.askopenfilename(filetypes=[("Plik CSV", "*.csv")])
        if path:
            if stringvar:
                stringvar.set(path)
            return path
        return

    def start_window(self):
        self.root.title(self.name + " " + self.version)
        self.root.resizable(False, False)
        #Declare all frames and grid them
        f_menu = tk.Frame(self.root, height=400, width=150, highlightbackground=self.border_color, highlightthickness=1)
        f_menu.grid(column=0, row=0, sticky="n")
        f_menu.pack_propagate(False)

        ttk.Label(f_menu, text=self.name).pack(pady=10)
        menu_buttons = [
            ttk.Button(f_menu, text="Start", command=self.start_main),
            ttk.Button(f_menu, text="Ustawienia", command=self.start_settings),
            ttk.Button(f_menu, text="dev.run_default", command=self.run.main_compute),
            ttk.Button(f_menu, text="dev.run_info", command=self.show_info_box),
            ttk.Button(f_menu, text="Pomoc", command=self.start_help)
        ]
        for button in menu_buttons:
            button.pack()
            button.config(width=25) 
        exit_btn = ttk.Button(f_menu, text="Wyjdź", command=exit)
        exit_btn.pack(side="bottom")
        exit_btn.config(width=20) 

        self.start_main() 
        self.root.mainloop()

    def start_main(self):
        # Main Parent frame
        f_main = tk.Frame(self.root, height=400, width=800, bg="red")
        f_main.grid(column=1, row=0)
        f_main.grid_propagate(False)
        # f_menu.grid_propagate(False)

        # Delete Data Frame
        f_main_1 = tk.Frame(f_main, height=100, width=800, border=10, highlightbackground=self.border_color, highlightthickness=1)
        f_main_1.grid(column=0, row=0)
        f_main_1.grid_propagate(False)
        ttk.Label(f_main_1, text="Lokalizacja pliku ze zgonami:").grid(column=0, row=0, sticky="W")
        e_main_1_val = tk.StringVar(value="C:\Windows\System32")
        e_main_1 = ttk.Entry(f_main_1, width=100, state="readonly", textvariable=e_main_1_val)
        e_main_1.grid(column=0, row=1)
        ttk.Button(f_main_1, text="Przeglądaj...", command=lambda: self.get_open_path(e_main_1_val)).grid(column=1,row=1)

        # Source Data Frame
        f_main_2 = tk.Frame(f_main, height=100, width=800, border=10, highlightbackground=self.border_color, highlightthickness=1)
        f_main_2.grid(column=0, row=1)
        f_main_2.grid_propagate(False)
        ttk.Label(f_main_2, text="Lokalizacja raportu KS-Somed:").grid(column=0, row=0, sticky="W")
        e_main_2_val = tk.StringVar()
        ttk.Entry(f_main_2, width=100, textvariable=e_main_2_val).grid(column=0, row=1)
        ttk.Button(f_main_2, text="Przeglądaj...", command=lambda: self.get_open_path(e_main_2_val)).grid(column=1,row=1)

        # Date Selectors Frame and Subframes
        f_main_3 = tk.Frame(f_main, height=100, width=800)
        f_main_3.grid(column=0, row=2)
        f_main_3.grid_propagate(False)
        # Delete date subframe - incomplete
        f_main_3_b1 = tk.Frame(f_main_3, height=100, width=400, highlightbackground=self.border_color, highlightthickness=1)
        f_main_3_b1.grid(column=0, row=0)
        f_main_3_b1.grid_propagate(False)
        del_date_val = tk.StringVar(f_main_3_b1, value=self.config.get_val("year_cutoff"))
        ttk.Label(f_main_3_b1, text="Rok usuwanych danych: ").grid(column=0, row=0)
        ttk.Label(f_main_3_b1,textvariable=del_date_val).grid(column=1, row=0)
        del_date_entry = ttk.Spinbox(f_main_3_b1, from_=2000, to=2100, width=15)
        del_date_entry.grid(column=0, row=1)
        del_date_entry.insert(0, del_date_val.get())
        ttk.Button(f_main_3_b1, width=15, text="Ustaw", command=lambda: self.set_date_var(del_date_entry, del_date_val)).grid(column=1, row=1)
        # Source date subframe - testing selector functionality
        f_main_3_b2 = tk.Frame(f_main_3, height=100, width=400, highlightbackground=self.border_color, highlightthickness=1)
        f_main_3_b2.grid(column=1, row=0)
        f_main_3_b2.grid_propagate(False)
        src_date_val = tk.StringVar(f_main_3_b2, value=self.config.get_val("year_print"))
        ttk.Label(f_main_3_b2,text="Rok wykonania raportu: ").grid(column=0, row=0)
        ttk.Label(f_main_3_b2,textvariable=src_date_val).grid(column=1, row=0)
        src_date_entry = ttk.Entry(f_main_3_b2, width=15)
        src_date_entry.grid(column=0, row=1)
        src_date_entry.insert(0, src_date_val.get())
        # ttk.Button(f_main_3_b2, width=10, text="Ustaw", command=lambda: src_date_val.set(src_date_entry.get())).grid(column=0, row=2)
        ttk.Button(f_main_3_b2, width=15, text="Ustaw", command=lambda: self.set_date_var(src_date_entry, src_date_val)).grid(sticky="W", column=1, row=1)

    # Example Function to showcase inplace frame changes
    def start_help(self):
        f_main = tk.Frame(self.root, height=400, width=800, bg="red")
        f_main.grid(column=1, row=0)
    def start_settings(self):
        f_main = tk.Frame(self.root, height=400, width=800, bg="green")
        f_main.grid(column=1, row=0)
    # Placeholder for future function, will be used to run main_compute with default params when UI is functional
    def run_default(self):
        pass

    # Example function for displaying messages in windows
    def show_info_box(self, msg="This is a debug window... what are you doing here?"):
        info_box = tk.Toplevel(self.root, takefocus=1)
        x, y = self.root.winfo_x(), self.root.winfo_y()
        info_box.geometry("+%d+%d" % (x+300, y+150))
        info_box.resizable(False, False)
        info_box.grab_set()

        ttk.Label(info_box, text=msg).grid(column=0, row=0, padx=20, pady=20)
        f_info_button = tk.Frame(info_box)
        f_info_button.grid(column=0, row=1)
        ttk.Button(f_info_button, text="OK", command=info_box.destroy).grid(column=0, row=0)

    def set_date_var(self, entry, var):
        entry_val = entry.get()
        
        try:
            entry_val = int(entry_val)
            if(not(self.year_low <= entry_val <= self.year_high)):
                entry.delete(0, tk.END)
                entry.insert(0, var.get())
                print("[ERR] Value not in range")
                return 0
        except ValueError:
            entry.delete(0, tk.END)
            entry.insert(0, var.get())
            print("[ERR] Incorrect value")
            return 0
        
        var.set(entry_val)
        print(var.get())