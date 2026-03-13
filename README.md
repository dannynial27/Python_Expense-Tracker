# Sistem Rekod Perbelanjaan (Expense Tracker)

Ini adalah sebuah aplikasi Python Command-Line Interface (CLI) untuk merekod dan memantau perbelanjaan harian anda. Aplikasi ini menggunakan library `rich` untuk memaparkan output terminal yang cantik dan teratur di dalam bentuk jadual.

## Ciri-ciri
- Tambah rekod perbelanjaan berserta jumlah, kategori, dan penerangan.
- Lihat senarai perbelanjaan dalam bentuk jadual yang interaktif.
- Lihat ringkasan keseluruhan berdasarkan kategori (peratusan dan jumlah).
- Padam rekod perbelanjaan jika tersalah isi.
- Pengiraan jumlah keseluruhan semua perbelanjaan secara automatik.
- Data disimpan secara kekal (persisten) di dalam fail `expenses.json`.

## Cara Pemasangan & Penggunaan

1. Pastikan anda mempunyai prapemasangan Python.
2. Pasang library yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   python main.py
   ```
