import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Gahar
st.set_page_config(page_title="MTL Production Dashboard", layout="wide")

# Link CSV Dashboard kamu
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsBRvf_sGqgV0e3tbSxxakUfwicBDolwJnG8myK_Ss_SjLG4i0ISy8rjBAR-C3l_aVFRfyIwR9WoDY/pub?gid=1320809524&single=true&output=csv"

@st.cache_data(ttl=10)
def fetch_data():
    # Membaca data tanpa header agar koordinat iloc akurat
    df = pd.read_csv(CSV_URL, header=None)
    return df

# CSS UI Hitam-Kuning MTL
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: white; }
    .metric-box { 
        background-color: #111; 
        padding: 15px; 
        border: 1px solid #444; 
        border-radius: 8px;
        text-align: center;
        margin-bottom: 10px;
        border-left: 5px solid #fbff00;
    }
    .lbl { color: #8bc34a; font-size: 13px; font-weight: bold; }
    .val { font-size: 26px; font-weight: bold; color: #ffffff; }
    header {visibility: hidden;}
    .stTable { background-color: #111; color: white; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

try:
    df = fetch_data()
    st.markdown("<h1 style='text-align: center; color: #fbff00;'>🚜 HAULING PRODUCTION MONITORING</h1>", unsafe_allow_html=True)
    st.write("---")

    col_main, col_side = st.columns([3, 1])

    with col_side:
        st.markdown("<h3 style='color: #8bc34a;'>PRODUCTION SUMMARY</h3>", unsafe_allow_html=True)
        
        # --- KOORDINAT BERDASARKAN FILE EXCEL ASLI ---
        # Plan DT: Baris 4, Kolom AA(26) | Act DT: Baris 5, Kolom AA(26)
        # Plan Rit: Baris 6, Kolom AA(26) | Act Rit: Baris 7, Kolom AA(26)
        
        def draw_card(label, value, color="#ffffff"):
            st.markdown(f"<div class='metric-box'><div class='lbl'>{label}</div><div class='val' style='color:{color}'>{value}</div></div>", unsafe_allow_html=True)

        plan_dt  = df.iloc[3, 26] if len(df) > 3 else "0"
        act_dt   = df.iloc[4, 26] if len(df) > 4 else "0"
        plan_rit = df.iloc[6, 26] if len(df) > 6 else "0"
        act_rit  = df.iloc[7, 26] if len(df) > 7 else "0"
        plan_ton = df.iloc[8, 26] if len(df) > 8 else "0"
        act_ton  = df.iloc[9, 26] if len(df) > 9 else "0"

        draw_card("PLAN DT", plan_dt)
        draw_card("ACT. DT", act_dt)
        draw_card("PLAN RITASE", plan_rit)
        draw_card("ACT. RITASE", act_rit, "#fbff00")
        draw_card("ACT. TONASE", act_ton, "#00f2fe")

    with col_main:
        # --- GRAFIK TREND RITASE/HOUR ---
        st.markdown("<h3 style='color: #fbff00;'>📈 TREND RITASE PER HOUR</h3>", unsafe_allow_html=True)
        
        # Mengambil data ritase per jam dari Baris 90 (Total Ritase/Hour)
        # Sesuai file kamu: Jam 06-07 ada di kolom C(2) sampai V(21)
        hours = ['06-07','07-08','08-09','09-10','10-11','11-12','12-13','13-14','14-15','15-16','16-17','17-18','18-19','19-20']
        values = df.iloc[89, 2:16].fillna(0).tolist() # Mengambil Baris Total Ritase/Hour
        
        trend_data = pd.DataFrame({'Jam': hours, 'Ritase': values})
        trend_data['Ritase'] = pd.to_numeric(trend_data['Ritase'], errors='coerce').fillna(0)

        fig = px.bar(trend_data, x='Jam', y='Ritase', text='Ritase', color_discrete_sequence=['#fbff00'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=350)
        st.plotly_chart(fig, use_container_width=True)

        # --- MECHANICAL PROBLEM ---
        st.markdown("<h3 style='color: #ff4b4b;'>🛠️ MECHANICAL PROBLEM</h3>", unsafe_allow_html=True)
        # Tabel merah di tengah: Baris 19-26, Kolom M(12) sampai Q(16)
        prob_table = df.iloc[18:28, 12:17].copy()
        prob_table.columns = ["NO UNIT", "PROBLEM", "START", "FINISH", "TIME"]
        st.table(prob_table.fillna("-"))

except Exception as e:
    st.error(f"Data sedang sinkronisasi... ({e})")

# Auto-refresh sederhana
if st.sidebar.button('🔄 UPDATE DATA TERBARU'):
    st.rerun()
