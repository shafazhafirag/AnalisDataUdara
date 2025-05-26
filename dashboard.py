import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Konfigurasi Streamlit ---
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
st.title("📊 Air Quality Analysis Dashboard (PM2.5)")
st.subheader("Shafa Zhafira Gunvany")

# --- Load Data ---
@st.cache_data
def load_data():
    def prep(file, station_name):
        df = pd.read_csv(file)
        df["station"] = station_name
        df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]])
        df.set_index("datetime", inplace=True)
        return df

    d1 = prep("data/PRSA_Data_Dingling_20130301-20170228.csv", "Dingling")
    d2 = prep("data/PRSA_Data_Dongsi_20130301-20170228.csv", "Dongsi")
    d3 = prep("data/PRSA_Data_Gucheng_20130301-20170228.csv", "Gucheng")
    d4 = prep("data/PRSA_Data_Dongsi_20130301-20170228.csv", "Tiantan")
    d5 = prep("data/PRSA_Data_Tiantan_20130301-20170228.csv", "Wanliu")
    return pd.concat([d1, d2, d3, d4, d5])

df = load_data()
df = df.dropna(subset=["PM2.5"])
df["year"] = df.index.year
df["month"] = df.index.month
df["season"] = df["month"] % 12 // 3 + 1

# --- Sidebar Filter ---
st.sidebar.header("Filter Data")
selected_station = st.sidebar.multiselect(
    "Pilih Stasiun", 
    options=sorted(df["station"].unique()), 
    default=sorted(df["station"].unique()) 
)

selected_year = st.sidebar.multiselect(
    "Pilih Tahun", 
    options=sorted(df["year"].unique()), 
    default=sorted(df["year"].unique())
)

# Filter DataFrame
filtered_df = df[
    (df["station"].isin(selected_station)) &
    (df["year"].isin(selected_year))
]

# --- Visualisasi 1: Rata-rata PM2.5 per Stasiun ---
st.subheader("📍 Rata-rata PM2.5 per Stasiun")
avg_pm25 = filtered_df.groupby("station")["PM2.5"].mean().sort_values()
fig1, ax1 = plt.subplots()
sns.barplot(x=avg_pm25.index, y=avg_pm25.values, ax=ax1)
ax1.set_ylabel("PM2.5 (µg/m³)")
st.pyplot(fig1)

# --- Visualisasi 2: Tren PM2.5 per Tahun ---
st.subheader("📈 Tren Rata-rata PM2.5 per Tahun")
yearly = filtered_df.groupby(["year", "station"])["PM2.5"].mean().reset_index()
fig2, ax2 = plt.subplots()
sns.lineplot(data=yearly, x="year", y="PM2.5", hue="station", marker="o", ax=ax2)
st.pyplot(fig2)

# --- Visualisasi 3: PM2.5 per Musim ---
st.subheader("❄️☀️ PM2.5 per Musim")
season_names = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
filtered_df["season_name"] = filtered_df["season"].map(season_names)
seasonal = filtered_df.groupby(["season_name", "station"])["PM2.5"].mean().reset_index()
fig3, ax3 = plt.subplots()
sns.barplot(data=seasonal, x="season_name", y="PM2.5", hue="station", ax=ax3)
st.pyplot(fig3)
