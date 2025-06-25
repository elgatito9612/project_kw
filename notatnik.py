# liczby = []
# for i in range(1,1000):
#     if i % 7 == 0 and i % 3 == 0:
#         liczby.append(i)
#
# for liczba in reversed(liczby):
#     print(liczba)



# wyniki=[]
#
# liczba = int(input("Podaj liczbe: "))
# print(f"DzieLniki liczby {liczba} to:")
# for i in range (1, liczba+1):
#     if liczba % i == 0:
#       print(liczba)



#ciąg fibonacciego
# previous_result = 0  # początkowy wynik
# current_result = 1  # pierwszy wynik, który dodamy

# for i in range(1, 101):
#     new_result = previous_result + current_result
#     print(new_result)
#
#     previous_result = current_result
#     current_result = new_result










import tkinter as tk
from tkinter import ttk, Listbox, Frame, Label, Entry, END, Toplevel
import tkintermapview
import requests
from bs4 import BeautifulSoup





class Worker:
    def __init__(self, name, surname, coordinates=None):
        self.name = name
        self.surname = surname
        self.coordinates = coordinates
        self.marker = None

class Supplier:
    def __init__(self, name, contact, coordinates=None):
        self.name = name
        self.contact = contact
        self.coordinates = coordinates
        self.marker = None



class Shop:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"{self.name}", icon=shop_pin_image)
        self.workers = []
        self.suppliers = []


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
        shops[idx].coordinates[0], shops[idx].coordinates[1], text=f"{shops[idx].name}", icon=shop_pin_image, anchor="se"
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
    window.geometry("1000x420")
    window.configure(bg="#1f1f1f")

    main_frame = Frame(window, bg="#1f1f1f", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    # Lista pracowników (lewa kolumna)
    label_left_title = Label(
        main_frame,
        text="📋 Lista pracowników",
        font=("Segoe UI", 12, "bold"),
        bg="#fc86f0",
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
             bg="#db9cce", fg="black",
             selectbackground="#42243d",
             selectforeground="white")
    lb.pack()
    for i, worker in enumerate(shop.workers, start=1):
        lb.insert(END, f"{i}. {worker.name} {worker.surname}")

    # Formularz pracownika (środek)
    label_right_title = Label(
        main_frame,
        text="✏️ Edycja / Dodawanie",
        font=("Segoe UI", 12, "bold"),
        bg="#fc86f0",
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

    Label(right_frame, text="Wybrane współrzędne:", font=("Segoe UI", 10), bg="#2e2e2e", fg="white").grid(row=2, column=0, sticky="e", pady=5)
    label_coordinates = Label(right_frame, text="", font=("Segoe UI", 10), bg="#2e2e2e", fg="#8ee150")
    label_coordinates.grid(row=2, column=1, pady=5)

    selected_coordinates = [None]  # typ: [(lat, lon)] – lista, bo zamknięcie!

    # Mapa pracowników (prawa kolumna)
    map_frame = tk.Frame(main_frame, bg="#2e2e2e", relief=tk.RIDGE, bd=2)
    map_frame.grid(row=1, column=2, padx=10, pady=10, sticky="n")
    map_workers = tkintermapview.TkinterMapView(map_frame, width=350, height=250)
    # domyślna pozycja na sklep, albo na Polskę
    start_lat, start_lon = shop.coordinates if shop.coordinates else (52.23, 21.0)
    map_workers.set_position(start_lat, start_lon)
    map_workers.set_zoom(13)
    map_workers.pack(fill="both", expand=True)

    # Pinezki pracowników na mapie
    worker_markers = []

    def refresh_worker_markers():
        for marker in worker_markers:
            marker.delete()
        worker_markers.clear()
        for worker in shop.workers:
            if worker.coordinates:
                marker = map_workers.set_marker(
                    worker.coordinates[0], worker.coordinates[1],
                    text=f"{worker.name} {worker.surname}",
                    icon=worker_pin_image,
                    anchor="se",
                )
                worker.marker = marker
                worker_markers.append(marker)

    refresh_worker_markers()

    # Dodawanie pinezki na mapie po kliknięciu
    selected_marker = [None]

    def on_map_click(event):
        lat, lon = map_workers.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        label_coordinates.config(text=f"{lat:.5f}, {lon:.5f}")
        selected_coordinates[0] = (lat, lon)
        if selected_marker[0]:
            selected_marker[0].delete()
        marker = map_workers.set_marker(lat, lon, text="Nowy pracownik", icon=worker_pin_image, anchor="se")
        selected_marker[0] = marker

    map_workers.canvas.bind("<Button-1>", on_map_click)

    # Kliknięcie na pracownika z listy – pokaż pinezkę do edycji na mapie
    def on_worker_select(event):
        idx = lb.curselection()
        if not idx:
            return
        worker = shop.workers[idx[0]]
        entry_name_w.delete(0, END)
        entry_name_w.insert(0, worker.name)
        entry_surname.delete(0, END)
        entry_surname.insert(0, worker.surname)
        if worker.coordinates:
            label_coordinates.config(text=f"{worker.coordinates[0]:.5f}, {worker.coordinates[1]:.5f}")
            map_workers.set_position(worker.coordinates[0], worker.coordinates[1])
            if selected_marker[0]:
                selected_marker[0].delete()
            marker = map_workers.set_marker(worker.coordinates[0], worker.coordinates[1], text="Edytowany", icon=worker_pin_image, anchor="se")
            selected_marker[0] = marker
            selected_coordinates[0] = worker.coordinates
        else:
            label_coordinates.config(text="Brak")
            if selected_marker[0]:
                selected_marker[0].delete()
            selected_coordinates[0] = None

    lb.bind("<<ListboxSelect>>", on_worker_select)

    # Dodawanie nowego pracownika (wraz z pinezką)
    def add_worker():
        name = entry_name_w.get()
        surname = entry_surname.get()
        coords = selected_coordinates[0]
        if not name or not surname or not coords:
            return
        worker = Worker(name, surname, coords)
        shop.workers.append(worker)
        lb.insert(END, f"{len(shop.workers)}. {worker.name} {worker.surname}")
        entry_name_w.delete(0, END)
        entry_surname.delete(0, END)
        label_coordinates.config(text="")
        if selected_marker[0]:
            selected_marker[0].delete()
            selected_marker[0] = None
        selected_coordinates[0] = None
        refresh_worker_markers()

    # Edycja pracownika (wraz z pinezką)
    def edit_worker():
        idx = lb.curselection()
        if not idx:
            return
        worker = shop.workers[idx[0]]
        worker.name = entry_name_w.get()
        worker.surname = entry_surname.get()
        coords = selected_coordinates[0]
        if coords:
            worker.coordinates = coords
        lb.delete(idx[0])
        lb.insert(idx[0], f"{idx[0] + 1}. {worker.name} {worker.surname}")
        entry_name_w.delete(0, END)
        entry_surname.delete(0, END)
        label_coordinates.config(text="")
        if selected_marker[0]:
            selected_marker[0].delete()
            selected_marker[0] = None
        selected_coordinates[0] = None
        refresh_worker_markers()

    # Usuwanie pracownika (wraz z pinezką)
    def delete_worker():
        idx = lb.curselection()
        if not idx:
            return
        worker = shop.workers[idx[0]]
        if worker.marker:
            worker.marker.delete()
        del shop.workers[idx[0]]
        lb.delete(idx[0])
        entry_name_w.delete(0, END)
        entry_surname.delete(0, END)
        label_coordinates.config(text="")
        if selected_marker[0]:
            selected_marker[0].delete()
            selected_marker[0] = None
        selected_coordinates[0] = None
        refresh_worker_markers()

    button_frame = Frame(right_frame, bg="#2e2e2e")
    button_frame.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(button_frame, text="➕ Dodaj", bg="#fc86f0", fg="black",
              activebackground="#942589", font=("Segoe UI", 10, "bold"), command=add_worker).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="🖉 Edytuj", bg="#fc86f0", fg="black",
              activebackground="#942589", font=("Segoe UI", 10, "bold"), command=edit_worker).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="❌ Usuń", bg="#fc86f0", fg="black",
              activebackground="#942589", font=("Segoe UI", 10, "bold"), command=delete_worker).grid(row=0, column=2, padx=5)


def show_suppliers_window():
    selection = listbox_lista_sklepow.curselection()
    if not selection:
        return

    shop = shops[selection[0]]
    window = Toplevel(root)
    window.title(f"📦 Dostawcy sklepu: {shop.name}")
    window.geometry("1000x420")
    window.configure(bg="#1f1f1f")

    main_frame = Frame(window, bg="#1f1f1f", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    # Lista dostawców (lewa kolumna)
    label_left_title = Label(
        main_frame,
        text="📋 Lista dostawców",
        font=("Segoe UI", 12, "bold"),
        bg="#fca47a",
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
                 bg="#ccada6", fg="black",
                 selectbackground="#422E24",
                 selectforeground="white")
    lb.pack()
    for i, supplier in enumerate(shop.suppliers, start=1):
        lb.insert(END, f"{i}. {supplier.name} ({supplier.contact})")

    # Formularz dostawcy (środek)
    label_right_title = Label(
        main_frame,
        text="✏️ Edycja / Dodawanie",
        font=("Segoe UI", 12, "bold"),
        bg="#fca47a",
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

    Label(right_frame, text="Nazwa:", font=("Segoe UI", 10), bg="#2e2e2e", fg="white").grid(row=0, column=0, sticky="e", pady=5)
    entry_name_s = Entry(right_frame, bg="#dbbda7", fg="black", font=("Segoe UI", 10), width=20)
    entry_name_s.grid(row=0, column=1, pady=5)

    Label(right_frame, text="Kontakt:", font=("Segoe UI", 10), bg="#2e2e2e", fg="white").grid(row=1, column=0, sticky="e", pady=5)
    entry_contact = Entry(right_frame, bg="#dbbda7", fg="black", font=("Segoe UI", 10), width=20)
    entry_contact.grid(row=1, column=1, pady=5)

    Label(right_frame, text="Wybrane współrzędne:", font=("Segoe UI", 10), bg="#2e2e2e", fg="white").grid(row=2, column=0, sticky="e", pady=5)
    label_coordinates_s = Label(right_frame, text="", font=("Segoe UI", 10), bg="#2e2e2e", fg="#8ee150")
    label_coordinates_s.grid(row=2, column=1, pady=5)

    selected_coordinates_s = [None]  # typ: [(lat, lon)]

    # Mapa dostawców (prawa kolumna)
    map_frame = tk.Frame(main_frame, bg="#2e2e2e", relief=tk.RIDGE, bd=2)
    map_frame.grid(row=1, column=2, padx=10, pady=10, sticky="n")
    map_suppliers = tkintermapview.TkinterMapView(map_frame, width=350, height=250)
    # domyślna pozycja na sklep, albo na Polskę
    start_lat, start_lon = shop.coordinates if shop.coordinates else (52.23, 21.0)
    map_suppliers.set_position(start_lat, start_lon)
    map_suppliers.set_zoom(13)
    map_suppliers.pack(fill="both", expand=True)

    # Pinezki dostawców na mapie
    supplier_markers = []

    def refresh_supplier_markers():
        for marker in supplier_markers:
            marker.delete()
        supplier_markers.clear()
        for supplier in shop.suppliers:
            if supplier.coordinates:
                marker = map_suppliers.set_marker(
                    supplier.coordinates[0], supplier.coordinates[1],
                    text=f"{supplier.name}",
                    icon=delivery_pin_image,
                    anchor="se",
                )
                supplier.marker = marker
                supplier_markers.append(marker)

    refresh_supplier_markers()

    # Dodawanie pinezki na mapie po kliknięciu
    selected_marker_s = [None]

    def on_map_click_s(event):
        lat, lon = map_suppliers.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        label_coordinates_s.config(text=f"{lat:.5f}, {lon:.5f}")
        selected_coordinates_s[0] = (lat, lon)
        if selected_marker_s[0]:
            selected_marker_s[0].delete()
        marker = map_suppliers.set_marker(lat, lon, text="Nowy dostawca", icon=delivery_pin_image, anchor="se")
        selected_marker_s[0] = marker

    map_suppliers.canvas.bind("<Button-1>", on_map_click_s)

    # Kliknięcie na dostawcę z listy – pokaż pinezkę do edycji na mapie
    def on_supplier_select(event):
        idx = lb.curselection()
        if not idx:
            return
        supplier = shop.suppliers[idx[0]]
        entry_name_s.delete(0, END)
        entry_name_s.insert(0, supplier.name)
        entry_contact.delete(0, END)
        entry_contact.insert(0, supplier.contact)
        if supplier.coordinates:
            label_coordinates_s.config(text=f"{supplier.coordinates[0]:.5f}, {supplier.coordinates[1]:.5f}")
            map_suppliers.set_position(supplier.coordinates[0], supplier.coordinates[1])
            if selected_marker_s[0]:
                selected_marker_s[0].delete()
            marker = map_suppliers.set_marker(supplier.coordinates[0], supplier.coordinates[1], text="Edytowany", icon=delivery_pin_image, anchor="se")
            selected_marker_s[0] = marker
            selected_coordinates_s[0] = supplier.coordinates
        else:
            label_coordinates_s.config(text="Brak")
            if selected_marker_s[0]:
                selected_marker_s[0].delete()
            selected_coordinates_s[0] = None

    lb.bind("<<ListboxSelect>>", on_supplier_select)

    # Dodawanie nowego dostawcy (wraz z pinezką)
    def add_supplier():
        name = entry_name_s.get()
        contact = entry_contact.get()
        coords = selected_coordinates_s[0]
        if not name or not contact or not coords:
            return
        supplier = Supplier(name, contact, coords)
        shop.suppliers.append(supplier)
        lb.insert(END, f"{len(shop.suppliers)}. {supplier.name} ({supplier.contact})")
        entry_name_s.delete(0, END)
        entry_contact.delete(0, END)
        label_coordinates_s.config(text="")
        if selected_marker_s[0]:
            selected_marker_s[0].delete()
            selected_marker_s[0] = None
        selected_coordinates_s[0] = None
        refresh_supplier_markers()

    # Edycja dostawcy (wraz z pinezką)
    def edit_supplier():
        idx = lb.curselection()
        if not idx:
            return
        supplier = shop.suppliers[idx[0]]
        supplier.name = entry_name_s.get()
        supplier.contact = entry_contact.get()
        coords = selected_coordinates_s[0]
        if coords:
            supplier.coordinates = coords
        lb.delete(idx[0])
        lb.insert(idx[0], f"{idx[0] + 1}. {supplier.name} ({supplier.contact})")
        entry_name_s.delete(0, END)
        entry_contact.delete(0, END)
        label_coordinates_s.config(text="")
        if selected_marker_s[0]:
            selected_marker_s[0].delete()
            selected_marker_s[0] = None
        selected_coordinates_s[0] = None
        refresh_supplier_markers()

    # Usuwanie dostawcy (wraz z pinezką)
    def delete_supplier():
        idx = lb.curselection()
        if not idx:
            return
        supplier = shop.suppliers[idx[0]]
        if supplier.marker:
            supplier.marker.delete()
        del shop.suppliers[idx[0]]
        lb.delete(idx[0])
        entry_name_s.delete(0, END)
        entry_contact.delete(0, END)
        label_coordinates_s.config(text="")
        if selected_marker_s[0]:
            selected_marker_s[0].delete()
            selected_marker_s[0] = None
        selected_coordinates_s[0] = None
        refresh_supplier_markers()

    button_frame = Frame(right_frame, bg="#2e2e2e")
    button_frame.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(button_frame, text="➕ Dodaj", bg="#fca47a", fg="black",
              activebackground="#943F25", font=("Segoe UI", 10, "bold"), command=add_supplier).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="🖉 Edytuj", bg="#fca47a", fg="black",
              activebackground="#943F25", font=("Segoe UI", 10, "bold"), command=edit_supplier).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="❌ Usuń", bg="#fca47a", fg="black",
              activebackground="#943F25", font=("Segoe UI", 10, "bold"), command=delete_supplier).grid(row=0, column=2, padx=5)




# === GŁÓWNE OKNO ===
shops = []

root = tk.Tk()
root.title("💼 Zarządzanie sklepami")
root.geometry("1300x750")
root.configure(bg="#121212")
shop_pin_image = tk.PhotoImage(file="shop_pin(1).png")
worker_pin_image = tk.PhotoImage(file="worker_pin(1).png")
delivery_pin_image = tk.PhotoImage(file="delivery_pin(1).png")

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
ramka_formularz_sklepow.pack(fill="both", expand=True, pady=(0, 10))  # Skrócone wypełnienie
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


button_pokaz_dostawcow = tk.Button(ramka_lista_sklepow, text="🚚 Pokaż dostawców", bg="#c38fff", fg="black", activebackground="#501e8a", font=("Segoe UI", 10, "bold"), command=show_suppliers_window)
button_pokaz_dostawcow.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()

