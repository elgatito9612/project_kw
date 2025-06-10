from tkinter import *

import tkintermapview

import tkinter as tk

from tkinter import simpledialog, messagebox


shops:list = []



class Shop:
    def __init__(self, name, location):
        self.name=name
        self.location=location
        self.coordinates= self.get_coordinates()
        self.marker=map_widget.set_marker(self.coordinates[0], self.coordinates[1])
        self.workers = []

    def __str__(self):
            return self.name

class Worker:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __str__(self):
        return f"{self.name} {self.surname}"





def get_coordinates(self) -> list:
    import requests
    from bs4 import BeautifulSoup
    address_url: str = f"https://pl.wikipedia.org/wiki/{self.location}"
    response = requests.get(address_url).text
    response_html = BeautifulSoup(response, "html.parser")
    longitude: float = float(response_html.select(".longitude")[1].text.replace(",", "."))

    latitude: float = float(response_html.select(".latitude")[1].text.replace(",", "."))

    return [latitude, longitude]


def add_shop():
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    tmp_shop=Shop(name=nazwa, location=miejscowosc)
    shops.append(tmp_shop)

    print(shops)
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_name.focus()
    show_shops()

def show_shops():
    listbox_lista_sklepow.delete(0, END)
    for idx,shop in enumerate(shops):
        listbox_lista_sklepow.insert(idx, f"{idx+1}. {shop.name}, {shop.location}")


def delete_shop():
    idx=listbox_lista_sklepow.index(ACTIVE)
    shops[idx].marker.delete()
    shops.pop(idx)
    show_shops()

def shop_details():
    idx=listbox_lista_sklepow.index(ACTIVE)
    label_name_szczegoly_sklepow_wartosc.configure(text=shops[idx].name)
    label_location_szczegoly_sklepow_wartosc.configure(text=shops[idx].location)
    map_widget.set_position(shops[idx].coordinates[0],shops[idx].coordinates[1])
    map_widget.set_zoom(16)

def edit_shop():
    idx=listbox_lista_sklepow.index(ACTIVE)
    entry_name.insert(0, shops[idx].name)
    entry_location.insert(0, shops[idx].location)

    button_dodaj_sklep.configure(text="Zapisz", command=lambda:update_shop(idx))

def update_shop(idx):
    name=entry_name.get()
    location=entry_location.get()


    shops[idx].name=name
    shops[idx].location=location


    shops[idx].marker.delete()
    shops[idx].coordinates=shops[idx].get_coordinates()
    shops[idx].marker=map_widget.set_marker(shops[idx].coordinates[0],shops[idx].coordinates[1])

    button_dodaj_sklep.configure(text="Dodaj", command=add_shop)
    show_shops()

    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_name.focus()







def shop_choice(evt):
    show_workers()







def show_workers():
    lista_pracownikow.delete(0, tk.END)
    choice = lista_sklepow.curselection()
    if not choice:
        return
    shop = shops[choice[0]]
    for p in shop.worker:
        lista_pracownikow.insert(tk.END, str(p))


def add_worker():
    choice = lista_sklepow.curselection()
    if not choice:
        messagebox.showwarning("Brak sklepu", "Najpierw wybierz sklep.")
        return
    name = simpledialog.askstring("Imię pracownika", "Podaj imię:")
    surname = simpledialog.askstring("Nazwisko pracownika", "Podaj nazwisko:")
    if name and surname:
        shop = shops[choice[0]]
        shop.workers.append(Worker(name, surname))
        show_workers()

def delete_worker():
    shop_idx = lista_sklepow.curselection()
    worker_idx = lista_pracownikow.curselection()
    if shop_idx and worker_idx:
        shop = shops[shop_idx[0]]
        del shop.workers[worker_idx[0]]
        show_workers()


def edit_worker():
    shop_idx = lista_sklepow.curselection()
    worker_idx = lista_pracownikow.curselection()

    if not shop_idx or not worker_idx:
        messagebox.showwarning("Brak wyboru", "Wybierz pracownika do edycji.")
        return

    shop = shops[shop_idx[0]]
    worker = shop.workers[worker_idx[0]]

    new_name = simpledialog.askstring("Edytuj imię", "Nowe imię:", initialvalue=worker.name)
    new_surname = simpledialog.askstring("Edytuj nazwisko", "Nowe nazwisko:", initialvalue=worker.surname)

    if new_name and new_surname:
        worker.name = new_name
        worker.surname = new_surname
        show_workers()








root = Tk()
root.title("Mapbook_kw")
root.geometry("1024x768")


# RAMKI
ramka_lista_sklepow=Frame(root)
ramka_formularz=Frame(root)
ramka_szczegoly_sklepow=Frame(root)
ramka_mapa=Frame(root)

ramka_lista_sklepow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_sklepow.grid(row=1, column=0)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# RAMKA LISTA OBIEKTÓW
label_lista_sklepow=Label(ramka_lista_sklepow, text="Lista sklepów: ")
label_lista_sklepow.grid(row=0, column=0, columnspan=3)
listbox_lista_sklepow=Listbox(ramka_lista_sklepow, width=50, height=10)
listbox_lista_sklepow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly=Button(ramka_lista_sklepow, text="Pokaż szczegóły", command=shop_details)
button_pokaz_szczegoly.grid(row=2, column=0)
button_edytuj_sklep=Button(ramka_lista_sklepow, text="Edytuj sklep", command=edit_shop)
button_edytuj_sklep.grid(row=2, column=1)
button_usun_sklep=Button(ramka_lista_sklepow, text="Usuń sklep", command=delete_shop)
button_usun_sklep.grid(row=2, column=2)

# RAMKA FORMULARZ
label_formularz=Label(ramka_formularz, text="Formularz: ")
label_formularz.grid(row=0, column=0, columnspan=2)
label_name=Label(ramka_formularz, text="Nazwa sklepu: ")
label_name.grid(row=1, column=0, sticky=W)
label_location=Label(ramka_formularz, text="Miejscowość: ")
label_location.grid(row=4, column=0, sticky=W)

entry_name=Entry(ramka_formularz)
entry_name.grid(row=1, column=1,)
entry_location=Entry(ramka_formularz)
entry_location.grid(row=4, column=1)
button_dodaj_sklep=Button(ramka_formularz, text="Dodaj ", command=add_shop)
button_dodaj_sklep.grid(row=5, column=1, columnspan=2)


#RAMKA SZCZEGÓŁY SKLEPÓW
label_szczegoly_sklepow=Label(ramka_szczegoly_sklepow, text="Szczegóły sklepu: ")
label_szczegoly_sklepow.grid(row=0, column=0, sticky=W)

label_name_szczegoly_sklepow=Label(ramka_szczegoly_sklepow, text="Imię: ")
label_name_szczegoly_sklepow.grid(row=1, column=0)
label_name_szczegoly_sklepow_wartosc=Label(ramka_szczegoly_sklepow, text="....")
label_name_szczegoly_sklepow_wartosc.grid(row=1, column=1)

label_location_szczegoly_sklepow=Label(ramka_szczegoly_sklepow, text="Miejscowośc: ")
label_location_szczegoly_sklepow.grid(row=1, column=6)
label_location_szczegoly_sklepow_wartosc=Label(ramka_szczegoly_sklepow, text="....")
label_location_szczegoly_sklepow_wartosc.grid(row=1, column=7)

# RAMKA MAPA
map_widget=tkintermapview.TkinterMapView(ramka_mapa, width=1024, height=400)
map_widget.set_position(52.23, 21)
map_widget.set_zoom(5)
map_widget.grid(row=0, column=0, columnspan=8)



# sklepy = []


root = tk.Tk()
root.title("CRUD: Sklepy i Pracownicy")

# Sklepy
ramka_sklepy = tk.Frame(root)
ramka_sklepy.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(ramka_sklepy, text="Sklepy").pack()
lista_sklepow = tk.Listbox(ramka_sklepy, width=30, height=10)
lista_sklepow.pack()
lista_sklepow.bind('<<ListboxSelect>>', shop_choice)

tk.Button(ramka_sklepy, text="Dodaj sklep", command=add_shop).pack(fill='x')
tk.Button(ramka_sklepy, text="Usuń sklep", command=delete_shop).pack(fill='x')

# Pracownicy
ramka_pracownicy = tk.Frame(root)
ramka_pracownicy.pack(side=tk.RIGHT, padx=10, pady=10)

tk.Label(ramka_pracownicy, text="Pracownicy").pack()
lista_pracownikow = tk.Listbox(ramka_pracownicy, width=30, height=10)
lista_pracownikow.pack()

tk.Button(ramka_pracownicy, text="Dodaj pracownika", command=add_worker).pack(fill='x')
tk.Button(ramka_pracownicy, text="Usuń pracownika", command=delete_worker).pack(fill='x')

# Start GUI
root.mainloop()