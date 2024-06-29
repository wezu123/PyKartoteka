import tkinter as tk

class MainMenu:
    def __init__(self, n, v):
        self.name = n
        self.version = v

    def startMainMenu(self):
        root = tk.Tk()
        root.title(self.name + " " + self.version)
        root.resizable(False, False)
        #Declare all frames and grid them
        f_buttons = tk.Frame(root, height=400, width=200, bg="blue")
        f_main = tk.Frame(root, height=400, width=800, bg="red")
        f_buttons.grid(column=0, row=0, sticky="n")
        f_main.grid(column=1, row=0)

        tk.Label(f_buttons, text=self.name).pack(pady=20)
        control_buttons = [
            tk.Button(f_buttons, text="Start"),
            tk.Button(f_buttons, text="Pomoc"),
            tk.Button(f_buttons, text="Wyjdź", command=exit),
        ]
        for button in control_buttons:
            button.pack(anchor="s")

        root.mainloop()