import tkinter as tk

#Declare root
root = tk.Tk()
root.title("Menu testowe")
root.resizable(False, False)
#Declare all frames and grid them
f_buttons = tk.Frame(root, height=400, width=200, bg="blue")
f_main = tk.Frame(root, height=400, width=800, bg="red")
f_buttons.grid(column=0, row=0, sticky="n")
f_main.grid(column=1, row=0)

tk.Label(f_buttons, text="SPZOZ1 - Karty").pack(pady=20)
control_buttons = [
    tk.Button(f_buttons, text="Button 1"),
    tk.Button(f_buttons, text="Button 2"),
    tk.Button(f_buttons, text="Button 3"),
    tk.Button(f_buttons, text="Button 4"),
    tk.Button(f_buttons, text="Exit", command=exit),
]
for button in control_buttons:
    button.pack(anchor="s")

root.mainloop()