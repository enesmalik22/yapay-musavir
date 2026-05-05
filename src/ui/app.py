"""
YapayMusavir - Streamlit UI
"""

import sys
from pathlib import Path
from decimal import Decimal

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.db.database import get_db
from src.db.crud import (
    kategori_listele,
    musteri_listele,
    gider_listele,
    gelir_listele,
)


st.set_page_config(
    page_title="YapayMusavir",
    page_icon="📊",
    layout="wide",
)


def format_para(tutar):
    if tutar is None:
        return "0,00 TL"
    return f"{float(tutar):,.2f} TL"


@st.cache_data(ttl=60)
def ozet_verileri_getir():
    db = get_db()
    try:
        giderler = gider_listele(db)
        gelirler = gelir_listele(db)
        musteriler = musteri_listele(db)
        kategoriler = kategori_listele(db)

        toplam_gider = sum(Decimal(str(g.toplam_tutar)) for g in giderler)
        toplam_gelir = sum(Decimal(str(g.net_tahsilat)) for g in gelirler)
        net_kar = toplam_gelir - toplam_gider

        return {
            "gider_sayisi": len(giderler),
            "gelir_sayisi": len(gelirler),
            "musteri_sayisi": len(musteriler),
            "kategori_sayisi": len(kategoriler),
            "toplam_gider": toplam_gider,
            "toplam_gelir": toplam_gelir,
            "net_kar": net_kar,
        }
    finally:
        db.close()


st.title("📊 YapayMusavir")
st.caption("Freelancer'lar icin fatura ve vergi asistani")

st.divider()

ozet = ozet_verileri_getir()

st.subheader("Genel Ozet")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Toplam Gelir", format_para(ozet["toplam_gelir"]))

with col2:
    st.metric("Toplam Gider", format_para(ozet["toplam_gider"]))

with col3:
    st.metric("Net Kar", format_para(ozet["net_kar"]))

with col4:
    st.metric("Musteri Sayisi", ozet["musteri_sayisi"])

st.divider()

st.subheader("Kayit Sayilari")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Gider Kaydi", ozet["gider_sayisi"])

with col2:
    st.metric("Gelir Kaydi", ozet["gelir_sayisi"])

with col3:
    st.metric("Toplam Kategori", ozet["kategori_sayisi"])

st.divider()

with st.sidebar:
    st.markdown("---")
    
    if st.button("🔄 Verileri Yenile", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.caption("⚠️ Bu uygulama mali musavir yerine gecmez.")
st.info("Uygulamanin ilerleyen versiyonlarinda gider/gelir ekleme eklenecek.")
