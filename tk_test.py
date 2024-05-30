import tkinter as tk

nr = 1
def test():
    global nr
    nr += 1
    print(nr)
    label1 = tk.Label(root, text="Counter = "+str(nr))
    label1.grid(column=0, row=0)

root = tk.Tk()
label1 = tk.Label(root, text="Counter = "+str(nr))
# label2 = tk.Label(root, text="Moje imię to Mateusz.")
button = tk.Button(root, text="Add +1", command=test, padx=10, fg="white", bg="blue")


label1.grid(column=0, row=0)
button.grid(column=0, row=1)
# label2.grid(column=1, row=1)

root.mainloop()