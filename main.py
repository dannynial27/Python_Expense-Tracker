import json
import os
import csv
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.align import Align
from rich import box
import pyfiglet

console = Console()
DATA_FILE = "expenses.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    clear_screen()
    ascii_banner = pyfiglet.figlet_format("EXPANSE", font="slant")
    console.print(f"[bold cyan]{ascii_banner}[/bold cyan]")
    subtitle = Panel(Align.center("[bold yellow]💰 Sistem Rekod dan Pemantauan Perbelanjaan Peribadi 💰[/bold yellow]"), box=box.ROUNDED, border_style="cyan")
    console.print(subtitle)
    console.print("\n")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_expense():
    show_header()
    amount_str = Prompt.ask("[bold green]💵 Masukkan jumlah (RM)[/bold green]")
    try:
        amount = float(amount_str)
    except ValueError:
        console.print("\n[bold red]❌ Ralat: Sila masukkan nilai nombor yang sah.[/bold red]")
        Prompt.ask("\nTekan [bold cyan]Enter[/bold cyan] untuk kembali.")
        return

    category = Prompt.ask("[bold blue]🏷️ Kategori (contoh: Makanan, Transport, Bil)[/bold blue]")
    description = Prompt.ask("[bold magenta]📝 Penerangan ringkas[/bold magenta]")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = load_data()
    data.append({
        "tarikh": date,
        "jumlah": amount,
        "kategori": category.title(),
        "penerangan": description.capitalize()
    })
    save_data(data)
    
    success_msg = Panel(f"✔ Berjaya menyimpan RM [bold green]{amount:.2f}[/bold green] untuk [bold blue]{category}[/bold blue]", border_style="green", expand=False)
    console.print("\n", success_msg)
    Prompt.ask("\nTekan [bold cyan]Enter[/bold cyan] untuk kembali.")

def view_expenses():
    show_header()
    data = load_data()
    if not data:
        console.print(Panel("📭 [bold yellow]Tiada rekod perbelanjaan ditemui buat masa ini.[/bold yellow]", border_style="yellow", expand=False))
        Prompt.ask("\nTekan [bold cyan]Enter[/bold cyan] untuk kembali.")
        return

    table = Table(title="\n[bold]📋 Senarai Perbelanjaan Semua[/bold]", box=box.HEAVY_EDGE, border_style="blue")
    table.add_column("ID", style="yellow", justify="center")
    table.add_column("Tarikh", style="dim")
    table.add_column("Kategori", style="bold magenta")
    table.add_column("Penerangan", style="cyan")
    table.add_column("Jumlah (RM)", justify="right", style="bold green")

    total = 0
    for i, item in enumerate(data, 1):
        amt = item['jumlah']
        color = "red" if amt > 100 else "green"
        table.add_row(str(i), item["tarikh"], item["kategori"], f"[{color}]{item['penerangan']}[/{color}]", f"[{color}]{amt:.2f}[/{color}]")
        total += amt

    console.print(table)
    total_panel = Panel(f"[bold white]Jumlah Keseluruhan Perbelanjaan: [bold red]RM {total:.2f}[/bold red][/bold white]", expand=False, border_style="red")
    console.print(total_panel)
    Prompt.ask("\nTekan [bold cyan]Enter[/bold cyan] untuk kembali.")

def view_summary():
    show_header()
    data = load_data()
    if not data:
        console.print("[bold yellow]📭 Tiada rekod perbelanjaan ditemui.[/bold yellow]\n")
        Prompt.ask("Tekan [bold cyan]Enter[/bold cyan] untuk kembali.")
        return
    
    summary = {}
    total = 0
    for item in data:
        cat = item["kategori"]
        amt = item["jumlah"]
        summary[cat] = summary.get(cat, 0) + amt
        total += amt
        
    table = Table(title="\n[bold]📊 Ringkasan Mengikut Kategori[/bold]", box=box.MINIMAL_DOUBLE_HEAD, border_style="magenta")
    table.add_column("Kategori", style="bold magenta")
    table.add_column("Jumlah (RM)", justify="right", style="bold green")
    table.add_column("Peratus (%)", justify="right", style="bold cyan")
    
    for cat, amt in sorted(summary.items(), key=lambda x: x[1], reverse=True):
        pct = (amt / total) * 100
        table.add_row(cat, f"{amt:.2f}", f"{pct:.1f}%")
        
    console.print(table)
    console.print(f"\n[bold green]💡 Jumlah: RM {total:.2f}[/bold green]\n")
    Prompt.ask("Tekan [bold cyan]Enter[/bold cyan] untuk kembali.")

def delete_expense():
    show_header()
    data = load_data()
    if not data:
        console.print("[bold yellow]📭 Tiada rekod perbelanjaan ditemui untuk dipadam.[/bold yellow]\n")
        Prompt.ask("Tekan [bold cyan]Enter[/bold cyan] untuk kembali.")
        return
    
    table = Table(box=box.SIMPLE, border_style="dim")
    table.add_column("ID", style="yellow")
    table.add_column("Kategori")
    table.add_column("Penerangan")
    table.add_column("RM")
    for i, item in enumerate(data, 1):
        table.add_row(str(i), item["kategori"], item["penerangan"], f"{item['jumlah']:.2f}")
    console.print(table)
    
    idx_input = Prompt.ask("\n[bold red]🗑️ Masukkan nombor ID untuk dipadam[/bold red] (tekan Enter untuk batal)")
    if not idx_input:
        return
    
    try:
        idx = int(idx_input)
        if 1 <= idx <= len(data):
            deleted = data.pop(idx - 1)
            save_data(data)
            console.print(f"\n[bold green]✔ Perbelanjaan '{deleted['penerangan']}' (RM {deleted['jumlah']:.2f}) berjaya dipadam![/bold green]")
        else:
            console.print("\n[bold red]❌ Nombor ID tidak wujud.[/bold red]")
    except ValueError:
        console.print("\n[bold red]❌ Ralat: Sila masukkan nombor yang sah.[/bold red]")
    
    Prompt.ask("\nTekan [bold cyan]Enter[/bold cyan] untuk kembali.")

def export_csv():
    show_header()
    data = load_data()
    if not data:
        console.print("[bold yellow]📭 Tiada rekod perbelanjaan ditemui untuk dieksport.[/bold yellow]\n")
        Prompt.ask("Tekan [bold cyan]Enter[/bold cyan] untuk kembali.")
        return
    
    filename = f"laporan_perbelanjaan_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Tarikh", "Kategori", "Penerangan", "Jumlah (RM)"])
        for item in data:
            writer.writerow([item["tarikh"], item["kategori"], item["penerangan"], item["jumlah"]])
            
    console.print(Panel(f"✅ Data berjaya dieksport ke dalam fail: [bold green]{filename}[/bold green]", border_style="green", expand=False))
    Prompt.ask("\nTekan [bold cyan]Enter[/bold cyan] untuk kembali.")

def main():
    while True:
        show_header()
        
        menu_text = (
            "[bold cyan]1.[/bold cyan] ➕ Tambah Perbelanjaan\n"
            "[bold cyan]2.[/bold cyan] 📋 Lihat Senarai Semua\n"
            "[bold cyan]3.[/bold cyan] 📊 Ringkasan Kategori\n"
            "[bold cyan]4.[/bold cyan] 🗑️ Padam Rekod\n"
            "[bold cyan]5.[/bold cyan] 📥 Eksport ke CSV\n"
            "[bold cyan]0.[/bold cyan] 🚪 Keluar"
        )
        
        console.print(Panel(menu_text, title="Pilihan Menu Utama", border_style="blue", expand=False))
        
        pilihan = Prompt.ask("\n[bold cyan]Sila masukkan pilihan anda[/bold cyan]", choices=["1", "2", "3", "4", "5", "0"], default="1")

        if pilihan == "1":
            add_expense()
        elif pilihan == "2":
            view_expenses()
        elif pilihan == "3":
            view_summary()
        elif pilihan == "4":
            delete_expense()
        elif pilihan == "5":
            export_csv()
        elif pilihan == "0":
            if Confirm.ask("[bold red]Adakah anda pasti mahu keluar?[/bold red]"):
                console.print("\n[bold green]Terima kasih! Semoga cermat berbelanja. 👋[/bold green]\n")
                break

if __name__ == "__main__":
    main()
