from datetime import datetime
from tkinter import filedialog
from tkinter import Tk
import pandas as pd
import time
import os

root = Tk()
# root.withdraw()

filename = filedialog.askopenfilename(filetypes=[("Plik CSV", "*.csv")])
zgony_file = "zgony_final.csv"

start_time = time.time()
try:  
    print("Ładowanie pliku: " + filename)
    ws = pd.read_csv(filename, sep=";", dtype="str", encoding="windows-1250", header=None)
except FileNotFoundError:
    print("[ERR] Wskazany plik nie istnieje!")
    exit()
try:
    print("Ładowanie pliku:", zgony_file)
    zgony = pd.read_csv(zgony_file, sep=",", dtype="str", header=None)
except FileNotFoundError:
    print("[ERR] Nie znaleziono pliku zgonów!")
    exit()

print("File loaded successfully")

master_list = []
ban_list = []
error_count = 0
cutoff_year = "2017"
print_year = "2023"

for i in range(len(ws)):
    pesel, patient, contact_date = ws[0][i], ws[1][i], ws[2][i]
    try:
        print(str(i) + ": " + pesel + " " + patient + " " + contact_date)
        data = [pesel, patient]
    except TypeError:
        error_count += 1
        continue

    # Get all contacts from 2017
    if cutoff_year + "-01-01" <= contact_date <= cutoff_year + "-12-31":
        if data not in master_list and pesel not in zgony[0].values:
            master_list.append(data)
    # Get contacts more recent than 2017
    elif contact_date > cutoff_year + "-12-31":
        if data not in ban_list:
            ban_list.append(data)

for i in range(len(ban_list)):
    if ban_list[i] in master_list:
        master_list.pop(master_list.index(ban_list[i]))

master_df = pd.DataFrame(data=master_list, columns=["PESEL", "Pacjent"])
master_df[['Imię', 'Nazwisko']] = master_df.Pacjent.str.split(" ", 1, expand=True)
del master_df["Pacjent"]

master_df[["Znak teczki", "Data ostatniej wizyty", "Kategoria akt", "Liczba teczek",
           "Miejsce przechowania akt", "Data przekazania"]] = ["5110", cutoff_year+" r.", "B 20", "", "", "30.06."+print_year]
master_df.sort_values(by=['Nazwisko'], inplace=True)
master_df.reset_index(drop=True, inplace=True)
master_df.index += 1
print(master_df)

now = datetime.now()
curtime = now.strftime("%d-%m_%H%M%S")
print("--- Zadanie wykonane, czas pracy: %s seconds ---" % (time.time() - start_time))
if error_count > 0:
    print("--- Błędy odczytu danych: " + str(error_count))

sav_name = "output-" + curtime + ".xlsx"
try:
    target = filedialog.asksaveasfilename(filetypes=[("Plik Excel 2007-365", "*.xlsx")],
                                          defaultextension=".xlsx", initialfile=sav_name)
    master_df.to_excel(target)
    print("--- Zapisano plik: " + target)
    os.startfile(target)
except ValueError:
    print("Nie wybrano prawidłowego miejsca zapisu pliku.")
