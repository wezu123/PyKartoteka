from tkinter import filedialog
from datetime import datetime
import pandas as pd
import time, os
import logging as log
from static.gui import GUI

class Run:
    def __init__(self, config, i_menu) -> None:
        self.config = config
        self.i_menu = i_menu

        self.logger = log.getLogger(__name__)

    def main_compute(self):
        raport_path = filedialog.askopenfilename(filetypes=[("Plik CSV", "*.csv")])
        del_list_path = self.config.get_val("path_del_file")
        self.cutoff_year = self.config.get_val("year_cutoff")
        self.print_year = self.config.get_val("year_print")

        start_time = time.time()

        raport_data, del_list = self.read_compute_data(raport_path, del_list_path)
        master_list, error_count = self.find_obsolete_records(raport_data, del_list)
        master_df = self.format_dataframe(master_list)

        now = datetime.now()
        self.logger.info(f'Zadanie wykonane, czas pracy: {time.time() - start_time}s')
        # GUI.draw_info_box("--- Zadanie wykonane, czas pracy: %s seconds ---" % (time.time() - start_time))
        if error_count > 0:
            self.logger.warning(f'Błędy odczytu danych: {str(error_count)}')
            GUI.draw_info_box("Błędy odczytu danych: " + str(error_count))

        self.save_result_excel(master_df)


    def read_compute_data(self, raport_path, del_list_path):
        try:  
            print("Ładowanie pliku: " + raport_path)
            raport_data = pd.read_csv(raport_path, sep=";", dtype="str", encoding="windows-1250", header=None)
        except FileNotFoundError:
            GUI.show_info_box("[ERR] Wskazany plik nie istnieje!")
            return 0
            # print("[ERR] Wskazany plik nie istnieje!")
            # exit()
        try:
            print("Ładowanie pliku:", del_list_path)
            del_list = pd.read_csv(del_list_path, sep=",", dtype="str", header=None)
        except FileNotFoundError:
            GUI.show_info_box("[ERR] Nie znaleziono pliku zgonów!")
            return 0
            # print("[ERR] Nie znaleziono pliku zgonów!")
            # exit()
        print("File loaded successfully")

        return raport_data, del_list


    def find_obsolete_records(self, raport_data, del_list):
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
            if self.cutoff_year + "-01-01" <= contact_date <= self.cutoff_year + "-12-31":
                if data not in master_list and pesel not in del_list[0].values:
                    master_list.append(data)
            # Get contacts more recent than cutoff year
            elif contact_date > self.cutoff_year + "-12-31":
                if data not in ban_list:
                    ban_list.append(data)

        for i in range(len(ban_list)):
            if ban_list[i] in master_list:
                master_list.pop(master_list.index(ban_list[i]))

        return master_list, error_count


    def format_dataframe(self, master_list):
        ### EXCEL FORMATTING ###
        master_df = pd.DataFrame(data=master_list, columns=["PESEL", "Pacjent"])
        master_df[['Imię', 'Nazwisko']] = master_df.Pacjent.str.split(pat=" ", n=1, expand=True)
        del master_df["Pacjent"]

        master_df[["Znak teczki", "Data ostatniej wizyty", "Kategoria akt", "Liczba teczek",
                "Miejsce przechowania akt", "Data przekazania"]] = ["5110", self.cutoff_year+" r.", "B 20", "", "", "30.06."+self.print_year]
        master_df.sort_values(by=['Nazwisko'], inplace=True)
        master_df.reset_index(drop=True, inplace=True)
        master_df.index += 1

        return master_df


    def save_result_excel(self, master_df):
        ### SAVING RESULT ###
        sav_name = "output-" + datetime.now().strftime("%d-%m_%H%M%S") + ".xlsx"
        try:
            target = filedialog.asksaveasfilename(filetypes=[("Plik Excel 2007-365", "*.xlsx")],
                                                defaultextension=".xlsx", initialfile=sav_name)
            master_df.to_excel(target)
            # print("--- Zapisano plik: " + target)
            GUI.draw_info_box("Zapisano plik: " + target)
            os.startfile(target)
        except ValueError:
            GUI.draw_info_box("[ERR] Nie wybrano prawidłowego miejsca zapisu pliku!")
            # print("Nie wybrano prawidłowego miejsca zapisu pliku.")

