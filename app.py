import streamlit as st

# 1. Konfigurasi Halaman agar tampil penuh (Wide Mode)
st.set_page_config(page_title="MTL Production Dashboard", layout="wide")

# 2. Link Web Page (PubHTML) kamu
# Saya tambahkan parameter &widget=false&chrome=false agar tampilan bersih tanpa menu Google
HTML_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsBRvf_sGqgV0e3tbSxxakUfwicBDolwJnG8myK_Ss_SjLG4i0ISy8rjBAR-C3l_aVFRfyIwR9WoDY/pubhtml?gid=1320809524&single=true&widget=false&chrome=false&rm=minimal"

# 3. CSS sakti untuk menghilangkan header Streamlit dan membuat background hitam
st.markdown("""
    <style>
    /* Menghilangkan padding aplikasi */
    .block-container { padding: 0rem; }
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    
    /* Menghilangkan header dan footer bawaan Streamlit */
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Membuat IFrame (jendela spreadsheet) memenuhi layar */
    iframe {
        width: 100%;
        height: 100vh;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Menampilkan Dashboard Asli
st.markdown(f'<iframe src="{HTML_URL}"></iframe>', unsafe_allow_html=True)

# Tambahkan info di sidebar jika perlu
with st.sidebar:
    st.title("MTL Monitoring")
    st.info("Dashboard ini sinkron otomatis dengan Google Sheets.")
    if st.button('🔄 Refresh Dashboard'):
        st.rerun()
