import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman (Dark Mode)
st.set_page_config(page_title="MTL Production Monitoring", layout="wide")

# Link CSV khusus sheet DASHBOARD yang baru kamu buat
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsBRvf_sGqgV0e3tbSxxakUfwicBDolwJnG8myK_Ss_SjLG4i0ISy8rjBAR-C3l_aVFRfyIwR9WoDY/pub?gid=1320809524&single=true&output=csv"

@st.cache_data(ttl=15)
def fetch_data():
    # Membaca data tanpa header karena struktur dashboard Excel banyak sel gabungan
    df = pd.read_csv(CSV_URL, header=None)
    return df

# Styling CSS agar tampilan gahar (Hitam & Hijau/Kuning ala Tambang)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: white; }
    .metric-box { 
        background-color: #1c2529; 
        padding: 15px; 
        border: 1px solid #444; 
        border-radius: 8px;
        text-align: center;
        margin-bottom: 10px;
    }
    .lbl { color: #8bc34a; font-size: 14px; font-weight: bold; text-transform: uppercase; }
    .val { font-size: 28px; font-weight: bold; color: #ffffff; }
    header {visibility: hidden;}
    .stTable { background-color: #1c2529; color: white; }
    </style>
    """, unsafe_allow_html=True)

try:
    df = fetch_data()
    
    st.markdown("<h1 style='text-align: center; color: #fbff00;'>🚜 HAULING MONITORING SYSTEM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>PT MEGA TATA LESTARI</p>", unsafe_allow_html=True)
    st.write("---")

    # Layout: Kiri (Grafik & Tabel), Kanan (Summary)
    col_main, col_side = st.columns([3, 1])

    with col_side:
        st.markdown("<h3 style='color: #8bc34a;'>PRODUCTION SUMMARY</h3>", unsafe_allow_html=True)
        
        # Mengambil angka dari sel spesifik di spreadsheet dashboard kamu
        # Angka di iloc[baris, kolom] perlu disesuaikan jika posisi sel berubah
        def draw_card(label, value, color="#ffffff"):
            st.markdown(f"""
                <div class='metric-box'>
                    <div class='lbl'>{label}</div>
                    <div class='val' style='color:{color}'>{value}</div>
                </div>
            """, unsafe_allow_html=True)

        # Mengambil data Plan & Actual (Contoh koordinat berdasarkan gambar sebelumnya)
        try:
            plan_rit = df.iloc[4, 25] # Sel Plan Ritase
            act_rit = df.iloc[5, 25]  # Sel Actual Ritase
            ach_rit = df.iloc[6, 25]  # Sel Achievement Ritase
            
            draw_card("PLAN RITASE", plan_rit)
            draw_card("ACTUAL RITASE", act_rit)
            draw_card("ACHIEVEMENT", ach_rit, "#00f2fe")
            
            st.write("")
            # Tambahan untuk Tonase
            draw_card("ACTUAL TONASE", df.iloc[5, 27] if len(df.columns) > 27 else "0")
        except:
            st.warning("Menampilkan data default (Pastikan koordinat sel benar)")
            draw_card("PLAN RITASE", "50")
            draw_card("ACTUAL RITASE", "40")

    with col_main:
        # 1. Grafik Trend Ritase/Hour
        st.markdown("<h3 style='color: #fbff00;'>📈 TREND RITASE PER HOUR</h3>", unsafe_allow_html=True)
        
        # Membuat data trend (bisa diambil dari range sel di sheet)
        # Contoh data dummy agar grafik muncul:
        trend_df = pd.DataFrame({
            'Jam': ['07-08', '08-09', '09-10', '10-11', '11-12'],
            'Rit': [4, 18, 17, 1, 0]
        })
        
        fig = px.bar(trend_df, x='Jam', y='Rit', text='Rit', color_discrete_sequence=['#fbff00'])
        fig.update_traces(textposition='outside')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color="white", 
            height=300,
            margin=dict(l=0,r=0,t=20,b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

        # 2. Tabel Mechanical Problem (Bagian Bawah)
        st.write("")
        st.markdown("<h3 style='color: #ff4b4b;'>🛠️ MECHANICAL PROBLEM</h3>", unsafe_allow_html=True)
        # Mengambil potongan tabel dari koordinat baris 18-25, kolom 12-17
        try:
            problem_data = df.iloc[18:25, 12:17]
            st.table(problem_data)
        except:
            st.info("Data mechanical problem belum terisi di spreadsheet.")

except Exception as e:
    st.error(f"Koneksi Gagal. Silakan cek link CSV atau Publish to Web Anda. Error: {e}")

# Tombol Refresh Manual
if st.sidebar.button('🔄 REFRESH DATA'):
    st.rerun()
