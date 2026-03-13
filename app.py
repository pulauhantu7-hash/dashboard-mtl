import streamlit as st
import pandas as pd

# 1. Konfigurasi Tampilan Modern
st.set_page_config(page_title="MTL Hauling Dashboard", layout="wide")

# Link data kamu (Link CSV Google Sheets)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsBRvf_sGqgV0e3tbSxxakUfwicBDolwJnG8myK_Ss_SjLG4i0ISy8rjBAR-C3l_aVFRfyIwR9WoDY/pub?gid=528195320&single=true&output=csv"

@st.cache_data(ttl=10)
def fetch_data():
    df = pd.read_csv(CSV_URL)
    # Bersihkan nama kolom dari spasi dan jadikan huruf besar
    df.columns = [str(c).strip().upper() for c in df.columns]
    # Buang kolom yang tidak perlu (Unnamed)
    df = df.loc[:, ~df.columns.str.contains('^UNNAMED')]
    return df

# CSS untuk Dashboard Gelap
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0e1117; color: white; }
    .metric-card { background-color: #1c2529; padding: 20px; border-radius: 10px; border-bottom: 4px solid #00f2fe; text-align: center; }
    .val { font-size: 32px; font-weight: bold; color: white; }
    .lbl { color: #80cbc4; font-size: 14px; font-weight: bold; }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

try:
    df = fetch_data()
    st.title("🚜 MTL HAULING MONITORING")
    
    # Hitung angka utama
    df["TONASE"] = pd.to_numeric(df["TONASE"], errors='coerce').fillna(0)
    df["RITASE"] = pd.to_numeric(df["RITASE"], errors='coerce').fillna(0)
    
    total_tonase = df["TONASE"].sum()
    total_ritase = df["RITASE"].sum()
    unit_running = len(df[df["STATUS"].str.contains("RUNNING", na=False, case=False)])

    # Layout Kotak Metrik
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="lbl">TOTAL TONASE</div><div class="val">{total_tonase:,.0f}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="lbl">TOTAL RITASE</div><div class="val">{total_ritase:,.0f}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="lbl">UNIT RUNNING</div><div class="val">{unit_running}</div></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("📋 Detail Aktivitas")
    
    # Tabel dengan highlight untuk Breakdown
    def highlight_status(row):
        return ['background-color: #442727' if 'BREAKDOWN' in str(row['STATUS']).upper() else '' for _ in row]

    st.dataframe(df.style.apply(highlight_status, axis=1), use_container_width=True, height=500)

except Exception as e:
    st.error(f"Gagal memuat data: {e}")
