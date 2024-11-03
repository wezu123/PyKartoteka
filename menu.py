import tkinter.filedialog
import tkinter as tk
from run import Run

class MainMenu:
    def __init__(self, config):
        self.config = config
        self.name = self.config["app_name"]
        self.version = self.config["app_version"]
        self.root = tk.Tk()
        self.run = Run(self.config, self)

    def get_open_path(self, stringvar=None):
        path = tkinter.filedialog.askopenfilename(filetypes=[("Plik CSV", "*.csv")])
        if path:
            if stringvar:
                stringvar.set(path)
            return path
        return

    def start_window(self):
        # root = tk.Tk()
        self.root.title(self.name + " " + self.version)
        self.root.resizable(False, False)
        #Declare all frames and grid them
        f_menu = tk.Frame(self.root, height=400, width=200, bg="blue", highlightbackground="black", highlightthickness=1)
        f_menu.grid(column=0, row=0, sticky="n")

        tk.Label(f_menu, text=self.name).pack(pady=20)
        menu_buttons = [
            tk.Button(f_menu, text="Start", command=self.start_main),
            tk.Button(f_menu, text="Pomoc", command=self.start_help),
            tk.Button(f_menu, text="dev.run_default", command=self.run.main_compute),
            tk.Button(f_menu, text="dev.run_info", command=self.show_info_box),
            tk.Button(f_menu, text="Wyjdź", command=exit),
        ]
        for button in menu_buttons:
            button.pack(anchor="s")
            button.config(width=20)

        self.start_main() 
        self.root.mainloop()

    def start_main(self):
        f_main = tk.Frame(self.root, height=400, width=800, bg="red")
        f_main.grid(column=1, row=0)
        # f_main.grid_propagate(False)
        # f_menu.grid_propagate(False)

        f_main_1 = tk.Frame(f_main, height=100, width=800, border=10, highlightbackground="black", highlightthickness=1, bg="yellow")
        f_main_1.grid(column=0, row=0)
        f_main_1.grid_propagate(False)
        tk.Label(f_main_1, text="Lokalizacja pliku ze zgonami:").grid(column=0, row=0, sticky="W")
        e_main_1_val = tk.StringVar(value="C:\Windows\System32")
        e_main_1 = tk.Entry(f_main_1, width=100, state="readonly", textvariable=e_main_1_val)
        e_main_1.grid(column=0, row=1)
        tk.Button(f_main_1, text="Przeglądaj...", command=lambda: self.get_open_path(e_main_1_val)).grid(column=1,row=1)

        f_main_2 = tk.Frame(f_main, height=100, width=800, border=10, highlightbackground="black", highlightthickness=1)
        f_main_2.grid(column=0, row=1)
        f_main_2.grid_propagate(False)
        tk.Label(f_main_2, text="Lokalizacja raportu KS-Somed:").grid(column=0, row=0, sticky="W")
        e_main_2_val = tk.StringVar()
        tk.Entry(f_main_2, width=100, textvariable=e_main_2_val).grid(column=0, row=1)
        tk.Button(f_main_2, text="Przeglądaj...", command=lambda: self.get_open_path(e_main_2_val)).grid(column=1,row=1)

        f_main_3 = tk.Frame(f_main, height=100, width=800, bg="pink", highlightbackground="black", highlightthickness=1)
        f_main_3.grid(column=0, row=2)
        f_main_3_b1 = tk.Frame(f_main_3, height=100, width=400, bg="orange", highlightbackground="black", highlightthickness=1)
        f_main_3_b1.grid(column=0, row=0)
        f_main_3_b2 = tk.Frame(f_main_3, height=100, width=400, bg="purple", highlightbackground="black", highlightthickness=1)
        f_main_3_b2.grid(column=1, row=0)

    def start_help(self):
        f_main = tk.Frame(self.root, height=400, width=800, bg="red")
        f_main.grid(column=1, row=0)

    def show_info_box(self, msg="This is a debug window... what are you doing here?"):
        info_box = tk.Toplevel(self.root)
        info_box.grab_set()

        tk.Label(info_box, text=msg).grid(column=0, row=0, padx=20, pady=20)
        f_info_button = tk.Frame(info_box)
        f_info_button.grid(column=0, row=1)
        tk.Button(f_info_button, text="OK", command=info_box.destroy).grid(column=0, row=0)

    def run_default(self):
        pass