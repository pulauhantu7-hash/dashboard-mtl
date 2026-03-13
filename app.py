import streamlit as st
import pandas as pd

st.set_page_config(page_title="MTL Hauling Dashboard", layout="wide")

# Link CSV Google Sheets kamu
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsBRvf_sGqgV0e3tbSxxakUfwicBDolwJnG8myK_Ss_SjLG4i0ISy8rjBAR-C3l_aVFRfyIwR9WoDY/pub?gid=528195320&single=true&output=csv"

@st.cache_data(ttl=10)
def fetch_data():
    # Membaca data tanpa header dulu karena di web terbaca COLUMN 1, dst
    df = pd.read_csv(CSV_URL)
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

    # --- PEMETAAN KOLOM BERDASARKAN GAMBAR KAMU ---
    # Berdasarkan screenshot: 
    # COLUMN 1 = Tanggal/Jam, COLUMN 2 = Driver, COLUMN 3 = Unit, dst.
    # Kita asumsikan Ritase ada di kolom ke-4 dan Tonase di kolom ke-6 (sesuaikan nomornya)
    
    # Kita ambil kolom berdasarkan urutan (index)
    # df.iloc[:, 3] artinya kolom ke-4, df.iloc[:, 5] artinya kolom ke-6
    ritase_col = pd.to_numeric(df.iloc[:, 3], errors='coerce').fillna(0)
    tonase_col = pd.to_numeric(df.iloc[:, 5], errors='coerce').fillna(0)
    
    val_ton = tonase_col.sum()
    val_rit = ritase_col.sum()
    # Anggap unit running adalah total baris yang ada datanya
    val_run = len(df[df.iloc[:, 2].notna()]) 

    # --- TAMPILAN KOTAK METRIK ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="lbl">TOTAL TONASE</div><div class="val">{val_ton:,.0f}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="lbl">TOTAL RITASE</div><div class="val">{val_rit:,.0f}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="lbl">UNIT RUNNING</div><div class="val">{val_run}</div></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("📋 Detail Aktivitas")
    
    # Ganti nama kolom biar cantik di web
    df.columns = ['JAM', 'DRIVER', 'UNIT', 'RITASE', 'TUJUAN', 'TONASE', 'DUMPING', 'STATUS'][:len(df.columns)]
    
    st.dataframe(df, use_container_width=True, height=500)

except Exception as e:
    st.error(f"Sikit lagi Buts! Error: {e}")
