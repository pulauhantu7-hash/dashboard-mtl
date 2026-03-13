import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MTL Production Dashboard", layout="wide")

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsBRvf_sGqgV0e3tbSxxakUfwicBDolwJnG8myK_Ss_SjLG4i0ISy8rjBAR-C3l_aVFRfyIwR9WoDY/pub?gid=1320809524&single=true&output=csv"

@st.cache_data(ttl=10)
def fetch_data():
    df = pd.read_csv(CSV_URL, header=None)
    # Bersihkan data dari spasi
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    return df

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: white; }
    .metric-box { background-color: #111; padding: 15px; border-radius: 8px; border: 1px solid #444; text-align: center; border-left: 5px solid #fbff00; }
    .lbl { color: #8bc34a; font-size: 13px; font-weight: bold; }
    .val { font-size: 24px; font-weight: bold; color: #ffffff; }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

try:
    df = fetch_data()
    st.markdown("<h1 style='text-align: center; color: #fbff00;'>🚜 HAULING PRODUCTION MONITORING</h1>", unsafe_allow_html=True)

    # FUNGSI PENCARI DATA OTOMATIS
    def get_val(keyword, offset_col=1):
        try:
            # Cari baris dan kolom di mana kata kunci berada
            mask = df.apply(lambda s: s.astype(str).str.contains(keyword, na=False, case=False))
            pos = mask.stack()[mask.stack()].index.tolist()[0]
            # Ambil nilai di sebelahnya (offset_col)
            res = df.iloc[pos[0], pos[1] + offset_col]
            return res if pd.notna(res) else "0"
        except:
            return "0"

    col_main, col_side = st.columns([3, 1])

    with col_side:
        st.subheader("📊 SUMMARY")
        # Dia bakal nyari tulisan ini di excel kamu dan ambil angka di kanannya
        p_rit = get_val("PLAN RITASE")
        a_rit = get_val("ACT. RITASE")
        p_ton = get_val("PLAN TONASE")
        a_ton = get_val("ACT. TONASE")
        
        def draw_card(l, v, c="#fff"):
            st.markdown(f"<div class='metric-box'><div class='lbl'>{l}</div><div class='val' style='color:{c}'>{v}</div></div>", unsafe_allow_html=True)
        
        draw_card("PLAN RITASE", p_rit)
        draw_card("ACT. RITASE", a_rit, "#fbff00")
        draw_card("PLAN TONASE", p_ton)
        draw_card("ACT. TONASE", a_ton, "#00f2fe")

    with col_main:
        st.subheader("📈 TREND RITASE")
        # Cari baris "TOTAL RITASE/HOUR"
        try:
            mask_trend = df.apply(lambda s: s.astype(str).str.contains("TOTAL RITASE/HOUR", na=False))
            row_idx = mask_trend.stack()[mask_trend.stack()].index.tolist()[0][0]
            # Ambil 10 jam pertama (kolom C sampai L)
            trend_vals = pd.to_numeric(df.iloc[row_idx, 2:14], errors='coerce').fillna(0).tolist()
            hours = ['06','07','08','09','10','11','12','13','14','15','16','17']
            
            fig = px.bar(x=hours, y=trend_vals, text=trend_vals, color_discrete_sequence=['#fbff00'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=300)
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.warning("Trend belum sinkron")

        st.subheader("🛠️ MECHANICAL PROBLEM")
        # Ambil tabel di bawah tulisan NO UNIT
        try:
            mask_unit = df.apply(lambda s: s.astype(str).str.fullmatch("NO UNIT", na=False))
            pos_u = mask_unit.stack()[mask_unit.stack()].index.tolist()[0]
            prob_df = df.iloc[pos_u[0]+1 : pos_u[0]+7, pos_u[1] : pos_u[1]+5]
            prob_df.columns = ["UNIT", "PROBLEM", "START", "FINISH", "TIME"]
            st.table(prob_df.fillna("-"))
        except:
            st.info("Problem log kosong")

except Exception as e:
    st.error(f"Syncing... {e}")

if st.sidebar.button('🔄 REFRESH'):
    st.rerun()
