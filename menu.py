import tkinter.filedialog
import tkinter as tk
from run import Run

class MainMenu:
    def __init__(self, n, v):
        self.name = n
        self.version = v
        self.root = tk.Tk()

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
            tk.Button(f_menu, text="dev.run_default", command=exit),
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

        f_main_3 = tk.Frame(f_main, height=100, width=800, bg="pink", highlightbackground="black", highlightthickness=1).grid(column=0, row=2)

    def start_help(self):
        f_main = tk.Frame(self.root, height=400, width=800, bg="red")
        f_main.grid(column=1, row=0)