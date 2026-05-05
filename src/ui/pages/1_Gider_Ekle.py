"""
Gider Ekleme Sayfasi.
"""

import sys
from pathlib import Path
from datetime import date

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.db.database import get_db
from src.db.crud import kategori_listele, gider_ekle


st.set_page_config(
    page_title="Gider Ekle - YapayMusavir",
    page_icon="📥",
    layout="wide"
)

st.title("📥 Gider Ekle")
st.caption("Yeni bir fatura/fis kaydi olustur")

st.divider()


def kategorileri_getir():
    db = get_db()
    try:
        return kategori_listele(db, tip="gider")
    finally:
        db.close()


def fatura_dosyasi_kaydet(uploaded_file) -> str:
    upload_dir = PROJECT_ROOT / "data" / "uploads" / "giderler"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = date.today().strftime("%Y%m%d")
    filename = f"{timestamp}_{uploaded_file.name}"
    filepath = upload_dir / filename
    
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return str(filepath)


kategoriler = kategorileri_getir()
kategori_dict = {k.ad: k for k in kategoriler}


with st.form("gider_ekle_form", clear_on_submit=True):
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Temel Bilgiler")
        
        tarih = st.date_input("Tarih", value=date.today())
        
        satici = st.text_input(
            "Satici",
            placeholder="Ornek: Migros, GitHub Inc, Turk Telekom"
        )
        
        satici_vkn = st.text_input(
            "Satici VKN/TCKN (opsiyonel)",
            max_chars=11
        )
        
        kategori_adi = st.selectbox(
            "Kategori",
            options=list(kategori_dict.keys()),
            help="KDV orani kategoriden otomatik gelir"
        )
        secilen_kategori = kategori_dict[kategori_adi]
    
    with col2:
        st.subheader("Tutar Bilgileri")
        
        tutar = st.number_input(
            "Tutar (KDV haric)",
            min_value=0.0,
            step=10.0,
            format="%.2f"
        )
        
        kdv_orani = st.number_input(
            "KDV Orani (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(secilen_kategori.kdv_orani),
            step=1.0,
            format="%.2f"
        )
        
        kdv_tutari = tutar * (kdv_orani / 100)
        toplam = tutar + kdv_tutari
        
        st.markdown("---")
        st.metric("KDV Tutari", f"{kdv_tutari:,.2f} TL")
        st.metric("Toplam Tutar", f"{toplam:,.2f} TL")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Detay")
        
        aciklama = st.text_area(
            "Aciklama (opsiyonel)",
            placeholder="Faturanin icerigi, notlar...",
            height=100
        )
    
    with col2:
        st.subheader("Diger")
        
        odeme_yontemi = st.radio(
            "Odeme Yontemi",
            options=["kredi karti", "havale", "nakit", "diger"],
            horizontal=True
        )
        
        fatura_dosyasi = st.file_uploader(
            "Fatura Dosyasi (Opsiyonel)",
            type=["pdf", "jpg", "jpeg", "png"]
        )
    
    st.divider()
    
    submitted = st.form_submit_button(
        "Gideri Kaydet",
        type="primary",
        use_container_width=True
    )


if submitted:
    if not satici.strip():
        st.error("Satici bos birakilamaz")
    elif tutar <= 0:
        st.error("Tutar 0'dan buyuk olmali")
    else:
        dosya_yolu = None
        if fatura_dosyasi is not None:
            try:
                dosya_yolu = fatura_dosyasi_kaydet(fatura_dosyasi)
            except Exception as e:
                st.warning(f"Dosya kaydedilemedi: {e}")
        
        db = get_db()
        try:
            yeni_gider = gider_ekle(
                db=db,
                tarih=tarih,
                satici=satici.strip(),
                kategori_id=secilen_kategori.id,
                tutar=tutar,
                kdv_orani=kdv_orani,
                satici_vkn=satici_vkn.strip() if satici_vkn else None,
                aciklama=aciklama.strip() if aciklama else None,
                odeme_yontemi=odeme_yontemi,
                fatura_no=None,
                fatura_dosyasi=dosya_yolu
            )
            
            st.success(f"Gider basariyla kaydedildi! (ID: {yeni_gider.id})")
            st.balloons()
            st.cache_data.clear()
            
        except Exception as e:
            st.error(f"Kayit hatasi: {e}")
        finally:
            db.close()


with st.sidebar:
    st.info(
        "Ipucu: Kategori sectiginde KDV orani otomatik gelir. "
        "Gerekirse degistirebilirsin."
    )
