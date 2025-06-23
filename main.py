import tkinter as tk
from tkinter import ttk, Listbox, Frame, Label, Entry, END, Toplevel
import tkintermapview
import requests
from bs4 import BeautifulSoup





class Worker:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname


class Shop:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"🏦 {self.name}", icon=pin_image)
        self.workers = []


    def get_coordinates(self):
        address_url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(address_url).text
        soup = BeautifulSoup(response, "html.parser")
        longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
        latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
        return [latitude, longitude]


def add_shop():
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    if not nazwa or not miejscowosc:
        return
    tmp_shop = Shop(name=nazwa, location=miejscowosc)
    shops.append(tmp_shop)
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_name.focus()
    show_shops()


def show_shops():
    listbox_lista_sklepow.delete(0, END)
    for i, shop in enumerate(shops, start=1):
        listbox_lista_sklepow.insert(END, f"📅 {i}. {shop.name}, {shop.location}")


def update_shop():
    idx = listbox_lista_sklepow.index(tk.ACTIVE)
    name = entry_name.get()
    location = entry_location.get()
    if not name or not location:
        return
    shops[idx].name = name
    shops[idx].location = location
    shops[idx].marker.delete()
    shops[idx].coordinates = shops[idx].get_coordinates()
    shops[idx].marker = map_widget.set_marker(
        shops[idx].coordinates[0], shops[idx].coordinates[1], text=f"🏦 {shops[idx].name}", icon=pin_image
    )
    show_shops()


def delete_shop():
    idx = listbox_lista_sklepow.index(tk.ACTIVE)
    shops[idx].marker.delete()
    shops.pop(idx)
    show_shops()

def on_shop_select(event):
    selection = listbox_lista_sklepow.curselection()
    if not selection:
        return
    idx = selection[0]
    shop = shops[idx]
    entry_name.delete(0, END)
    entry_name.insert(0, shop.name)
    entry_location.delete(0, END)
    entry_location.insert(0, shop.location)

def show_workers_window():
    selection = listbox_lista_sklepow.curselection()
    if not selection:
        return

    shop = shops[selection[0]]
    window = Toplevel(root)
    window.title(f"👥 Pracownicy sklepu: {shop.name}")
    window.geometry("600x350")
    window.configure(bg="#1f1f1f")

    main_frame = Frame(window, bg="#1f1f1f", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    label_left_title = Label(
        main_frame,
        text="📋 Lista pracowników",
        font=("Segoe UI", 12, "bold"),
        bg="#fc86f0",  # miętowy
        fg="black",
        padx=5, pady=2
    )
    label_left_title.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 0))

    left_frame = tk.Frame(
        main_frame,
        bg="#2e2e2e",
        relief=tk.RIDGE,
        bd=2
    )
    left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")
    lb = Listbox(left_frame, width=30, height=15, font=("Segoe UI", 10),
             bg="#b4a1cc", fg="black",
             selectbackground="#322442",
             selectforeground="white")
    lb.pack()
    for i, worker in enumerate(shop.workers, start=1):
        lb.insert(END, f"{i}. {worker.name} {worker.surname}")

    label_right_title = Label(
        main_frame,
        text="✏️ Edycja / Dodawanie",
        font=("Segoe UI", 12, "bold"),
        bg="#fc86f0",  # ten sam kolor, żeby wyglądał jak pasek nad ramką
        fg="black",
        padx=5, pady=2
    )
    label_right_title.grid(row=0, column=1, sticky="ew", padx=10, pady=(0, 0))

    right_frame = tk.Frame(
        main_frame,
        bg="#2e2e2e",
        relief=tk.RIDGE,
        bd=2
    )
    right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")

    Label(right_frame, text="Imię:", font=("Segoe UI", 10), bg="#2e2e2e", fg="white").grid(row=0, column=0, sticky="e", pady=5)
    entry_name_w = Entry(right_frame,bg="#dbadd7", fg="black", font=("Segoe UI", 10), width=20)
    entry_name_w.grid(row=0, column=1, pady=5)

    Label(right_frame, text="Nazwisko:", font=("Segoe UI", 10), bg="#2e2e2e", fg="white").grid(row=1, column=0, sticky="e", pady=5)
    entry_surname = Entry(right_frame, bg="#dbadd7", fg="black", font=("Segoe UI", 10), width=20)
    entry_surname.grid(row=1, column=1, pady=5)

    def on_worker_select(event):
        idx = lb.curselection()
        if not idx:
            return
        worker = shop.workers[idx[0]]
        entry_name_w.delete(0, END)
        entry_name_w.insert(0, worker.name)
        entry_surname.delete(0, END)
        entry_surname.insert(0, worker.surname)

    lb.bind("<<ListboxSelect>>", on_worker_select)

    def add_worker():
        name = entry_name_w.get()
        surname = entry_surname.get()
        if not name or not surname:
            return
        worker = Worker(name, surname)
        shop.workers.append(worker)
        lb.insert(END, f"{len(shop.workers)}. {worker.name} {worker.surname}")
        entry_name_w.delete(0, END)
        entry_surname.delete(0, END)

    def edit_worker():
        idx = lb.curselection()
        if not idx:
            return
        shop.workers[idx[0]].name = entry_name_w.get()
        shop.workers[idx[0]].surname = entry_surname.get()
        lb.delete(idx[0])
        lb.insert(idx[0], f"{idx[0] + 1}. {entry_name_w.get()} {entry_surname.get()}")
        entry_name_w.delete(0, END)
        entry_surname.delete(0, END)

    def delete_worker():
        idx = lb.curselection()
        if not idx:
            return
        del shop.workers[idx[0]]
        lb.delete(idx[0])
        entry_name_w.delete(0, END)
        entry_surname.delete(0, END)

    button_frame = Frame(right_frame, bg="#2e2e2e")
    button_frame.grid(row=2, column=0, columnspan=2, pady=10)

    tk.Button(button_frame, text="➕ Dodaj", bg="#fc86f0", fg="black",
                             activebackground="#942589", font=("Segoe UI", 10, "bold"), command=add_worker).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="🖉 Edytuj", bg="#fc86f0", fg="black",
                             activebackground="#942589", font=("Segoe UI", 10, "bold"), command=edit_worker).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="❌ Usuń", bg="#fc86f0", fg="black",
                             activebackground="#942589", font=("Segoe UI", 10, "bold"), command=delete_worker).grid(row=0, column=2, padx=5)



# === GŁÓWNE OKNO ===
shops = []

root = tk.Tk()
root.title("💼 Zarządzanie sklepami")
root.geometry("1300x750")
root.configure(bg="#121212")
pin_image = tk.PhotoImage(file="purple_pin.png")

# Konfiguracja stylu
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#000000", foreground="white", font=("Segoe UI", 10, "bold"))


# Ustawienie siatki
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)

# RAMKA MAPY
ramka_mapa = Frame(root, bg="#000000")
ramka_mapa.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=700, height=600)
map_widget.set_position(52.23, 21)
map_widget.set_zoom(6)
map_widget.pack(fill="both", expand=True)



# PRAWA KOLUMNA
prawa_kolumna = Frame(root, bg="#1f1f1f")
prawa_kolumna.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# LISTA SKLEPÓW
ramka_lista_sklepow = Frame(prawa_kolumna, bg="#2e2e2e", padx=10, pady=10, relief=tk.RIDGE, bd=2)
ramka_lista_sklepow.pack(fill="x", pady=(0, 10))
Label(ramka_lista_sklepow, text="🛌 Lista sklepów", font=("Segoe UI", 12, "bold"), bg="#c38fff").grid(row=0, column=0, columnspan=2)
listbox_lista_sklepow = Listbox(ramka_lista_sklepow,
    width=40,
    height=20,
    font=("Segoe UI", 10),
    bg="#b4a1cc", fg="black",
    selectbackground="#322442",
    selectforeground="white")
listbox_lista_sklepow.grid(row=1, column=0, columnspan=2, pady=5)
listbox_lista_sklepow.bind("<<ListboxSelect>>", on_shop_select)

# FORMULARZ
ramka_formularz_sklepow = Frame(prawa_kolumna, bg="#2e2e2e", padx=10, pady=10, relief=tk.RIDGE, bd=2)
ramka_formularz_sklepow.pack(fill="both", expand=True)
Label(ramka_formularz_sklepow, text="📑 Formularz sklepu", font=("Segoe UI", 12, "bold"), bg="#03dac6").grid(row=0, column=0, columnspan=2, pady=5)
Label(ramka_formularz_sklepow, text="🏦 Nazwa:", font=("Segoe UI", 10), bg="#2e2e2e", fg="white").grid(row=1, column=0, sticky='w')
entry_name = Entry(ramka_formularz_sklepow, bg="#aed6d2", fg="black")
entry_name.grid(row=1, column=1, pady=2)
Label(ramka_formularz_sklepow, text="🌆 Miejscowość:", font=("Segoe UI", 10), bg="#2e2e2e", fg="white").grid(row=2, column=0, sticky='w')
entry_location = Entry(ramka_formularz_sklepow, bg="#aed6d2", fg="black")
entry_location.grid(row=2, column=1, pady=2)


button_dodaj = tk.Button(ramka_formularz_sklepow, text="➕ Dodaj", bg="#03dac6", fg="black", activebackground="#1e635d", font=("Segoe UI", 10, "bold"), command=add_shop)
button_dodaj.grid(row=3, column=0, pady=10)

button_edytuj = tk.Button(ramka_formularz_sklepow, text="🖉 Edytuj", bg="#03dac6", fg="black", activebackground="#1e635d", font=("Segoe UI", 10, "bold"), command=update_shop)
button_edytuj.grid(row=3, column=1, pady=10)

button_usun_sklep = tk.Button(ramka_lista_sklepow, text="❌ Usuń sklep", bg="#c38fff", fg="black", activebackground="#501e8a", font=("Segoe UI", 10, "bold"), command=delete_shop)
button_usun_sklep.grid(row=2, column=0, pady=5)

button_pokaz_pracownikow = tk.Button(ramka_lista_sklepow, text="💼 Pokaż pracowników", bg="#c38fff", fg="black", activebackground="#501e8a", font=("Segoe UI", 10, "bold"), command=show_workers_window)
button_pokaz_pracownikow.grid(row=2, column=1, pady=5)



root.mainloop()
