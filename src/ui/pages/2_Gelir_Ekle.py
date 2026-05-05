"""
Gelir Ekleme Sayfasi.
"""

import sys
from pathlib import Path
from datetime import date

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.db.database import get_db
from src.db.crud import (
    kategori_listele, 
    musteri_listele, musteri_ekle,
    gelir_ekle
)


st.set_page_config(
    page_title="Gelir Ekle - YapayMusavir",
    page_icon="📤",
    layout="wide"
)

st.title("📤 Gelir Ekle")
st.caption("Kestigin faturayi sisteme kaydet")

st.divider()


def kategorileri_getir():
    db = get_db()
    try:
        return kategori_listele(db, tip="gelir")
    finally:
        db.close()


def musterileri_getir():
    db = get_db()
    try:
        return musteri_listele(db)
    finally:
        db.close()


def fatura_dosyasi_kaydet(uploaded_file) -> str:
    upload_dir = PROJECT_ROOT / "data" / "uploads" / "gelirler"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = date.today().strftime("%Y%m%d")
    filename = f"{timestamp}_{uploaded_file.name}"
    filepath = upload_dir / filename
    
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return str(filepath)


# MUSTERI BOLUMU
st.subheader("👤 Musteri Secimi")

musteriler = musterileri_getir()

if not musteriler:
    st.warning("⚠️ Henuz musteri yok. Once asagidan yeni musteri ekleyin.")

with st.expander("➕ Yeni Musteri Ekle"):
    with st.form("yeni_musteri_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            yeni_musteri_ad = st.text_input("Musteri Adi *", key="yeni_m_ad")
            yeni_musteri_vkn = st.text_input("VKN/TCKN", key="yeni_m_vkn", max_chars=11)
            yeni_musteri_yurtdisi = st.checkbox("Yurtdisi musterisi", key="yeni_m_yd")
        with col2:
            yeni_musteri_email = st.text_input("E-posta", key="yeni_m_email")
            yeni_musteri_tel = st.text_input("Telefon", key="yeni_m_tel")
        
        musteri_ekle_btn = st.form_submit_button("💾 Musteri Ekle", type="primary")
        
        if musteri_ekle_btn:
            if not yeni_musteri_ad.strip():
                st.error("❌ Musteri adi bos olamaz")
            else:
                db = get_db()
                try:
                    yeni_m = musteri_ekle(
                        db=db,
                        ad=yeni_musteri_ad,
                        vkn_tckn=yeni_musteri_vkn or None,
                        email=yeni_musteri_email or None,
                        telefon=yeni_musteri_tel or None,
                        yurtdisi=yeni_musteri_yurtdisi
                    )
                    st.success(f"✅ Musteri eklendi: {yeni_m.ad}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hata: {e}")
                finally:
                    db.close()

st.divider()


# GELIR FORMU
if musteriler:
    st.subheader("📋 Fatura Bilgileri")
    
    kategoriler = kategorileri_getir()
    kategori_dict = {k.ad: k for k in kategoriler}
    musteri_dict = {f"{m.ad}{' (Yurtdisi)' if m.yurtdisi else ''}": m for m in musteriler}
    
    with st.form("gelir_ekle_form", clear_on_submit=True):
        
        col1, col2 = st.columns(2)
        
        with col1:
            tarih = st.date_input("Tarih *", value=date.today())
            
            musteri_secim = st.selectbox(
                "Musteri *",
                options=list(musteri_dict.keys())
            )
            secilen_musteri = musteri_dict[musteri_secim]
            
            kategori_adi = st.selectbox(
                "Kategori *",
                options=list(kategori_dict.keys()),
                help="KDV ve stopaj otomatik gelir"
            )
            secilen_kategori = kategori_dict[kategori_adi]
            
        with col2:
            st.markdown("**💰 Tutar Bilgileri**")
            
            tutar = st.number_input(
                "Tutar (KDV haric) *",
                min_value=0.0,
                step=100.0,
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
            
            stopaj_orani = st.number_input(
                "Stopaj Orani (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(secilen_kategori.stopaj_orani),
                step=1.0,
                format="%.2f"
            )
            
            kdv_tutari = tutar * (kdv_orani / 100)
            toplam = tutar + kdv_tutari
            stopaj_tutari = tutar * (stopaj_orani / 100)
            net_tahsilat = toplam - stopaj_tutari
            
            st.markdown("---")
            st.metric("KDV Tutari", f"{kdv_tutari:,.2f} TL")
            st.metric("Stopaj", f"-{stopaj_tutari:,.2f} TL")
            st.metric(
                "Net Tahsilat", 
                f"{net_tahsilat:,.2f} TL",
                delta=f"Toplam Fatura: {toplam:,.2f} TL"
            )
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            aciklama = st.text_area(
                "Aciklama",
                placeholder="Hizmetin detayi, proje adi...",
                height=100
            )
        
        with col2:
            odendi = st.checkbox("Tahsilat alindi mi?")
            
            if odendi:
                odeme_tarihi = st.date_input("Odeme Tarihi", value=date.today())
            else:
                odeme_tarihi = None
            
            fatura_dosyasi = st.file_uploader(
                "Fatura Dosyasi (Opsiyonel)",
                type=["pdf", "jpg", "jpeg", "png"]
            )
        
        st.divider()
        
        submitted = st.form_submit_button(
            "💾 Geliri Kaydet",
            type="primary",
            use_container_width=True
        )
    
    
    if submitted:
        if tutar <= 0:
            st.error("❌ Tutar 0'dan buyuk olmali")
        else:
            dosya_yolu = None
            if fatura_dosyasi is not None:
                try:
                    dosya_yolu = fatura_dosyasi_kaydet(fatura_dosyasi)
                except Exception as e:
                    st.warning(f"⚠️ Dosya kaydedilemedi: {e}")
            
            db = get_db()
            try:
                yeni_gelir = gelir_ekle(
                    db=db,
                    tarih=tarih,
                    musteri_id=secilen_musteri.id,
                    kategori_id=secilen_kategori.id,
                    tutar=tutar,
                    kdv_orani=kdv_orani,
                    stopaj_orani=stopaj_orani,
                    fatura_no=None,              
                    aciklama=aciklama or None,
                    odendi=odendi,
                    odeme_tarihi=odeme_tarihi
                )
                
                st.success(f"✅ Gelir basariyla kaydedildi! (ID: {yeni_gelir.id})")
                st.balloons()
                st.cache_data.clear()
                
            except Exception as e:
                st.error(f"❌ Kayit hatasi: {e}")
            finally:
                db.close()


with st.sidebar:
    st.info(
        "💡 **Yurtdisi musterisi** secersen ve **Yurtdisi kategorisi** kullanirsan "
        "KDV ve stopaj otomatik %0 olur (ihracat istisnasi)."
    )
