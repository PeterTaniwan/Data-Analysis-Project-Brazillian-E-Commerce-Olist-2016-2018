# Brazilian E-Commerce Dashboard

Project ini menganalisis Brazilian E-Commerce Public Dataset by Olist.

## Pertanyaan Bisnis

1. Bagaimana tren performa penjualan e-commerce dari bulan ke bulan berdasarkan jumlah pesanan dan total pendapatan, lalu pada bulan apa penjualan tertinggi terjadi?
2. Bagaimana segmentasi pelanggan berdasarkan perilaku belanjanya dengan RFM analysis lalu kelompok pelanggan mana yang paling berharga (Loyal/VIP) bagi bisnis?

## Struktur Folder

```text
submission
├── dashboard
│   ├── dashboard.py
│   ├── main_data.csv
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

## Cara Menjalankan Notebook

1. Buka file `notebook.ipynb`.
2. Jalankan seluruh cell dari awal sampai akhir.
3. Pastikan folder `data` berada dalam direktori yang sama dengan notebook.

## Cara Menjalankan Dashboard

Jalankan perintah berikut dari folder utama submission:

```bash
streamlit run dashboard/dashboard.py
```

## Library yang Digunakan

- pandas
- matplotlib
- seaborn
- streamlit
