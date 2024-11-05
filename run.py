from tkinter import filedialog
from datetime import datetime
import time, os
import pandas as pd

class Run:
    def __init__(self, config, i_menu) -> None:
        self.config = config
        self.i_menu = i_menu

    def main_compute(self):
        raport_path = filedialog.askopenfilename(filetypes=[("Plik CSV", "*.csv")])
        del_list_path = self.config.get_val("path_del_file")
        cutoff_year = self.config.get_val("year_cutoff")
        print_year = self.config.get_val("year_print")

        start_time = time.time()
        try:  
            print("Ładowanie pliku: " + raport_path)
            raport_data = pd.read_csv(raport_path, sep=";", dtype="str", encoding="windows-1250", header=None)
        except FileNotFoundError:
            self.i_menu.show_info_box("[ERR] Wskazany plik nie istnieje!")
            return 0
            # print("[ERR] Wskazany plik nie istnieje!")
            # exit()
        try:
            print("Ładowanie pliku:", del_list_path)
            del_list = pd.read_csv(del_list_path, sep=",", dtype="str", header=None)
        except FileNotFoundError:
            self.i_menu.show_info_box("[ERR] Nie znaleziono pliku zgonów!")
            return 0
            # print("[ERR] Nie znaleziono pliku zgonów!")
            # exit()
        print("File loaded successfully")

        ### COMPUTE RAPORT DATA ###
        master_list = []
        ban_list = []
        error_count = 0

        for i in range(len(raport_data)):
            pesel, patient, contact_date = raport_data[0][i], raport_data[1][i], raport_data[2][i]
            try:
                # print(str(i) + ": " + pesel + " " + patient + " " + contact_date)
                data = [pesel, patient]
            except TypeError:
                error_count += 1
                continue

            # Get all contacts from cutoff year
            if cutoff_year + "-01-01" <= contact_date <= cutoff_year + "-12-31":
                if data not in master_list and pesel not in del_list[0].values:
                    master_list.append(data)
            # Get contacts more recent than cutoff year
            elif contact_date > cutoff_year + "-12-31":
                if data not in ban_list:
                    ban_list.append(data)

        for i in range(len(ban_list)):
            if ban_list[i] in master_list:
                master_list.pop(master_list.index(ban_list[i]))

        ### EXCEL FORMATTING ###
        master_df = pd.DataFrame(data=master_list, columns=["PESEL", "Pacjent"])
        master_df[['Imię', 'Nazwisko']] = master_df.Pacjent.str.split(pat=" ", n=1, expand=True)
        del master_df["Pacjent"]

        master_df[["Znak teczki", "Data ostatniej wizyty", "Kategoria akt", "Liczba teczek",
                "Miejsce przechowania akt", "Data przekazania"]] = ["5110", cutoff_year+" r.", "B 20", "", "", "30.06."+print_year]
        master_df.sort_values(by=['Nazwisko'], inplace=True)
        master_df.reset_index(drop=True, inplace=True)
        master_df.index += 1

        ### BENCHMARK END ###
        now = datetime.now()
        curtime = now.strftime("%d-%m_%H%M%S")
        # print("--- Zadanie wykonane, czas pracy: %s seconds ---" % (time.time() - start_time))
        self.i_menu.show_info_box("--- Zadanie wykonane, czas pracy: %s seconds ---" % (time.time() - start_time))
        if error_count > 0:
            print("--- Błędy odczytu danych: " + str(error_count))

        ### SAVING RESULT ###
        sav_name = "output-" + curtime + ".xlsx"
        try:
            target = filedialog.asksaveasfilename(filetypes=[("Plik Excel 2007-365", "*.xlsx")],
                                                defaultextension=".xlsx", initialfile=sav_name)
            master_df.to_excel(target)
            # print("--- Zapisano plik: " + target)
            self.i_menu.show_info_box("--- Zapisano plik: " + target)
            os.startfile(target)
        except ValueError:
            self.i_menu.show_info_box("[ERR] Nie wybrano prawidłowego miejsca zapisu pliku!")
            # print("Nie wybrano prawidłowego miejsca zapisu pliku.")

