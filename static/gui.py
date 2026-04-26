from tkinter import ttk
import os.path
import logging as log

class GUI:
    def get_open_path(tk, stringvar=None):
        logger = log.getLogger(__name__)
        open_path = tk.filedialog.askopenfilename(filetypes=[("Plik CSV", "*.csv")])
        if os.path.isfile():
            if stringvar:
                stringvar.set(open_path)
            return open_path
        logger.error("Specified path does not point to a file!")
        return False

    # Example function for displaying messages in windows
    def draw_info_box(tk, msg="This is a debug window... what are you doing here?"):
        info_box = tk.Toplevel(tk.root, takefocus=1)
        x, y = tk.root.winfo_x(), tk.root.winfo_y()
        info_box.geometry("+%d+%d" % (x+300, y+150))
        info_box.resizable(False, False)
        info_box.grab_set()

        ttk.Label(info_box, text=msg).grid(column=0, row=0, padx=20, pady=20)
        f_info_button = tk.Frame(info_box)
        f_info_button.grid(column=0, row=1)
        ttk.Button(f_info_button, text="OK", command=info_box.destroy).grid(column=0, row=0)

        def infobox_log(self, record):
        GUI.draw_info_box(self.root, f'[{record.levelname}] {record.getMessage()}')
        return True

    def set_date_var(tk, entry, var, year_low=2000, year_high=2100):
        logger = log.getLogger(__name__)
        entry_val = entry.get()
        
        try:
            entry_val = int(entry_val)
            if(not(year_low <= entry_val <= year_high)):
                entry.delete(0, tk.END)
                entry.insert(0, var.get())
                logger.error("Value not in range!")
                return 0
        except ValueError:
            entry.delete(0, tk.END)
            entry.insert(0, var.get())
            logger.error("Incorrect value!")
            return 0
        
        var.set(entry_val)
        print(var.get())