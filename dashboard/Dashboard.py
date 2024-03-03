import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_day_df(df):
    df.rename(columns={
        "instant": "no"
    }, inplace=True)

    return df

def create_hour_df(df):
    df.rename(columns={
        "instant": "no"
    }, inplace=True)

    return df

def create_rfm_df(df):
    # Hitung recency, frequency, dan monetary dari DataFrame
    recency = df.groupby('season')['dteday'].max()
    recency = (df['dteday'].max() - recency).dt.days

    frequency = df.groupby('season').size()

    monetary = df.groupby('season')['cnt'].sum()

    # Gabungkan hasil-hasil perhitungan RFM menjadi sebuah DataFrame
    rfm_df = pd.DataFrame({'recency': recency, 'frequency': frequency, 'monetary': monetary})
    
    return rfm_df

def create_rfm2_df(df):
    # Menghitung recency, frequency, dan monetary dari DataFrame
    rfm2_df = df.groupby(by="mnth", as_index=False).agg({
        "dteday": "max",  # Mengambil tanggal order terakhir
        "registered": "sum",  # Jumlah total pendaftaran (registered) per bulan
        "cnt": "sum"  # Jumlah total pengeluaran (cnt) per bulan
    })
    
    # Mengubah nama kolom
    rfm2_df.columns = ["mnth", "max_order_date", "frequency", "monetary"]
    
    # Menghitung recency
    recent_date = df['dteday'].max()
    rfm2_df["recency"] = rfm2_df["max_order_date"].apply(lambda x: (recent_date - x).days)
    
    # Menghapus kolom yang tidak diperlukan
    rfm2_df.drop("max_order_date", axis=1, inplace=True)
    
    return rfm2_df

# Load cleaned data
merged_df = pd.read_csv("data/merged_df.csv")

datetime_columns = ["dteday"]
for column in datetime_columns:
    merged_df[column]= pd.to_datetime(merged_df[column])

# Filter data    
min_date = merged_df["dteday"].min()
max_date = merged_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/TifaniDea/Bangkit-Dicoding-Streamlit/main/gambar_2-removebg.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu Dataset',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = merged_df[(merged_df["dteday"] >= str(start_date)) & 
                (merged_df["dteday"] <= str(end_date))]

# Menyiapkan berbagai dataframe
day_df = create_day_df(main_df)
hour_df = create_hour_df(main_df)
rfm_df = create_rfm_df(main_df)
rfm2_df = create_rfm2_df(main_df)

# Product performance
# Visualisasi menggunakan Streamlit
st.header('Bike Sharing Dataset🚴🏻')

# Subheader untuk musim terbaik perentalan sepeda
st.subheader("Perentalan Sepeda pada Musim Terbaik 🏅")

# Jumlah perentalan pada musim gugur/season 3
jumlah_perentalan_season_3 = day_df[day_df['season'] == 3]['cnt'].sum()
st.write("Jumlah perentalan sepeda pada musim gugur/season 3 adalah:", jumlah_perentalan_season_3)

# Buat plot
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))

# Hitung jumlah perentalan per musim
jumlah_perentalan_season = day_df.groupby('season')['cnt'].sum()

# Buat bar plot 1
ax.bar(jumlah_perentalan_season.index, jumlah_perentalan_season.values)

# Atur label dan judul
ax.set_xlabel('Musim', fontsize=20)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=20)
ax.set_title('Jumlah perentalan sepeda per musim', loc="center", fontsize=30)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)

# Tampilkan plot menggunakan streamlit
st.pyplot(fig)

# Menampilkan pesan 
st.write("Dari bar chart di atas memberikan tampilan untuk membandingkan tiap semua musim dan hasil yang ditampilkan dominan pada musim gugur.")

# Visualisasi pie plot  1
st.subheader("Persentase Jumlah Perentalan Sepeda per Musim 🏅")

# Menghitung jumlah perentalan per musim
jumlah_perentalan_season = day_df.groupby('season')['cnt'].sum()

# Buat pie plot
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
plt.pie(jumlah_perentalan_season, labels=jumlah_perentalan_season.index, autopct='%1.1f%%', startangle=140)
plt.title('Persentase Jumlah perentalan sepeda per musim')
plt.axis('equal')

# Tampilkan plot menggunakan streamlit
st.pyplot(fig)

# Menampilkan pesan 
st.write("Dari pie chart yang ditampilkan memberikan persentase pada tiap musim dan hasilnya dominan pada musim gugur dengan persentase 32.2%.")

# Visualisasi line plot 1
st.subheader("Jumlah Perentalan Sepeda per Musim pada Line Chart 🏅")

# Buat plot line
fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(jumlah_perentalan_season.index, jumlah_perentalan_season.values, marker='o', linestyle='-')

# Menyeting label dan judul
plt.xlabel('Musim', fontsize=20)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=20)
plt.title('Jumlah perentalan sepeda per musim', fontsize=30)

# Menampilkan grid  
plt.grid(True)

# Tampilkan plot menggunakan streamlit
st.pyplot(fig)

# Menampilkan pesan 
st.write("Dari line chart diatas memberikan tampilan untuk membandingkan tiap semua musim dan hasil yang ditampilkan dominan pada musim gugur atau season 3.")

# Visualisasi histogram RFM Analisis menggunakan Streamlit  1
st.subheader("RFM Analysis Based on Seasons 🏅")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)
# Buat subplots
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))

# Warna untuk histogram
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

# Plot histogram untuk recency
sns.barplot(y=rfm_df['recency'], x=rfm_df.index, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis='x', labelsize=15)

# Plot histogram untuk frequency
sns.barplot(y=rfm_df['frequency'], x=rfm_df.index, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)

# Plot histogram untuk monetary
sns.barplot(y=rfm_df['monetary'], x=rfm_df.index, palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)

# Tampilkan plot menggunakan streamlit
st.pyplot(fig)

# Menampilkan Pesan 
st.write("Dari bar plot yang ditampilkan diatas terdapat subplot Recency. subplot Frequency, dan subplot Monetary. Subplot Recency dihitung dengan mengelompokkan data berdasarkan musim dan kemudian mencari tanggal terakhir setiap grup musim. Subplot Frequency dihitung dengan menghitung jumlah entri data dalam setiap grup musim. Subplot Monetary dihitung dengan menjumlahkan nilai dalam kolom 'cnt' (jumlah peminjaman sepeda) dalam setiap grup musim.")

# Visualisasi menggunakan Streamlit
st.header('Jumlah Registered')
st.subheader('Jumlah Pengguna Terdaftar per Bulan 🏅')

#jumlah pengguna terdaftar (registered) dalam sebulan
registered_per_month = day_df.groupby('mnth')['registered'].sum()
st.write("Jumlah pengguna terdaftar/registered perbulan : ", registered_per_month)

# Buat plot bar chart
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
registered_per_month = day_df.groupby('mnth')['registered'].sum()
ax.bar(registered_per_month.index, registered_per_month.values)

# Atur label dan judul
ax.set_xlabel('Bulan', fontsize=20)
ax.set_ylabel('Jumlah Pengguna Terdaftar', fontsize=20)
ax.set_title('Jumlah Pengguna Terdaftar per bulan 🏅', fontsize=30)
ax.tick_params(axis='both', labelsize=15)

# Tampilkan plot menggunakan streamlit
st.pyplot(fig)

# Menampilkan Pesan 
st.write("Dari bar chart diatas memberikan tampilan untuk membandingkan tiap bulan untuk pelanggan terdaftar dan hasil yang ditampilkan dominan pada bulan ke - 8.")

# Subheader untuk persentase jumlah pengguna terdaftar per bulan
st.subheader("Persentase Jumlah Pengguna Terdaftar per Bulan 🏅")

# Hitung jumlah pendaftaran terdaftar (registered) per bulan
registered_per_month = day_df.groupby('mnth')['registered'].sum()

# Buat pie plot
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(registered_per_month, labels=registered_per_month.index, autopct='%1.1f%%', startangle=140)
ax.set_title('Persentase Jumlah Pengguna Terdaftar per Bulan')

# Tampilkan plot menggunakan Streamlit
st.pyplot(fig)

# Menampilkan Pesan 
st.write("Pie chart yang ditampilkan memberikan persentase pada tiap bulan dan hasilnya dominan pada bulan ke - 8 dengan persentase 10.4%.")

# Tampilkan subjudul
st.subheader("Jumlah Pengguna Terdaftar per bulan 🏅")

# Buat plot line chart
fig, ax = plt.subplots(figsize=(12, 6))

# Data registered per bulan
registered_per_month = day_df.groupby('mnth')['registered'].sum()
plt.plot(registered_per_month.index, registered_per_month.values, marker='o', linestyle='-')

# Set label dan judul
plt.xlabel('Bulan')
plt.ylabel('Jumlah Pengguna Terdaftar')
plt.title('Jumlah Pengguna Terdaftar per bulan')

# Tampilkan grid
plt.grid(True)

# Tampilkan plot menggunakan Streamlit
st.pyplot(fig)

# Menampilkan Pesan
st.write("Dari line chart diatas memberikan tampilan untuk membandingkan tiap bulan dan hasil yang ditampilkan dominan pada bulan ke-8 dengan hasil 280000.")

# Menghitung RFM
latest_date = day_df['dteday'].max()
day_df['recency'] = (latest_date - day_df['dteday']).dt.days
registered_per_month = day_df.groupby('mnth')['registered'].sum().reset_index()
registered_per_month.columns = ['mnth', 'frequency']
monetary_per_month = day_df.groupby('mnth')['cnt'].sum().reset_index()
monetary_per_month.columns = ['mnth', 'monetary']
rfm_df = registered_per_month.merge(monetary_per_month, on='mnth')

# Visualisasi RFM menggunakan Streamlit
st.subheader("Best Customer Based on RFM Parameters (month) 🏅")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm2_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm2_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = format_currency(rfm2_df.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)

# Buat subplots
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

# Visualisasi Recency
sns.barplot(y="mnth", x="recency", data=day_df.groupby('mnth')['recency'].min().reset_index().sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=15)

# Visualisasi Frequency
sns.barplot(y="mnth", x="frequency", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

# Visualisasi Monetary
sns.barplot(y="mnth", x="monetary", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='y', labelsize=15)

# Tampilkan plot menggunakan streamlit
st.pyplot(fig)

# Menampilkan Pesan
st.write("Dari bar plot diatas terdapat subplot Recency, subplot Frequency, subplot Monetary. Subplot pertama menampilkan visualisasi Recency dengan menggunakan bar plot. Data yang digunakan adalah lima bulan dengan nilai Recency terendah, yang diurutkan berdasarkan nilai Recency secara menaik. Subplot kedua menampilkan visualisasi Frequency dengan menggunakan bar plot. Data yang digunakan adalah lima bulan dengan nilai Frequency tertinggi. Subplot ketiga menampilkan visualisasi Monetary dengan menggunakan bar plot. Data yang digunakan adalah lima bulan dengan nilai Monetary tertinggi.")
