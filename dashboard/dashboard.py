from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "main_data.csv"

st.set_page_config(
    page_title="Olist E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    datetime_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "order_month_date",
        "order_date"
    ]

    for column in datetime_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column])

    df = df.sort_values("order_purchase_timestamp")
    return df


def format_currency(value):
    return f"R$ {value:,.0f}"


def format_number(value):
    return f"{int(value):,}"

def center_table(df):
    return (
        df.style
        .set_table_styles([
            {"selector": "th", "props": [("text-align", "center")]},
            {"selector": "td", "props": [("text-align", "center")]}
        ])
        .set_properties(**{"text-align": "center"})
    )

def create_monthly_sales_df(df):
    monthly_df = df.groupby(["order_month", "order_month_date"], as_index=False).agg(
        order_count=("order_id", "nunique"),
        total_revenue=("payment_value", "sum"),
        avg_revenue_per_order=("payment_value", "mean")
    )

    return monthly_df.sort_values("order_month_date")


def create_rfm_df(df):
    if df.empty:
        return pd.DataFrame(columns=[
            "customer_unique_id", "recency", "frequency", "monetary",
            "r_score", "f_score", "m_score", "rfm_score", "customer_segment"
        ])

    snapshot_date = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

    rfm_df = df.groupby("customer_unique_id", as_index=False).agg(
        last_order_date=("order_purchase_timestamp", "max"),
        frequency=("order_id", "nunique"),
        monetary=("payment_value", "sum")
    )

    rfm_df["recency"] = (snapshot_date - rfm_df["last_order_date"]).dt.days

    if len(rfm_df) >= 4:
        rfm_df["r_score"] = pd.qcut(
            rfm_df["recency"].rank(method="first"),
            4,
            labels=[4, 3, 2, 1]
        ).astype(int)

        rfm_df["f_score"] = pd.qcut(
            rfm_df["frequency"].rank(method="first"),
            4,
            labels=[1, 2, 3, 4]
        ).astype(int)

        rfm_df["m_score"] = pd.qcut(
            rfm_df["monetary"].rank(method="first"),
            4,
            labels=[1, 2, 3, 4]
        ).astype(int)
    else:
        rfm_df["r_score"] = 1
        rfm_df["f_score"] = 1
        rfm_df["m_score"] = 1

    rfm_df["rfm_score"] = (
        rfm_df["r_score"].astype(str) +
        rfm_df["f_score"].astype(str) +
        rfm_df["m_score"].astype(str)
    )

    def define_customer_segment(row):
        if row["r_score"] >= 3 and row["f_score"] >= 3 and row["m_score"] >= 3:
            return "Loyal/VIP Customer"
        elif row["r_score"] >= 3 and row["f_score"] <= 2:
            return "New Customer"
        elif row["r_score"] <= 2 and row["f_score"] >= 3 and row["m_score"] >= 3:
            return "At Risk High Value"
        elif row["m_score"] >= 3:
            return "Potential Customer"
        else:
            return "Regular Customer"

    rfm_df["customer_segment"] = rfm_df.apply(define_customer_segment, axis=1)

    return rfm_df


def create_segment_summary_df(rfm_df):
    if rfm_df.empty:
        return pd.DataFrame(columns=[
            "customer_segment", "customer_count", "avg_recency",
            "avg_frequency", "avg_monetary", "total_monetary"
        ])

    summary_df = rfm_df.groupby("customer_segment", as_index=False).agg(
        customer_count=("customer_unique_id", "nunique"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
        total_monetary=("monetary", "sum")
    )

    return summary_df.sort_values("avg_monetary", ascending=False)


all_df = load_data()

min_date = all_df["order_date"].min().date()
max_date = all_df["order_date"].max().date()

with st.sidebar:
    st.title("Filter Dashboard")
    st.caption("Silakan pilih periode transaksi yang ingin dianalisis.")

    selected_dates = st.date_input(
        label="Rentang Tanggal Transaksi",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date, end_date = min_date, max_date


main_df = all_df[
    (all_df["order_date"].dt.date >= start_date) &
    (all_df["order_date"].dt.date <= end_date)
].copy()

if main_df.empty:
    st.warning("Tidak ada data pada rentang tanggal yang dipilih. Silakan pilih rentang tanggal lain.")
    st.stop()


monthly_sales_df = create_monthly_sales_df(main_df)
rfm_df = create_rfm_df(main_df)
segment_summary_df = create_segment_summary_df(rfm_df)

with st.sidebar:
    segment_options = sorted(rfm_df["customer_segment"].dropna().unique()) if not rfm_df.empty else []

    selected_segments = st.multiselect(
        label="Pilih Segmen Pelanggan",
        options=segment_options,
        default=segment_options
    )


if selected_segments:
    filtered_rfm_df = rfm_df[rfm_df["customer_segment"].isin(selected_segments)].copy()
else:
    filtered_rfm_df = rfm_df.copy()

filtered_segment_summary_df = create_segment_summary_df(filtered_rfm_df)


st.title("Olist E-Commerce Sales & Customer Dashboard 🛒")

st.markdown(
    "Dashboard ini menampilkan tren penjualan bulanan dan segmentasi pelanggan "
    "berdasarkan RFM analysis untuk transaksi berstatus delivered pada periode "
    "Oktober 2016-Agustus 2018."
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Orders", f"{main_df['order_id'].nunique():,}")

with col2:
    st.metric("Total Revenue", format_currency(main_df["payment_value"].sum()))

with col3:
    st.metric("Total Customers", f"{main_df['customer_unique_id'].nunique():,}")

with col4:
    st.metric("Avg Revenue / Order", format_currency(main_df["payment_value"].mean()))


tab_sales, tab_rfm, tab_data = st.tabs(["Sales Trend", "RFM Segment", "Data Preview"])


with tab_sales:
    st.subheader("Tren Performa Penjualan Bulanan")
    st.caption(
        "Visualisasi ini menjawab pertanyaan bisnis pertama terkait jumlah pesanan "
        "dan total pendapatan bulanan."
    )

    if not monthly_sales_df.empty:
        peak_revenue_month = monthly_sales_df.sort_values(
            "total_revenue",
            ascending=False
        ).iloc[0]

        st.info(
            f"Bulan dengan total pendapatan tertinggi pada periode terpilih adalah "
            f"{peak_revenue_month['order_month']} dengan revenue "
            f"{format_currency(peak_revenue_month['total_revenue'])}."
        )

    fig, ax = plt.subplots(figsize=(12, 5))

    sns.lineplot(
        data=monthly_sales_df,
        x="order_month_date",
        y="order_count",
        marker="o",
        color="#4C72B0",
        ax=ax
    )

    ax.set_title("Tren Jumlah Pesanan Bulanan", fontsize=13, pad=12)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    sns.despine()
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)

    fig, ax = plt.subplots(figsize=(12, 5))

    sns.lineplot(
        data=monthly_sales_df,
        x="order_month_date",
        y="total_revenue",
        marker="o",
        color="#4C72B0",
        ax=ax
    )

    ax.set_title("Tren Total Pendapatan Bulanan", fontsize=13, pad=12)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Pendapatan")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    sns.despine()
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)


with tab_rfm:
    st.subheader("Segmentasi Pelanggan Berdasarkan RFM Analysis")
    st.caption(
        "Visualisasi ini menjawab pertanyaan bisnis kedua terkait kelompok pelanggan "
        "paling berharga."
    )

    if not filtered_segment_summary_df.empty:
        top_segment = filtered_segment_summary_df.sort_values(
            "avg_monetary",
            ascending=False
        ).iloc[0]

        st.info(
            f"Segmen dengan rata-rata monetary tertinggi pada filter saat ini adalah "
            f"{top_segment['customer_segment']} dengan rata-rata monetary "
            f"{format_currency(top_segment['avg_monetary'])}."
        )

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric("Avg Recency", f"{filtered_rfm_df['recency'].mean():.1f} hari")

        with col_b:
            st.metric("Avg Frequency", f"{filtered_rfm_df['frequency'].mean():.2f}")

        with col_c:
            st.metric("Avg Monetary", format_currency(filtered_rfm_df["monetary"].mean()))

        fig, ax = plt.subplots(figsize=(10, 5))

        plot_df = filtered_segment_summary_df.sort_values(
            "customer_count",
            ascending=False
        )

        sns.barplot(
            data=plot_df,
            x="customer_count",
            y="customer_segment",
            ax=ax,
            color="#4C72B0"
        )

        ax.set_title("Jumlah Pelanggan per Segmen RFM", fontsize=13, pad=12)
        ax.set_xlabel("Jumlah Pelanggan")
        ax.set_ylabel("Segmen Pelanggan")

        for container in ax.containers:
            ax.bar_label(
                container,
                labels=[format_number(v) for v in container.datavalues],
                padding=5,
                fontsize=9
            )

        ax.set_xlim(0, plot_df["customer_count"].max() * 1.15)

        sns.despine()
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)

        fig, ax = plt.subplots(figsize=(10, 5))

        plot_df = filtered_segment_summary_df.sort_values(
            "avg_monetary",
            ascending=False
        )

        sns.barplot(
            data=plot_df,
            x="avg_monetary",
            y="customer_segment",
            ax=ax,
            color="#4C72B0"
        )

        ax.set_title("Rata-Rata Monetary per Segmen RFM", fontsize=13, pad=12)
        ax.set_xlabel("Rata-Rata Monetary")
        ax.set_ylabel("Segmen Pelanggan")

        for container in ax.containers:
            ax.bar_label(
                container,
                labels=[format_currency(v) for v in container.datavalues],
                padding=5,
                fontsize=9
            )

        ax.set_xlim(0, plot_df["avg_monetary"].max() * 1.20)

        sns.despine()
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)

        st.markdown("### Ringkasan Segmen RFM")
        st.dataframe(filtered_segment_summary_df, use_container_width=True)

    else:
        st.warning("Tidak ada segmen pelanggan pada filter yang dipilih.")


with tab_data:
    st.subheader("Preview Data yang Digunakan Dashboard")
    st.caption(
        "Data ini berasal dari file dashboard/main_data.csv yang sudah dibersihkan dari notebook."
    )

    st.markdown("### Preview Data")
    st.dataframe(main_df.head(50), use_container_width=True)

    st.markdown("### Ringkasan Statistik Data Numerik")

    numeric_cols = main_df.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()

    if numeric_cols:
        numeric_summary_df = main_df[numeric_cols].describe().T.reset_index()

        numeric_summary_df = numeric_summary_df.rename(columns={
            "index": "column",
            "count": "count",
            "mean": "mean",
            "std": "std",
            "min": "min",
            "25%": "q1",
            "50%": "median",
            "75%": "q3",
            "max": "max"
        })

        st.dataframe(numeric_summary_df, use_container_width=True)
    else:
        st.info("Tidak ada kolom numerik pada data yang sedang difilter.")

    st.markdown("### Ringkasan Statistik Data Kategorik")

    categorical_cols = main_df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    if categorical_cols:
        categorical_summary_df = main_df[categorical_cols].describe().T.reset_index()

        categorical_summary_df = categorical_summary_df.rename(columns={
            "index": "column",
            "count": "count",
            "unique": "unique",
            "top": "most_frequent_value",
            "freq": "frequency"
        })

        st.dataframe(categorical_summary_df, use_container_width=True)

        st.markdown("### Frekuensi 10 Data Teratas pada Kolom Kategorik")

        selected_cat_col = st.selectbox(
            label="Pilih kolom kategorik",
            options=categorical_cols
        )

        category_count_df = main_df[selected_cat_col].value_counts().head(10).reset_index()
        category_count_df.columns = [selected_cat_col, "count"]

        st.dataframe(category_count_df, use_container_width=True)

    else:
        st.info("Tidak ada kolom kategorik pada data yang sedang difilter.")