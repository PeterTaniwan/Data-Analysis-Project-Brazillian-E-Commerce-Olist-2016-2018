# Brazilian E-Commerce Olist Dashboard 

Dashboard ini menggunakan dataset **Brazilian E-Commerce Public Dataset by Olist**. Fokus analisisnya adalah tren penjualan bulanan dan segmentasi pelanggan menggunakan RFM analysis.

## Business Questions

1. Bagaimana tren performa penjualan Olist ari bulan ke bulan berdasarkan jumlah pesanan dan total pendapatan pada transaksi berstatus delivered selama periode Oktober 2016 - Agustus 2018, lalu pada bulan apa penjualan tertinggi terjadi?
2. Bagaimana segmentasi pelanggan Olist berdasarkan perilaku belanjanya dengan RFM analysis pada transaksi berstatus delivered selama periode Oktober 2016 - Agustus 2018 lalu kelompok pelanggan mana yang paling berharga (Loyal/VIP) bagi bisnis?

## Struktur Proyek

```text
submission
├── dashboard
│   ├── dashboard.py
│   ├── monthly_sales.csv
│   ├── rfm_data.csv
│   └── segment_summary.csv
├── data
│   ├── customers_dataset.csv
│   ├── order_payments_dataset.csv
│   └── orders_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Setup Environment - Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Setup File Project

Apabila project belum berada di folder `proyek_analisis_data`, maka pindahkan semua file dan folder submission ke dalam folder tersebut sehingga struktur project tetap seperti berikut:

```text
proyek_analisis_data
├── dashboard
├── data
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Run Notebook

Untuk menjalankan notebook analisis data, buka file berikut menggunakan Jupyter Notebook, JupyterLab, Google Colab, atau VS Code.

```bash
jupyter notebook notebook.ipynb
```

Pastikan folder `data` berada pada direktori yang sama dengan file `notebook.ipynb` supaya proses pembacaan dataset dapat berjalan dengan benar.

## Run Streamlit App

Pastikan posisi terminal berada pada folder utama project, lalu jalankan perintah berikut.

```bash
streamlit run dashboard/dashboard.py
```

Jika perintah `streamlit` tidak terbaca, gunakan alternatif berikut.

```bash
python -m streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka secara otomatis di browser. Jika tidak terbuka otomatis, akses alamat lokal berikut.

```text
http://localhost:8501
```

## Dashboard Features

Dashboard sederhana ini menampilkan beberapa informasi utama berikut.

- Tren jumlah pesanan bulanan selama periode Oktober 2016-Agustus 2018.
- Tren total pendapatan bulanan selama periode Oktober 2016-Agustus 2018.
- Ringkasan jumlah pelanggan berdasarkan segmen RFM.
- Ringkasan rata-rata monetary berdasarkan segmen RFM.
- Filter interaktif berdasarkan rentang bulan transaksi.
- Filter interaktif berdasarkan segmen pelanggan.

## Deploy to Streamlit Cloud

1. Upload seluruh file project ke repository GitHub.
2. Buka Streamlit Community Cloud.
3. Pilih repository GitHub yang berisi project ini.
4. Pada bagian **Main file path**, isi dengan path berikut.

```text
dashboard/dashboard.py
```

5. Klik **Deploy**.
6. Salin link dashboard yang berhasil dibuat ke dalam file `url.txt`.

## Requirements

Daftar library yang digunakan terdapat pada file `requirements.txt`.

