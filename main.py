from tkinter import *

import tkintermapview

import tkinter as tk

from tkinter import END



class Worker:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __repr__(self):
        return f"Worker(name='{self.name}, surname='{self.surname}')"


class Shop:
    def __init__(self, name, location):
        self.name=name
        self.location=location
        self.coordinates= self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.name)
        self.workers: list[Worker] = []

    def __repr__(self):
        return f"Shop(name='{self.name}', workers={self.workers})"

    def add_worker(self, worker: Worker):
        self.workers.append(worker)


    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        address_url: str = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(address_url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude: float = float(response_html.select(".longitude")[1].text.replace(",", "."))

        latitude: float = float(response_html.select(".latitude")[1].text.replace(",", "."))

        return [latitude, longitude]


shops: list[Shop] = []




#SKLLLEPYYYYYY



# CREATE
def add_shop() -> None:
    nazwa = entry_shop_name.get()
    miejscowosc = entry_shop_location.get()
    if not nazwa or not miejscowosc:
        return

    tmp_shop = Shop(name=nazwa, location=miejscowosc)
    shops.append(tmp_shop)

    entry_shop_name.delete(0, END)
    entry_shop_location.delete(0, END)
    entry_shop_name.focus()

    show_shops()

# READ
def show_shops():
    listbox_lista_sklepow.delete(0, END)
    for I, shop in enumerate(shops):
        listbox_lista_sklepow.insert(END, f"{I + 1}. {shop.name}, {shop.location}")

# UPDATE
def update_shop():
    selection = listbox_lista_sklepow.curselection()
    if not selection:
        return
    idx = selection[0]

    name = entry_shop_name.get()
    location = entry_shop_location.get()

    shops[idx].name = name
    shops[idx].location = location

    shops[idx].marker.delete()
    shops[idx].coordinates = shops[idx].get_coordinates()
    shops[idx].marker = map_widget.set_marker(shops[idx].coordinates[0], shops[idx].coordinates[1], text=shops[idx].name)
    show_shops()

# DELETE
def delete_shop():
    selection = listbox_lista_sklepow.curselection()
    if not selection:
        return
    idx = selection[0]

    shops[idx].marker.delete()
    shops.pop(idx)
    show_shops()





#PRRRACOWNICYYYYYY


# CREATE
def add_worker():
    shop_selection = listbox_lista_sklepow.curselection()
    if not shop_selection:
        return
    name = entry_worker_name.get().strip()
    surname = entry_worker_surname.get().strip()
    if not name or not surname:
        return



    shop = shops[shop_selection[0]]
    new_worker = Worker(name, surname)
    shop.workers.append(new_worker)

    entry_worker_name.delete(0, END)
    entry_worker_surname.delete(0, END)

    show_workers(shop)



# READ
def show_workers(shop) -> None:
    listbox_lista_pracownikow.delete(0, END)
    for worker in shop.workers:
        listbox_lista_pracownikow.insert(END, f"{worker.name} {worker.surname}")


# UPDATE
def edit_worker():
    shop_selection = listbox_lista_sklepow.curselection()
    worker_selection = listbox_lista_pracownikow.curselection()
    if not shop_selection or not worker_selection:
        return

    shop_idx = shop_selection[0]
    worker_idx = worker_selection[0]

    shop = shops[shop_idx]

    new_name = entry_worker_name.get().strip()
    new_surname = entry_worker_surname.get().strip()
    if not new_name or not new_surname:
        return

    shop.workers[worker_idx].name = new_name
    shop.workers[worker_idx].surname = new_surname

    show_workers(shop)

    listbox_lista_pracownikow.selection_set(worker_idx)
    listbox_lista_pracownikow.activate(worker_idx)
    on_worker_select(None)





# DELETE
def delete_worker():
    shop_selection = listbox_lista_sklepow.curselection()
    worker_selection = listbox_lista_pracownikow.curselection()
    if not shop_selection or not worker_selection:
        return
    shop = shops[shop_selection[0]]
    # worker_idx = worker_selection[0]

    # Usuwamy pracownika
    del shop.workers[worker_selection[0]]

    # Aktualizujemy listę pracowników
    show_workers(shop)

    # Ustaw zaznaczenie na pierwszy pracownika lub wyczyść formularz jeśli brak pracowników
    if shop.workers:
        listbox_lista_pracownikow.selection_set(0)
        listbox_lista_pracownikow.activate(0)
        on_worker_select(None)
    else:
        entry_worker_name.delete(0, END)
        entry_worker_surname.delete(0, END)







def on_shop_select(_):
    selection = listbox_lista_sklepow.curselection()
    if not selection:
        return
    index = selection[0]
    shop = shops[index]

    entry_shop_name.delete(0, END)
    entry_shop_location.delete(0, END)
    entry_shop_name.insert(0, shop.name)
    entry_shop_location.insert(0, shop.location)

    show_workers(shop)

    entry_worker_name.delete(0, END)
    entry_worker_surname.delete(0, END)

def on_worker_select(_):
    shop_selection = listbox_lista_sklepow.curselection()
    worker_selection = listbox_lista_pracownikow.curselection()
    if not shop_selection or not worker_selection:
        return

    # Ponowne zaznaczenie sklepu (wymuszenie zachowania zaznaczenia sklepu)
    listbox_lista_sklepow.selection_clear(0, END)
    listbox_lista_sklepow.selection_set(shop_selection[0])
    listbox_lista_sklepow.activate(shop_selection[0])

    shop = shops[shop_selection[0]]
    worker = shop.workers[worker_selection[0]]

    entry_worker_name.delete(0, END)
    entry_worker_name.insert(0, worker.name)
    entry_worker_surname.delete(0, END)
    entry_worker_surname.insert(0, worker.surname)










#WYGLĄĄĄĄD


root = tk.Tk()
root.title("🛒 Zarządzanie sklepami")
root.geometry("1024x768")
root.configure(bg="#f0f0f0")

# Ustawienia siatki (kolumny responsywne)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# --- MAPA ---
ramka_mapa = LabelFrame(root, text="📍 Mapa", bg="#f0f0f0", font=("Helvetica", 10, "bold"))
ramka_mapa.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1024, height=400)
map_widget.set_position(52.23, 21)
map_widget.set_zoom(5)
map_widget.pack(fill="both", expand=True)

# --- SKLEPY ---
ramka_lista_sklepow = LabelFrame(root, text="🏬 Sklepy", padx=10, pady=10, bg="#f0f0f0")
ramka_lista_sklepow.grid(row=0, column=0, padx=10, pady=10)

listbox_lista_sklepow = Listbox(ramka_lista_sklepow, width=30, height=15)
listbox_lista_sklepow.pack()
listbox_lista_sklepow.bind("<<ListboxSelect>>", on_shop_select)

button_usun_sklep = Button(ramka_lista_sklepow, text="🗑 Usuń sklep", bg="#ff4d4d", fg="white", command=delete_shop)
button_usun_sklep.pack(pady=5)



# --- FORMULARZ SKLEPU ---
ramka_formularz_sklepow = LabelFrame(root, text="✏️ Formularz sklepu", padx=10, pady=10, bg="#f0f0f0")
ramka_formularz_sklepow.grid(row=0, column=1, padx=10, pady=10)

Label(ramka_formularz_sklepow, text="Nazwa:", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
entry_shop_name = Entry(ramka_formularz_sklepow)
entry_shop_name.grid(row=0, column=1, pady=5)

Label(ramka_formularz_sklepow, text="Lokalizacja:", bg="#f0f0f0").grid(row=1, column=0, sticky="w")
entry_shop_location = Entry(ramka_formularz_sklepow)
entry_shop_location.grid(row=1, column=1, pady=5)

button_dodaj_sklep = Button(ramka_formularz_sklepow, text="➕ Dodaj", bg="#4CAF50", fg="white", command=add_shop)
button_dodaj_sklep.grid(row=2, column=0, pady=10)

button_edytuj_sklep = Button(ramka_formularz_sklepow, text="💾 Zapisz edycję", command=update_shop)
button_edytuj_sklep.grid(row=2, column=1)

# --- PRACOWNICY ---
ramka_lista_pracownikow = LabelFrame(root, text="👤 Pracownicy", padx=10, pady=10, bg="#f0f0f0")
ramka_lista_pracownikow.grid(row=0, column=2, padx=10, pady=10)

listbox_lista_pracownikow = Listbox(ramka_lista_pracownikow, width=30, height=15)
listbox_lista_pracownikow.pack()
listbox_lista_pracownikow.bind("<<ListboxSelect>>", on_worker_select)

button_add_worker = Button(ramka_lista_pracownikow, text="➕ Dodaj", command=add_worker)
button_add_worker.pack(side="left", padx=5)

button_update_worker = Button(ramka_lista_pracownikow, text="✏️ Edytuj", command=edit_worker)
button_update_worker.pack(side="left", padx=5)

button_delete_worker = Button(ramka_lista_pracownikow, text="🗑 Usuń", command=delete_worker)
button_delete_worker.pack(side="left", padx=5)

# --- FORMULARZ PRACOWNIKA ---
ramka_formularz_pracownikow = LabelFrame(root, text="📄 Formularz pracownika", padx=10, pady=10, bg="#f0f0f0")
ramka_formularz_pracownikow.grid(row=0, column=3, padx=10, pady=10)

Label(ramka_formularz_pracownikow, text="Imię:", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
entry_worker_name = Entry(ramka_formularz_pracownikow)
entry_worker_name.grid(row=0, column=1, pady=5)

Label(ramka_formularz_pracownikow, text="Nazwisko:", bg="#f0f0f0").grid(row=1, column=0, sticky="w")
entry_worker_surname = Entry(ramka_formularz_pracownikow)
entry_worker_surname.grid(row=1, column=1, pady=5)







# Start
root.mainloop()






# button_pokaz_pracownikow = Button(ramka_lista_sklepow, text="👥 Pokaż pracowników", command=show_workers_window)
# button_pokaz_pracownikow.pack()



# button_add_worker = Button(ramka_lista_pracownikow, text="Dodaj pracownika", command=add_worker)
# button_add_worker.grid(row=0, column=0)
#
# button_delete_worker = Button(ramka_lista_pracownikow, text="Usuń pracownika", command=delete_worker)
# button_delete_worker.grid(row=0, column=1)
#
# button_update_worker = Button(ramka_lista_pracownikow, text="Edytuj pracownika", command=edit_worker)
# button_update_worker.grid(row=0, column=2)
#
#
# label_pracownicy_sklepow = Label(ramka_lista_pracownikow, text="Pracownicy:")
# label_pracownicy_sklepow.grid(row=0, column=2)
#
#
#
# label_worker_name = Label(ramka_lista_pracownikow, text="Imię:")
# label_worker_name.grid(row=1, column=2)
# entry_worker_name = Entry(ramka_formularz_pracownikow)
# entry_worker_name.grid(row=1, column=3)
#
# label_worker_surname = Label(ramka_lista_pracownikow, text="Nazwisko:")
# label_worker_surname.grid(row=2, column=2)
# entry_worker_surname = Entry(ramka_formularz_pracownikow)
# entry_worker_surname.grid(row=2, column=3)
#
#
#
#
#
#
# # RAMKA LISTA SKLEPÓW
# label_lista_sklepow=Label(ramka_lista_sklepow, text="Sklepy")
# label_lista_sklepow.grid(row=0, column=0, columnspan=4)
#
#
# button_usun_sklep=Button(ramka_lista_sklepow, text="Usuń sklep", command=delete_shop)
# button_usun_sklep.grid(row=2, column=1)
# button_pokaz_pracownikow = Button(ramka_lista_sklepow, text="Pokaż pracowników", command=show_workers_window)
# button_pokaz_pracownikow.grid(row=2, column=2)
#
# #RAMKA SZCZEGÓŁY SKLEPÓW
# label_pracownicy_sklepow=Label(ramka_lista_pracownikow, text="Pracownicy:")
# label_pracownicy_sklepow.grid(row=0, column=2, sticky='W')
#
#
#
#
# # RAMKA FORMULARZ
# label_formularz_sklepow=Label(ramka_formularz_sklepow, text="Sklep:")
# label_formularz_sklepow.grid(row=0, column=2, columnspan=2)
# label_name=Label(ramka_formularz_sklepow, text="Nazwa sklepu: ")
# label_name.grid(row=1, column=1, sticky='W')
# label_location=Label(ramka_formularz_sklepow, text="Miejscowość: ")
# label_location.grid(row=2, column=1, sticky='W')
#
# entry_name=Entry(ramka_formularz_sklepow)
# entry_name.grid(row=1, column=2, columnspan=2)
# entry_location=Entry(ramka_formularz_sklepow)
# entry_location.grid(row=2, column=2, columnspan=2)
#
# button_dodaj_sklep=Button(ramka_formularz_sklepow, text="Dodaj", command=add_shop)
# button_dodaj_sklep.grid(row=5, column=2, sticky='W')
# button_edytuj_sklep=Button(ramka_formularz_sklepow, text="Zapisz edycję", command=update_shop)
# button_edytuj_sklep.grid(row=5, column=3, sticky='W')
#
#
#
# # Pola do wpisywania danych pracownika
# label_worker_name = Label(ramka_formularz_pracownikow, text="Imię:")
# label_worker_name.grid(row=1, column=0)
# entry_worker_name = Entry(ramka_formularz_pracownikow)
# entry_worker_name.grid(row=1, column=1)
#
# label_worker_surname = Label(ramka_formularz_pracownikow, text="Nazwisko:")
# label_worker_surname.grid(row=2, column=0)
# entry_worker_surname = Entry(ramka_formularz_pracownikow)
# entry_worker_surname.grid(row=2, column=1)
#
# # Przycisk dodawania i usuwania
# button_add_worker = Button(ramka_formularz_pracownikow, text="Dodaj pracownika", command=add_worker)
# button_add_worker.grid(row=3, column=0)
#
# button_delete_worker = Button(ramka_formularz_pracownikow, text="Usuń pracownika", command=delete_worker)
# button_delete_worker.grid(row=3, column=1)













# def show_workers_window():
#     selection = listbox_lista_sklepow.curselection()
#     if not selection:
#         return
#
#     shop = shops[selection[0]]
#
#     window = Toplevel(root)
#     window.title(f"Pracownicy sklepu: {shop.name}")
#     window.geometry("600x300")
#
#
#     main_frame = Frame(window)
#     main_frame.pack(fill="both", expand=True, padx=10, pady=10)
#
#     #LEWA STRONA: LISTA PRACOWNIKÓW
#     left_frame = Frame(main_frame)
#     left_frame.grid(row=0, column=0, padx=10)
#
#     Label(left_frame, text="Pracownicy:").pack()
#     lb = Listbox(left_frame, width=30, height=10)
#     lb.pack()
#
#     for worker in shop.workers:
#         lb.insert(END, f"{worker.name} {worker.surname}")
#
#     #PRAWA STRONA: FORMULARZ PRACOWNIKA
#     right_frame = Frame(main_frame)
#     right_frame.grid(row=0, column=1, padx=10)
#
#     Label(right_frame, text="Imię:").grid(row=0, column=0, sticky="e")
#     entry_name = Entry(right_frame)
#     entry_name.grid(row=0, column=1)
#
#     Label(right_frame, text="Nazwisko:").grid(row=1, column=0, sticky="e")
#     entry_surname = Entry(right_frame)
#     entry_surname.grid(row=1, column=1)

    # def add_worker_to_shop():
    #     name = entry_worker_name.get()
    #     surname = entry_worker_surname.get()
    #     if not name or not surname:
    #         return
    #
    #     new_worker = Worker(name, surname)
    #     shop.workers.append(new_worker)
    #
    #     lb.insert(END, f"{new_worker.name} {new_worker.surname}")
    #     entry_worker_name.delete(0, END)
    #     entry_worker_surname.delete(0, END)
    #
    # Button(right_frame, text="Dodaj", command=add_worker_to_shop).grid(row=2, column=0, columnspan=2, pady=10)




#RAMKIIIIIII

# root = tk.Tk()
# root.title("Zarządzanie sklepami")
# root.geometry("1024x768")
#
# #RAMKA MAPA
# ramka_mapa=Frame(root)
# ramka_mapa.grid(row=2, column=0, columnspan=2)
#
# map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1024, height=400)
# map_widget.set_position(52.23, 21)
# map_widget.set_zoom(5)
# map_widget.grid(row=0, column=0, columnspan=8)
#
#
# # RAMKI OGÓLNE
# ramka_lista_sklepow=Frame(root)
# ramka_formularz_sklepow=Frame(root)
# ramka_lista_pracownikow=Frame(root)
# ramka_formularz_pracownikow=Frame(root)
# ramka_mapa=Frame(root)
#
# ramka_lista_sklepow.grid(row=0, column=0)
# ramka_formularz_sklepow.grid(row=0, column=1, columnspan=1)
# ramka_lista_pracownikow.grid(row=0, column=2)
# ramka_formularz_pracownikow.grid(row=0, column=3)
# ramka_mapa.grid(row=2, column=0, columnspan=4)
#
#
# listbox_lista_sklepow=Listbox(ramka_lista_sklepow, width=30, height=15)
# listbox_lista_sklepow.grid(row=1, column=0, columnspan=4)
#
#
# listbox_lista_pracownikow = Listbox(ramka_lista_pracownikow, width=30, height=15)
# listbox_lista_pracownikow.grid(row=1, column=1, columnspan=4)



