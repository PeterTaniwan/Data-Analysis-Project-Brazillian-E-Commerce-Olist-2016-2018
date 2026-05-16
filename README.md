# Olist E-Commerce Sales & Customer Dashboard ✨

Project Analisis Data menggunakan **Brazilian E-Commerce Public Dataset by Olist**. Analisis berfokus pada tren performa penjualan dan segmentasi pelanggan menggunakan RFM analysis.

## Business Questions

1. **Pertanyaan 1:** Bagaimana tren performa penjualan Olist dari bulan ke bulan berdasarkan jumlah pesanan dan total pendapatan pada transaksi berstatus `delivered` selama periode Oktober 2016-Agustus 2018, lalu pada bulan apa penjualan tertinggi terjadi?
2. **Pertanyaan 2:** Bagaimana segmentasi pelanggan Olist berdasarkan perilaku belanjanya menggunakan RFM analysis pada transaksi berstatus `delivered` selama periode Oktober 2016-Agustus 2018, lalu segmen pelanggan mana yang paling berharga berdasarkan rata-rata monetary?

## Project Structure

```text
submission
├── dashboard
│   ├── dashboard.py
│   └── main_data.csv
├── data
│   ├── customers_dataset.csv
│   ├── order_payments_dataset.csv
│   └── orders_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Software Version

Project ini disiapkan agar bisa dijalankan pada Python berikut.

```text
Python 3.14.2
```

## Setup Environment - Anaconda

```bash
conda create --name main-ds python=3.14
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Untuk pengguna Mac/Linux, aktivasi virtual environment dapat menggunakan perintah berikut.

```bash
source .venv/bin/activate
```

## Setup Environment - Pipenv

```bash
pip install pipenv
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Notebook

1. Buka file `notebook.ipynb` menggunakan Jupyter Notebook, JupyterLab, Google Colab, atau VS Code.
2. Pastikan folder `data` berada pada direktori yang sama dengan notebook.
3. Pilih kernel Python yang sudah terpasang library pada `requirements.txt`.
4. Jalankan seluruh cell dari awal sampai akhir.
5. Output tabel dan visualisasi akan muncul langsung di notebook.

## Run Streamlit App

Pastikan posisi terminal berada pada folder utama `submission`, lalu jalankan perintah berikut.

```bash
streamlit run dashboard/dashboard.py
```

Jika perintah `streamlit` tidak terbaca, gunakan perintah alternatif berikut.

```bash
python -m streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka secara otomatis pada browser. Jika tidak terbuka otomatis, akses alamat berikut.

```text
http://localhost:8501
```

## Dashboard Features

- Menampilkan metrik utama: total orders, total revenue, total customers, dan average revenue per order.
- Menampilkan tren jumlah pesanan bulanan.
- Menampilkan tren total pendapatan bulanan.
- Menampilkan segmentasi pelanggan berdasarkan RFM analysis.
- Menampilkan jumlah pelanggan dan rata-rata monetary per segmen RFM.
- Menyediakan filter interaktif berbasis **date picker** untuk memilih rentang tanggal transaksi.
- Menyediakan filter interaktif berbasis **multiselect** untuk memilih segmen pelanggan.

## Deploy to Streamlit Community Cloud

1. Upload isi folder `submission` ke repository GitHub.
2. Pastikan file berikut tersedia di repository:
   - `dashboard/dashboard.py`
   - `dashboard/main_data.csv`
   - `requirements.txt`
   - `README.md`
3. Buka Streamlit Community Cloud.
4. Pilih repository GitHub yang berisi project ini.
5. Isi **Main file path** dengan:

```text
dashboard/dashboard.py
```

6. Klik **Deploy**.
7. Salin link hasil deploy ke file `url.txt`.

## Requirements

Daftar library yang digunakan tersedia pada file `requirements.txt`.
