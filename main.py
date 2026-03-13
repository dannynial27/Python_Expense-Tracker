import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()
DATA_FILE = "expenses.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_expense():
    amount = console.input("[bold cyan]Masukkan jumlah (RM): [/bold cyan]")
    try:
        amount = float(amount)
    except ValueError:
        console.print("[bold red]Ralat: Sila masukkan nombor yang sah.[/bold red]\n")
        return

    category = console.input("[bold cyan]Kategori (contoh: makanan/transport/bil): [/bold cyan]")
    description = console.input("[bold cyan]Penerangan ringkas: [/bold cyan]")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = load_data()
    data.append({
        "tarikh": date,
        "jumlah": amount,
        "kategori": category,
        "penerangan": description
    })
    save_data(data)
    console.print("[bold green]✔ Perbelanjaan berjaya direkodkan![/bold green]\n")

def view_expenses():
    data = load_data()
    if not data:
        console.print("[bold yellow]Tiada rekod perbelanjaan ditemui.[/bold yellow]\n")
        return

    table = Table(title="Senarai Perbelanjaan")
    table.add_column("Tarikh", style="dim")
    table.add_column("Kategori", style="magenta")
    table.add_column("Penerangan", style="cyan")
    table.add_column("Jumlah (RM)", justify="right", style="green")

    total = 0
    for item in data:
        table.add_row(item["tarikh"], item["kategori"], item["penerangan"], f"{item['jumlah']:.2f}")
        total += item["jumlah"]

    console.print(table)
    console.print(f"[bold green]Jumlah Keseluruhan: RM {total:.2f}[/bold green]\n")

def main():
    while True:
        console.print("\n[bold blue]== Sistem Rekod Perbelanjaan ==[/bold blue]")
        console.print("1. Tambah Perbelanjaan")
        console.print("2. Lihat Senarai Perbelanjaan")
        console.print("3. Keluar")
        pilihan = console.input("\n[bold cyan]Pilih menu (1/2/3): [/bold cyan]")

        if pilihan == "1":
            add_expense()
        elif pilihan == "2":
            view_expenses()
        elif pilihan == "3":
            console.print("[bold green]Terima kasih! Selamat tinggal.[/bold green]")
            break
        else:
            console.print("[bold red]Pilihan tidak sah.[/bold red]\n")

if __name__ == "__main__":
    main()
