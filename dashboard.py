import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

all_df = pd.read_csv("all_df.csv")


# Sidebar
with st.sidebar:
    # Menambahkan judul
    st.text('Welcome to my dashboard')

    # Menambahkan logo
    st.image("https://raw.githubusercontent.com/annisaprmts/analysis/master/mylogo.png", width=300)

    # Menambahkan informasi pribadi
    st.text('Nama : Annisa Permata Sari')
    st.text('Email : m011d4kx2767@bangkit.academy')
    st.text('ID Dicoding : annisa_permataa')

st.title('E-Commerce Public Dataset Dashboard :sparkles:')
st.image("https://raw.githubusercontent.com/annisaprmts/analysis/master/mylogo.png", width=300)

# Container 1
with st.container():
    st.subheader("**Mari Lihat Produk Terlaris Kami!**")

    sum_products_df = all_df.groupby("product_category_name").product_id.count().sort_values(ascending=False).reset_index()
    sum_products_df.head(15)

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 8))
    colors = ["#BA55D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(x="product_id", y="product_category_name", hue="product_category_name", data=sum_products_df.head(5), palette=colors, ax=ax, legend=False)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis ='y', labelsize=12)
    plt.suptitle("Produk Terlaris", fontsize=20)

    # Menampilkan plot menggunakan st.pyplot()
    st.pyplot(fig)

with st.expander("Penjelasan Produk Terlaris"):
    st.write(
        """Berdasarkan visualisasi 
        grafik dapat disimpulkan bahwa produk terlaris 
        pada platform *e-commerce* adalah Cama_Mesa_Banho 
        dan diikuti oleh produk Beleza_Saude, Esporte_Lazer, 
        Moveis_Decoracao, dan Informatica_Acessorios."""
    )

# Container 2
with st.container():
    st.subheader("Metode Pembayaran Apa yang Paling Banyak Digunakan?")

    sum_payments_df = all_df.groupby("payment_type").order_id.count().sort_values(ascending=False).reset_index()
    sum_payments_df.head(15)

    bypayments_df = all_df.groupby(by="payment_type").order_id.nunique().reset_index()
    bypayments_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)

    fig, ax = plt.subplots(figsize=(10, 5))

    colors = ["#DA70D6", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        x="payment_type",
        y="order_count",
        hue="payment_type",  # Menetapkan variabel x sebagai hue
        data=bypayments_df.sort_values(by="order_count", ascending=False),
        palette=colors,
        ax=ax,
        legend=False  # Menetapkan legend menjadi False
    )
    plt.title("Jumlah Order berdasarkan Tipe Pembayaran", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='x', labelsize=12)

    # Menampilkan plot menggunakan st.pyplot() dengan menyertakan objek gambar
    st.pyplot(fig)

with st.expander("Penjelasan Tipe Pembayaran"):
    st.write(
        """Berdasarkan visualisasi grafik dapat 
        disimpulkan bahwa tipe pembayaran yang paling 
        digunakan adalah pembayaran dengan credit card 
        dan diikuti oleh boleto, voucher, dan debit card."""
    )

# Container 3
with st.container():
    st.subheader("Apakah Pelanggan Puas dengan Platform E-Commerce Kami?")

    sum_reviews_df = all_df.groupby("review_score").order_id.count().sort_values(ascending=False).reset_index()
    sum_reviews_df.head(15)

    # Membuat kamus yang memetakan nilai skor ke keterangan labelnya
    keterangan = {
        5: 'Sangat Tidak Puas',
        4: 'Tidak Puas',
        3: 'Netral',
        2: 'Puas',
        1: 'Sangat Puas'
    }

    colors = ["#9400D3", "#BA55D3", "#DDA0DD", "#D8BFD8", "#EDEDFA"]

    sum_reviews_df['review_score'] = 'Skor ' + sum_reviews_df['review_score'].astype(str)

    # Membuat diagram pie
    fig, ax = plt.subplots()
    ax.pie(
        x=sum_reviews_df['order_id'],
        labels=sum_reviews_df['review_score'],
        autopct='%1.1f%%',
        colors=colors,
        wedgeprops={'width': 0.6, 'linewidth': 2, 'edgecolor': 'white'}
    )
    ax.set_title("Perbandingan Skor Kepuasan Pelanggan", loc="center", fontsize=15)
    ax.legend(labels=[keterangan[score] for score in range(1, 6)], loc='upper right', bbox_to_anchor=(1.4, 1))

    # Menampilkan plot menggunakan st.pyplot() dengan menyertakan objek gambar
    st.pyplot(fig)

with st.expander("Penjelasan Kepuasan Pelanggan"):
    st.write(
        """Berdasarkan visualisasi grafik dapat 
        disimpulkan bahwa platform *e-commerce* paling 
        banyak mendapatkan skor 5 dan diikuti oleh skor 4, 
        skor 1, skor 3, skor 3, dan terakhir skor 2."""
    )

# Container 4
# Konversi kolom order_approved_at menjadi tipe data datetime dengan menetapkan dayfirst=True
all_df['order_approved_at'] = pd.to_datetime(all_df['order_approved_at'], dayfirst=True)

# Tetapkan kolom order_approved_at sebagai indeks DataFrame
all_df.set_index('order_approved_at', inplace=True)

with st.container():
    st.header("Bagaimana Perkembangan Penjualan Tahun Ini?")

    # Resampling berdasarkan bulan
    month_df = all_df.resample(rule='ME').agg({
        "order_id": "nunique",
    })
    month_df.index = month_df.index.strftime('%B')
    month_df = month_df.reset_index()
    month_df.rename(columns={
        "order_id": "order_count",
    }, inplace=True)

    month_df.head()
    month_df = month_df.sort_values('order_count').drop_duplicates('order_approved_at', keep='last')
    month_df.head()
    month_number = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    month_df["month_numeric"] = month_df["order_approved_at"].map(month_number)
    month_df = month_df.sort_values("month_numeric")
    month_df = month_df.drop("month_numeric", axis=1)

    plt.figure(figsize=(12, 8))
    plt.plot(
        month_df["order_approved_at"],
        month_df["order_count"],
        marker='o',
        linewidth=2,
        color="#663399"
    )
    plt.title("Jumlah Order tiap Bulan per 2018", loc="center", fontsize=20)
    plt.xticks(fontsize=10, rotation=30)
    plt.yticks(fontsize=10)

    # Menampilkan plot menggunakan streamlit.pyplot()
    st.pyplot(plt)

with st.expander("Penjelasan Perkembangan Penjualan"):
    st.write(
        """Berdasarkan visualisasi grafik dapat 
        disimpulkan bahwa terjadi kenaikan dan penurunan 
        penjualan dari bulan Januari sampai bulan Agustus. 
        Mulai dari bulan Agustus terjadi penurunan yang sangat 
        signifikan sampai bulan September. Mulai dari bulan 
        September terjadi kenaikan penjualan sampai bulan 
        Oktober dan terjadi kenaikan yang sangat signifikan 
        sampai bulan November. Pada bulan Desember terjadi 
        penurunan yang cukup signifikan dari bulan November 
        sebelumnya."""
    )

# RFM Analysis
# Ubah kolom order_purchase_timestamp menjadi tipe data datetime jika belum
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'], dayfirst=True)

# Hitung RFM metrics
rfm_df = all_df.groupby(by="customer_id", as_index=False).agg({
    "order_purchase_timestamp": "max",  # mengambil tanggal order terakhir
    "order_id": "nunique",  # menghitung jumlah order
    "payment_value": "sum"  # menghitung jumlah revenue yang dihasilkan
})
rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

# Menghitung kapan terakhir pelanggan melakukan transaksi (hari)
rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
recent_date = all_df["order_purchase_timestamp"].dt.date.max()
rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)

rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
rfm_df.head()

# By Recency (days)
fig1, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
sns.barplot(x="recency", y="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), ax=ax1)
ax1.set_ylabel(None)
ax1.set_xlabel(None)
ax1.set_title("By Recency (days)", loc="center", fontsize=18)
ax1.tick_params(axis='y', labelsize=15)
plt.suptitle("Best Customer Based on RFM Parameters (customer_id)", fontsize=20)

# By Frequency
fig2, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
sns.barplot(x="frequency", y="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), ax=ax2)
ax2.set_ylabel(None)
ax2.set_xlabel(None)
ax2.set_title("By Frequency", loc="center", fontsize=18)
ax2.tick_params(axis='y', labelsize=15)
plt.suptitle("Best Customer Based on RFM Parameters (customer_id)", fontsize=20)

# By Monetary
fig3, ax3 = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
sns.barplot(x="monetary", y="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), ax=ax3)
ax3.set_ylabel(None)
ax3.set_xlabel(None)
ax3.set_title("By Monetary", loc="center", fontsize=18)
ax3.tick_params(axis='y', labelsize=15)
plt.suptitle("Best Customer Based on RFM Parameters (customer_id)", fontsize=20)

# Menampilkan tiga grafik di tiga tab yang berbeda
st.subheader('RFM Analysis')

tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

with tab1:
    st.header("By Recency (days)")
    st.pyplot(fig1)
    st.write(
        """Customer dengan customer_id a4b417188addbc05b26b72d5e44837a1 
        merupakan customer yang paling terakhir
        melakukan transaksi."""
    )

with tab2:
    st.header("By Frequency")
    st.pyplot(fig2)
    st.write(
        """Ternyata setiap customer hanya melakukan satu kali pembelian."""
    )

with tab3:
    st.header("By Monetary")
    st.pyplot(fig3)
    st.write(
        """Customer dengan customer_id 1617b1357756262bfa56ab541c47bc16 
        merupakan customer yang paling banyak
        menghabiskan uang untuk pembelian yaitu lebih dari 10000."""
    )

st.caption('Copyright (c) Annisa P. S. 2024')
    