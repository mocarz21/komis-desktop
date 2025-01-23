import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime

# Funkcja do pobierania danych z API
def fetch_data():
    url = "http://127.0.0.1:7474/drives/"  # Podmień na swój URL endpointa
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return sorted(data, key=lambda x: (x['test_drive_date'], x['test_drive_time']))
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas łączenia z API: {e}")
        return []

# Funkcja do aktualizacji tabeli
def update_table():
    for row in tree.get_children():
        tree.delete(row)

    data = fetch_data()
    for item in data:
        test_drive_datetime = f"{item['test_drive_date']} {item['test_drive_time']}"
        tree.insert("", "end", values=(
            test_drive_datetime,
            item['user_first_name'],
            item['user_last_name'],
            item['car_brand'],
            item['car_model']
        ))

# Tworzenie okna aplikacji
root = tk.Tk()
root.title("Dane Jazd Testowych")

# Tworzenie tabeli
columns = ("Data i godzina", "Imię", "Nazwisko", "Marka", "Model")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill=tk.BOTH, expand=True)

# Dodanie przycisku do odświeżania danych
refresh_button = tk.Button(root, text="Odśwież dane", command=update_table)
refresh_button.pack(pady=10)

# Wczytanie danych na start
update_table()

# Uruchomienie pętli aplikacji
root.mainloop()