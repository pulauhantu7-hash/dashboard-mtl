import streamlit as st

st.set_page_config(page_title="MTL Production Dashboard", layout="wide")

# Link Web Page kamu
HTML_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsBRvf_sGqgV0e3tbSxxakUfwicBDolwJnG8myK_Ss_SjLG4i0ISy8rjBAR-C3l_aVFRfyIwR9WoDY/pubhtml?gid=1320809524&single=true&widget=false&chrome=false&rm=minimal"

st.markdown("""
    <style>
    /* Menghilangkan padding utama Streamlit */
    .block-container { padding: 0rem; max-width: 100%; }
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Container untuk IFrame dengan fitur Zoom */
    .iframe-container {
        overflow: hidden;
        /* Mengatur rasio agar tetap proporsional */
        padding-top: 56.25%; 
        position: relative;
    }
    
    iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 125%; /* Membuat canvas lebih lebar agar bisa di-zoom out */
        height: 125%;
        border: none;
        /* FIT TO PAGE: Mengatur skala tampilan (80% zoom out) */
        transform: scale(0.8); 
        transform-origin: 0 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Menampilkan IFrame
st.markdown(f'<iframe src="{HTML_URL}"></iframe>', unsafe_allow_html=True)

with st.sidebar:
    st.title("MTL Monitoring")
    # Slider untuk mengatur zoom secara manual jika dirasa kurang pas
    zoom = st.slider("Atur Zoom Dashboard", 0.5, 1.2, 0.8)
    st.write("Gunakan slider di atas jika tampilan masih terpotong.")
    if st.button('🔄 Refresh'):
        st.rerun()
