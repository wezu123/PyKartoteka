import pandas as pd
import time, os
import logging
from tkinter import filedialog
from datetime import datetime
from static.gui import GUI

class Bot:
    def __init__(self, config, root, default=False) -> None:
        self.config = config
        self.root = root.root
        self.logger = logging.getLogger(__name__)

    def main_compute(self, raport_path=None, del_list_path=None, print_year=None, cutoff_year=None, from_config=False):
        if from_config:
            self.raport_path = self.config.get_val("path_raport_file")
            self.del_list_path = self.config.get_val("path_del_file")
            self.print_year = self.config.get_val("year_print")
            self.cutoff_year = self.config.get_val("year_cutoff")
        else:
            self.raport_path = raport_path
            self.del_list_path = del_list_path
            self.print_year = print_year
            self.cutoff_year = cutoff_year

        start_time = time.time()

        self.logger.info("Uruchomiono zadanie z parametrami:")
        self.logger.info(f"Raport path: {self.raport_path}")
        self.logger.info(f"Del list path: {self.del_list_path}")
        self.logger.info(f"Print year: {self.print_year}")
        self.logger.info(f"Cutoff year: {self.cutoff_year}")

        try:
            raport_data, del_list = self.read_compute_data(self.raport_path, self.del_list_path)
        except FileNotFoundError:
            self.logger.exception("Nie można kontynuować bez poprawnych danych wejściowych!")
            return

        try:
            master_list, error_count = self.find_obsolete_records(raport_data, del_list)
            master_df = self.format_dataframe(master_list)
        except (ValueError, KeyError) as e:
            GUI.draw_info_box(self.root, "[ERR] Format przekazanych danych jest nieprawidłowy!")
            self.logger.exception("Format przekazanych danych jest nieprawidłowy!")
            return

        self.logger.info(f'Zadanie wykonane, czas pracy: {time.time() - start_time}s')
        GUI.draw_info_box("--- Zadanie wykonane, czas pracy: %s seconds ---" % (time.time() - start_time))
        if error_count > 0:
            self.logger.warning(f'Błędy odczytu danych: {str(error_count)}')
            GUI.draw_info_box(self.root, "Błędy odczytu danych: " + str(error_count))

        self.save_result_excel(master_df)


    def read_compute_data(self, raport_path, del_list_path):
        try:  
            self.logger.info("Ładowanie pliku: " + raport_path)
            raport_data = pd.read_csv(raport_path, sep=";", dtype="str", encoding="windows-1250", header=None)
        except FileNotFoundError:
            GUI.draw_info_box(self.root, "[ERR] Wskazany plik nie istnieje!")
            self.logger.exception("Wskazany plik nie istnieje!")
            raise FileNotFoundError
        self.logger.info("Dane raportowe załadowane pomyślnie")

        try:
            self.logger.info("Ładowanie pliku: " + del_list_path)
            del_list = pd.read_csv(del_list_path, sep=",", dtype="str", header=None)
        except FileNotFoundError:
            GUI.draw_info_box(self.root, "[ERR] Nie znaleziono pliku zgonów!")
            self.logger.exception("Nie znaleziono pliku zgonów!")
            raise FileNotFoundError
        self.logger.info("Dane zgonów załadowane pomyślnie")

        return raport_data, del_list


    def find_obsolete_records(self, raport_data, del_list):
        ### COMPUTE RAPORT DATA ###
        master_list = []
        ban_list = []
        error_count = 0

        for i in range(len(raport_data)):
            pesel, patient, contact_date = raport_data[0][i], raport_data[1][i], raport_data[2][i]
            try:
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

            GUI.draw_info_box(self.root, "Zapisano plik: " + target)
            self.logger.info("Zapisano plik: " + target)
            os.startfile(target)
        except ValueError:
            GUI.draw_info_box(self.root, "[ERR] Nie wybrano prawidłowego miejsca zapisu pliku!")
            self.logger.exception("Nie wybrano prawidłowego miejsca zapisu pliku!")

