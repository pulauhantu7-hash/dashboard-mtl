import streamlit as st

# 1. Konfigurasi Halaman - Menghilangkan padding bawaan
st.set_page_config(page_title="MTL Production Dashboard", layout="wide", initial_sidebar_state="collapsed")

HTML_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsBRvf_sGqgV0e3tbSxxakUfwicBDolwJnG8myK_Ss_SjLG4i0ISy8rjBAR-C3l_aVFRfyIwR9WoDY/pubhtml?gid=1320809524&single=true&widget=false&chrome=false&rm=minimal"

# 2. CSS Khusus untuk membuang warna hitam di bawah dan Fit ke layar
st.markdown("""
    <style>
    /* Membuang semua margin dan padding dari Streamlit */
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    
    /* Menghilangkan header dan footer */
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Mengunci IFrame agar tingginya pas dengan layar browser (100vh) */
    iframe {
        width: 100%;
        height: 100vh; /* Menggunakan 100% tinggi layar */
        border: none;
        display: block;
    }

    /* Menghilangkan scrollbar pada body agar tidak ada warna hitam tersisa */
    [data-testid="stAppViewContainer"] {
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Menampilkan Dashboard
st.markdown(f'<iframe src="{HTML_URL}"></iframe>', unsafe_allow_html=True)
