"""
Gider ve Gelir Listeleme Sayfasi.
"""

import sys
from pathlib import Path
from datetime import date, timedelta
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from src.db.database import get_db
from src.db.crud import (
    kategori_listele,
    musteri_listele,
    gider_listele, gider_sil,
    gelir_listele,
)


st.set_page_config(
    page_title="Liste - YapayMusavir",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Liste ve Raporlar")
st.caption("Tum gider ve gelirleri goruntule, filtrele, dışa aktar")

st.divider()


def df_to_excel(df: pd.DataFrame, sheet_name: str = "Sheet1") -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()


def format_para(deger):
    try:
        return f"{float(deger):,.2f} TL"
    except (TypeError, ValueError):
        return ""


tab1, tab2 = st.tabs(["📥 Giderler", "📤 Gelirler"])


# ============================================================================
# TAB 1: GIDERLER
# ============================================================================

with tab1:
    st.subheader("Gider Listesi")
    
    # Filtre alanlari icin kategori cek
    db = get_db()
    try:
        kategoriler_gider = kategori_listele(db, tip="gider")
        kategori_listesi_g = [(k.id, k.ad) for k in kategoriler_gider]
    finally:
        db.close()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        baslangic_g = st.date_input(
            "Baslangic Tarihi",
            value=date.today() - timedelta(days=30),
            key="g_baslangic"
        )
    
    with col2:
        bitis_g = st.date_input(
            "Bitis Tarihi",
            value=date.today(),
            key="g_bitis"
        )
    
    with col3:
        kategori_secim_g = st.selectbox(
            "Kategori",
            options=["Tumu"] + [ad for _, ad in kategori_listesi_g],
            key="g_kategori"
        )
    
    # Verileri cek VE DataFrame'i SESSION ICINDE olustur
    db = get_db()
    try:
        kategori_id_filter = None
        if kategori_secim_g != "Tumu":
            for kid, ad in kategori_listesi_g:
                if ad == kategori_secim_g:
                    kategori_id_filter = kid
                    break
        
        giderler = gider_listele(
            db,
            baslangic_tarihi=baslangic_g,
            bitis_tarihi=bitis_g,
            kategori_id=kategori_id_filter
        )
        
        # Ozetler
        toplam_kdv_haric = sum(float(g.tutar) for g in giderler)
        toplam_kdv = sum(float(g.kdv_tutari) for g in giderler)
        toplam_brut = sum(float(g.toplam_tutar) for g in giderler)
        kayit_sayisi = len(giderler)
        
        # DataFrame - SESSION HENUZ ACIK!
        df_data_g = []
        for g in giderler:
            df_data_g.append({
                "ID": g.id,
                "Tarih": g.tarih,
                "Satici": g.satici,
                "Kategori": g.kategori.ad if g.kategori else "",
                "Tutar (Net)": format_para(g.tutar),
                "KDV %": f"%{float(g.kdv_orani):.0f}",
                "KDV Tutari": format_para(g.kdv_tutari),
                "Toplam": format_para(g.toplam_tutar),
                "Aciklama": g.aciklama or "",
                "Odeme": g.odeme_yontemi or "",
            })
    finally:
        db.close()
    
    # Artik session kapali ama DataFrame hazir, sorun yok
    
    if df_data_g:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Kayit Sayisi", kayit_sayisi)
        col2.metric("Net Toplam", format_para(toplam_kdv_haric))
        col3.metric("KDV Toplam", format_para(toplam_kdv))
        col4.metric("Brut Toplam", format_para(toplam_brut))
        
        st.divider()
        
        df_giderler = pd.DataFrame(df_data_g)
        st.dataframe(df_giderler, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            excel_bytes = df_to_excel(df_giderler, "Giderler")
            st.download_button(
                label="📥 Excel Olarak Indir",
                data=excel_bytes,
                file_name=f"giderler_{date.today().isoformat()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_giderler"
            )
        
        st.divider()
        
        with st.expander("🗑️ Gider Sil"):
            silinecek_id = st.number_input(
                "Silmek istediginiz gider ID'si:",
                min_value=1,
                step=1,
                key="g_sil_id"
            )
            
            if st.button("Sil", type="secondary", key="g_sil_btn"):
                db = get_db()
                try:
                    basarili = gider_sil(db, int(silinecek_id))
                    if basarili:
                        st.success(f"✅ Gider silindi (ID: {silinecek_id})")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"❌ ID {silinecek_id} bulunamadi")
                finally:
                    db.close()
    else:
        st.info("Bu kriterler icin gider bulunamadi. Filtreleri degistirin veya yeni gider ekleyin.")


# ============================================================================
# TAB 2: GELIRLER
# ============================================================================

with tab2:
    st.subheader("Gelir Listesi")
    
    db = get_db()
    try:
        musteriler = musteri_listele(db)
        musteri_listesi = [(m.id, m.ad) for m in musteriler]
    finally:
        db.close()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        baslangic_gl = st.date_input(
            "Baslangic Tarihi",
            value=date.today() - timedelta(days=30),
            key="gl_baslangic"
        )
    
    with col2:
        bitis_gl = st.date_input(
            "Bitis Tarihi",
            value=date.today(),
            key="gl_bitis"
        )
    
    with col3:
        musteri_secim_gl = st.selectbox(
            "Musteri",
            options=["Tumu"] + [ad for _, ad in musteri_listesi],
            key="gl_musteri"
        )
    
    with col4:
        tahsilat_filtre = st.selectbox(
            "Tahsilat Durumu",
            options=["Tumu", "Tahsil Edildi", "Beklemede"],
            key="gl_tahsilat"
        )
    
    db = get_db()
    try:
        musteri_id_filter = None
        if musteri_secim_gl != "Tumu":
            for mid, ad in musteri_listesi:
                if ad == musteri_secim_gl:
                    musteri_id_filter = mid
                    break
        
        odendi_filter = None
        if tahsilat_filtre == "Tahsil Edildi":
            odendi_filter = True
        elif tahsilat_filtre == "Beklemede":
            odendi_filter = False
        
        gelirler = gelir_listele(
            db,
            baslangic_tarihi=baslangic_gl,
            bitis_tarihi=bitis_gl,
            musteri_id=musteri_id_filter,
            odendi=odendi_filter
        )
        
        toplam_brut_gl = sum(float(g.toplam_tutar) for g in gelirler)
        toplam_stopaj = sum(float(g.stopaj_tutari) for g in gelirler)
        toplam_net = sum(float(g.net_tahsilat) for g in gelirler)
        bekleyen = sum(float(g.net_tahsilat) for g in gelirler if not g.odendi)
        kayit_sayisi_gl = len(gelirler)
        
        df_data_gl = []
        for g in gelirler:
            df_data_gl.append({
                "ID": g.id,
                "Tarih": g.tarih,
                "Musteri": g.musteri.ad if g.musteri else "",
                "Kategori": g.kategori.ad if g.kategori else "",
                "Tutar (Net)": format_para(g.tutar),
                "KDV %": f"%{float(g.kdv_orani):.0f}",
                "Toplam": format_para(g.toplam_tutar),
                "Stopaj": format_para(g.stopaj_tutari),
                "Net Tahsilat": format_para(g.net_tahsilat),
                "Tahsilat": "✅ Alindi" if g.odendi else "⏳ Bekliyor",
                "Aciklama": g.aciklama or "",
            })
    finally:
        db.close()
    
    if df_data_gl:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Kayit Sayisi", kayit_sayisi_gl)
        col2.metric("Brut Toplam", format_para(toplam_brut_gl))
        col3.metric("Stopaj", format_para(toplam_stopaj))
        col4.metric(
            "Net Tahsilat", 
            format_para(toplam_net),
            delta=f"-{bekleyen:,.2f} TL bekliyor" if bekleyen > 0 else None,
            delta_color="inverse"
        )
        
        st.divider()
        
        df_gelirler = pd.DataFrame(df_data_gl)
        st.dataframe(df_gelirler, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            excel_bytes_gl = df_to_excel(df_gelirler, "Gelirler")
            st.download_button(
                label="📥 Excel Olarak Indir",
                data=excel_bytes_gl,
                file_name=f"gelirler_{date.today().isoformat()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_gelirler"
            )
    else:
        st.info("Bu kriterler icin gelir bulunamadi. Filtreleri degistirin veya yeni gelir ekleyin.")


with st.sidebar:
    st.info(
        "💡 **Filtreler** verileri daraltir.  \n"
        "📥 **Excel export** ile muhasebecinize gonderebilirsiniz.  \n"
        "🗑️ **Silme** sadece yanlis girisleri duzeltmek icindir."
    )
