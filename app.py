import streamlit as st
import pandas as pd

st.set_page_config(page_title="MTL Hauling Dashboard", layout="wide")

# Link CSV Google Sheets kamu
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsBRvf_sGqgV0e3tbSxxakUfwicBDolwJnG8myK_Ss_SjLG4i0ISy8rjBAR-C3l_aVFRfyIwR9WoDY/pub?gid=528195320&single=true&output=csv"

@st.cache_data(ttl=10)
def fetch_data():
    df = pd.read_csv(CSV_URL)
    # Bersihkan nama kolom: hapus spasi di awal/akhir dan jadikan HURUF BESAR
    df.columns = [str(c).strip().upper() for c in df.columns]
    return df

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

    # CARI KOLOM SECARA OTOMATIS (Biar ga error nama kolom)
    col_ton = [c for c in df.columns if 'TON' in c][0] if [c for c in df.columns if 'TON' in c] else None
    col_rit = [c for c in df.columns if 'RIT' in c][0] if [c for c in df.columns if 'RIT' in c] else None
    col_sts = [c for c in df.columns if 'STAT' in c][0] if [c for c in df.columns if 'STAT' in c] else None

    # Hitung Angka
    val_ton = pd.to_numeric(df[col_ton], errors='coerce').sum() if col_ton else 0
    val_rit = pd.to_numeric(df[col_rit], errors='coerce').sum() if col_rit else 0
    val_run = len(df[df[col_sts].str.contains("RUN", na=False, case=False)]) if col_sts else 0

    # Tampilkan Kartu Metrik
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="lbl">TOTAL TONASE</div><div class="val">{val_ton:,.0f}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="lbl">TOTAL RITASE</div><div class="val">{val_rit:,.0f}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="lbl">UNIT RUNNING</div><div class="val">{val_run}</div></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("📋 Detail Aktivitas")
    
    # Tabel
    st.dataframe(df, use_container_width=True, height=500)

except Exception as e:
    st.error(f"Error: {e}")
    st.write("Kolom yang terbaca di Excel kamu:", df.columns.tolist() if 'df' in locals() else "Data tidak terbaca")
