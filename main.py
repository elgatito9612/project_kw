from tkinter import *

import tkintermapview

import tkinter as tk



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
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    tmp_shop=Shop(name=nazwa, location=miejscowosc)
    shops.append(tmp_shop)
    listbox_lista_sklepow.insert(END, tmp_shop.name, tmp_shop.location)

    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_name.focus()
    show_shops()


# READ
def show_shops():
    listbox_lista_sklepow.delete(0, END)
    for shop in shops:
        listbox_lista_sklepow.insert(END, shop.name, shop.location)

# UPDATE
def update_shop():
    idx = listbox_lista_sklepow.index(ACTIVE)
    name = entry_name.get()
    location = entry_location.get()

    shops[idx].name = name
    shops[idx].location = location

    shops[idx].marker.delete()
    shops[idx].coordinates = shops[idx].get_coordinates()
    shops[idx].marker = map_widget.set_marker(shops[idx].coordinates[0], shops[idx].coordinates[1], text=shops[idx].name)

# DELETE
def delete_shop():
    idx = listbox_lista_sklepow.index(ACTIVE)
    shops[idx].marker.delete()
    shops.pop(idx)
    show_shops()







#PRRRACOWNICYYYYYY


# CREATE
def add_worker():
    name = entry_worker_name.get()
    surname = entry_worker_surname.get()
    if not name or not surname:
        return

    selection = listbox_lista_sklepow.curselection()
    if not selection:
        return

    shop = shops[selection[0]]
    new_worker = Worker(name, surname)
    shop.workers.append(new_worker)

    on_shop_select(None)

    entry_worker_name.delete(0, END)
    entry_worker_surname.delete(0, END)
    show_workers(shop)

# READ
def show_workers(shop) -> None:
    listbox_lista_pracownikow.delete(0, END)
    for worker in shop.workers:
        listbox_lista_pracownikow.insert(END, f"{worker.name} {worker.surname}")


# UPDATE
def update_worker():
    selection = listbox_lista_sklepow.curselection()
    if not selection:
        return

    shop = shops[selection[0]]
    worker_selection = listbox_lista_pracownikow.curselection()
    if not worker_selection:
        return

    new_name = entry_worker_name.get()
    new_surname = entry_worker_surname.get()

    if not new_name or not new_surname:
        return


    shop.workers[worker_selection[0]].name = new_name
    shop.workers[worker_selection[0]].surname = new_surname

    entry_worker_name.delete(0, END)
    entry_worker_surname.delete(0, END)
    show_workers(shop)


# DELETE
def delete_worker():
    shop_selection = listbox_lista_sklepow.curselection()
    worker_selection = listbox_lista_pracownikow.curselection()
    if not shop_selection or not worker_selection:
        return
    shop = shops[shop_selection[0]]
    del shop.workers[worker_selection[0]]
    on_shop_select(None)
    show_workers(shop)


def show_workers_window():
    selection = listbox_lista_sklepow.curselection()
    if not selection:
        return

    shop = shops[selection[0]]

    window = Toplevel(root)
    window.title(f"Pracownicy sklepu: {shop.name}")
    window.geometry("600x300")


    main_frame = Frame(window)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    #LEWA STRONA: LISTA PRACOWNIKÓW
    left_frame = Frame(main_frame)
    left_frame.grid(row=0, column=0, padx=10)

    Label(left_frame, text="Pracownicy:").pack()
    lb = Listbox(left_frame, width=30, height=10)
    lb.pack()

    for worker in shop.workers:
        lb.insert(END, f"{worker.name} {worker.surname}")

    #PRAWA STRONA: FORMULARZ PRACOWNIKA
    right_frame = Frame(main_frame)
    right_frame.grid(row=0, column=1, padx=10)

    Label(right_frame, text="Imię:").grid(row=0, column=0, sticky="e")
    entry_name = Entry(right_frame)
    entry_name.grid(row=0, column=1)

    Label(right_frame, text="Nazwisko:").grid(row=1, column=0, sticky="e")
    entry_surname = Entry(right_frame)
    entry_surname.grid(row=1, column=1)

    def add_worker_to_shop():
        name = entry_name.get()
        surname = entry_surname.get()
        if not name or not surname:
            return

        new_worker = Worker(name, surname)
        shop.workers.append(new_worker)

        lb.insert(END, f"{new_worker.name} {new_worker.surname}")
        entry_name.delete(0, END)
        entry_surname.delete(0, END)

    Button(right_frame, text="Dodaj", command=add_worker_to_shop).grid(row=2, column=0, columnspan=2, pady=10)




#RAMKIIIIIII

root = tk.Tk()
root.title("Zarządzanie sklepami")
root.geometry("1024x768")

#RAMKA MAPA
ramka_mapa=Frame(root)
ramka_mapa.grid(row=2, column=0, columnspan=2)

map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1024, height=400)
map_widget.set_position(52.23, 21)
map_widget.set_zoom(5)
map_widget.grid(row=0, column=0, columnspan=8)


# RAMKI OGÓLNE
ramka_lista_sklepow=Frame(root)
ramka_formularz_sklepow=Frame(root)
ramka_lista_pracownikow=Frame(root)
ramka_formularz_pracownikow=Frame(root)
ramka_mapa=Frame(root)

ramka_lista_sklepow.grid(row=0, column=0)
ramka_formularz_sklepow.grid(row=0, column=1, columnspan=1)
ramka_lista_pracownikow.grid(row=0, column=2)
ramka_formularz_pracownikow.grid(row=0, column=3)
ramka_mapa.grid(row=2, column=0, columnspan=4)


listbox_lista_sklepow=Listbox(ramka_lista_sklepow, width=30, height=15)
listbox_lista_sklepow.grid(row=1, column=0, columnspan=4)

listbox_lista_pracownikow = Listbox(ramka_lista_pracownikow, width=30, height=15)
listbox_lista_pracownikow.grid(row=1, column=1, columnspan=4)



def on_shop_select(event):
    selection = listbox_lista_sklepow.curselection()
    if not selection:
        return
    index = selection[0]
    shop = shops[index]

    # czyścimy listę pracowników
    listbox_lista_pracownikow.delete(0, END)

    # wypełniamy listę pracowników
    for worker in shop.workers:
        listbox_lista_pracownikow.insert(END, f"{worker.name} {worker.surname}")

    # Czyścimy formularz pracownika
    entry_worker_name.delete(0, END)
    entry_worker_surname.delete(0, END)




button_add_worker = Button(ramka_lista_pracownikow, text="Dodaj pracownika", command=add_worker)
button_add_worker.grid(row=0, column=0)

button_delete_worker = Button(ramka_lista_pracownikow, text="Usuń pracownika", command=delete_worker)
button_delete_worker.grid(row=0, column=1)


label_pracownicy_sklepow = Label(ramka_lista_pracownikow, text="Pracownicy:")
label_pracownicy_sklepow.grid(row=0, column=2)



label_worker_name = Label(ramka_lista_pracownikow, text="Imię:")
label_worker_name.grid(row=1, column=2)
entry_worker_name = Entry(ramka_formularz_pracownikow)
entry_worker_name.grid(row=1, column=3)

label_worker_surname = Label(ramka_lista_pracownikow, text="Nazwisko:")
label_worker_surname.grid(row=2, column=2)
entry_worker_surname = Entry(ramka_formularz_pracownikow)
entry_worker_surname.grid(row=2, column=3)






# RAMKA LISTA SKLEPÓW
label_lista_sklepow=Label(ramka_lista_sklepow, text="Sklepy")
label_lista_sklepow.grid(row=0, column=0, columnspan=4)

button_edytuj_sklep=Button(ramka_lista_sklepow, text="Edytuj sklep", command=update_shop)
button_edytuj_sklep.grid(row=2, column=0)
button_usun_sklep=Button(ramka_lista_sklepow, text="Usuń sklep", command=delete_shop)
button_usun_sklep.grid(row=2, column=1)
button_pokaz_pracownikow = Button(ramka_lista_sklepow, text="Pokaż pracowników", command=show_workers_window)
button_pokaz_pracownikow.grid(row=2, column=2)

#RAMKA SZCZEGÓŁY SKLEPÓW
label_pracownicy_sklepow=Label(ramka_lista_pracownikow, text="Pracownicy:")
label_pracownicy_sklepow.grid(row=0, column=2, sticky='W')




# RAMKA FORMULARZ
label_formularz_sklepow=Label(ramka_formularz_sklepow, text="Sklep:")
label_formularz_sklepow.grid(row=0, column=1, columnspan=2)
label_name=Label(ramka_formularz_sklepow, text="Nazwa sklepu: ")
label_name.grid(row=1, column=1, sticky='W')
label_location=Label(ramka_formularz_sklepow, text="Miejscowość: ")
label_location.grid(row=2, column=1, sticky='W')

entry_name=Entry(ramka_formularz_sklepow)
entry_name.grid(row=1, column=2,)
entry_location=Entry(ramka_formularz_sklepow)
entry_location.grid(row=2, column=2)

button_dodaj_sklep=Button(ramka_formularz_sklepow, text="Dodaj", command=add_shop)
button_dodaj_sklep.grid(row=5, column=2, columnspan=1)




# Pola do wpisywania danych pracownika
label_worker_name = Label(ramka_formularz_pracownikow, text="Imię:")
label_worker_name.grid(row=1, column=0)
entry_worker_name = Entry(ramka_formularz_pracownikow)
entry_worker_name.grid(row=1, column=1)

label_worker_surname = Label(ramka_formularz_pracownikow, text="Nazwisko:")
label_worker_surname.grid(row=2, column=0)
entry_worker_surname = Entry(ramka_formularz_pracownikow)
entry_worker_surname.grid(row=2, column=1)

# Przycisk dodawania i usuwania
button_add_worker = Button(ramka_formularz_pracownikow, text="Dodaj pracownika", command=add_worker)
button_add_worker.grid(row=3, column=0)

button_delete_worker = Button(ramka_formularz_pracownikow, text="Usuń pracownika", command=delete_worker)
button_delete_worker.grid(row=3, column=1)




# Start
root.mainloop()





