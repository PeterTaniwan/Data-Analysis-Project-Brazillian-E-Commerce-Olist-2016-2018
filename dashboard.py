import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="whitegrid")

base_dir = os.path.dirname(__file__)

main_df = pd.read_csv(os.path.join(base_dir, "main_data.csv"))
monthly_sales_df = pd.read_csv(os.path.join(base_dir, "monthly_sales.csv"))
rfm_df = pd.read_csv(os.path.join(base_dir, "rfm_data.csv"))
segment_summary_df = pd.read_csv(os.path.join(base_dir, "segment_summary.csv"))

monthly_sales_df["order_month_date"] = pd.to_datetime(monthly_sales_df["order_month_date"])

st.title("Brazilian E-Commerce Dashboard")
st.caption("Dashboard untuk melihat tren penjualan bulanan dan segmentasi pelanggan berdasarkan RFM analysis")

st.sidebar.header("Filter Data")
month_options = sorted(monthly_sales_df["order_month"].unique())
selected_month = st.sidebar.multiselect(
    "Pilih bulan transaksi",
    month_options,
    default=month_options
)

filtered_monthly_df = monthly_sales_df[monthly_sales_df["order_month"].isin(selected_month)]

total_order = int(filtered_monthly_df["total_order"].sum())
total_revenue = filtered_monthly_df["total_revenue"].sum()
avg_revenue_per_order = total_revenue / total_order if total_order > 0 else 0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Pesanan", f"{total_order:,}")

with col2:
    st.metric("Total Pendapatan", f"{total_revenue:,.0f}")

with col3:
    st.metric("Rata-Rata Pendapatan per Order", f"{avg_revenue_per_order:,.0f}")

tab1, tab2 = st.tabs(["Tren Penjualan", "Segmentasi Pelanggan"])

with tab1:
    st.header("Tren Performa Penjualan Bulanan")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(
        data=filtered_monthly_df,
        x="order_month_date",
        y="total_order",
        marker="o",
        ax=ax
    )
    ax.set_title("Tren Jumlah Pesanan per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(
        data=filtered_monthly_df,
        x="order_month_date",
        y="total_revenue",
        marker="o",
        ax=ax
    )
    ax.set_title("Tren Total Pendapatan per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Pendapatan")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Data Tren Bulanan")
    st.dataframe(filtered_monthly_df[["order_month", "total_order", "total_revenue"]])

with tab2:
    st.header("Segmentasi Pelanggan Berdasarkan RFM")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=segment_summary_df.sort_values("total_customer", ascending=False),
        x="total_customer",
        y="customer_segment",
        color="steelblue",
        ax=ax
    )
    ax.set_title("Jumlah Pelanggan pada Setiap Segmen RFM")
    ax.set_xlabel("Jumlah Pelanggan")
    ax.set_ylabel("Segmen Pelanggan")
    plt.tight_layout()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=segment_summary_df.sort_values("avg_monetary", ascending=False),
        x="avg_monetary",
        y="customer_segment",
        color="steelblue",
        ax=ax
    )
    ax.set_title("Rata-Rata Monetary pada Setiap Segmen RFM")
    ax.set_xlabel("Rata-Rata Monetary")
    ax.set_ylabel("Segmen Pelanggan")
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Ringkasan Segmen")
    st.dataframe(segment_summary_df)

    st.subheader("Contoh Data RFM")
    st.dataframe(rfm_df.head(20))
