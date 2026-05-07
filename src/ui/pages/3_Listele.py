"""
Gider ve Gelir Listeleme Sayfasi (Dark Mode UI).
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
from src.db.models import Gelir


st.set_page_config(
    page_title="Liste - YapayMusavir",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CSS — app.py ile uyumlu dark mode
# ============================================================================
st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"] { display: none; }
[data-testid="stAppViewContainer"] { background: #0d1117; }

/* Topbar */
.ym-topbar {
    background: #111827;
    border-bottom: 0.5px solid rgba(255,255,255,0.08);
    padding: 0 28px;
    height: 48px;
    margin-top: -20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
}
.ym-logo { display: flex; align-items: center; gap: 9px; }
.ym-logo-icon {
    width: 30px; height: 30px;
    background: #4d8aff;
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
}
.ym-logo-name {
    font-size: 15px; font-weight: 600;
    color: #e8edf5; letter-spacing: -0.3px;
}
.ym-logo-dot { color: #4d8aff; }
.ym-topbar-right { display: flex; align-items: center; gap: 8px; }
.ym-notif {
    width: 28px; height: 28px;
    border-radius: 7px;
    background: rgba(255,255,255,0.06);
    border: 0.5px solid rgba(255,255,255,0.08);
    display: flex; align-items: center; justify-content: center;
    position: relative;
}
.ym-notif-dot {
    width: 6px; height: 6px;
    background: #4d8aff; border-radius: 50%;
    position: absolute; top: 4px; right: 4px;
    border: 1.5px solid #111827;
}
.ym-avatar {
    width: 28px; height: 28px;
    border-radius: 50%;
    background: #4d8aff;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 11px; font-weight: 600;
}

/* Nav */
[data-testid="stPageLink"] { width: 100% !important; }
[data-testid="stPageLink"] a {
    background: transparent !important;
    border: 0.5px solid transparent !important;
    border-radius: 10px !important;
    padding: 12px 18px !important;
    color: rgba(255,255,255,0.6) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    width: 100% !important;
}
[data-testid="stPageLink"] a:hover {
    background: rgba(77,138,255,0.10) !important;
    color: #ffffff !important;
    transform: translateY(-1px);
    border-color: rgba(77,138,255,0.25) !important;
    box-shadow: 0 4px 12px rgba(77,138,255,0.15);
}
[data-testid="stPageLink"] a[aria-current="page"] {
    background: rgba(77,138,255,0.18) !important;
    color: #6aaeff !important;
    border-color: rgba(77,138,255,0.35) !important;
    font-weight: 600 !important;
}
[data-testid="stPageLink"] a p {
    font-size: 14px !important;
    margin: 0 !important;
    font-weight: 500 !important;
}

/* Hero */
.ym-hero {
    background: linear-gradient(135deg, #0f1d3a 0%, #142347 100%);
    padding: 28px 32px;
    border-bottom: 0.5px solid rgba(255,255,255,0.06);
}
.ym-hero-title {
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
}
.ym-hero-title span { color: #6aaeff; }
.ym-hero-sub {
    font-size: 13px;
    color: rgba(255,255,255,0.42);
}

/* Body */
.ym-body { padding: 24px 32px 32px; }

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #1a2031;
    border: 0.5px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    color: rgba(255,255,255,0.55) !important;
    font-weight: 500 !important;
    padding: 10px 18px !important;
    transition: all 0.2s ease;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    background: rgba(255,255,255,0.04) !important;
    color: #e8edf5 !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: rgba(77,138,255,0.15) !important;
    color: #6aaeff !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    display: none !important;
}

/* Input alanlari */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="select"] > div {
    background: #0d1117 !important;
    border: 0.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #e8edf5 !important;
    transition: all 0.15s ease;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stDateInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #4d8aff !important;
    box-shadow: 0 0 0 2px rgba(77,138,255,0.15) !important;
}
label {
    color: rgba(255,255,255,0.7) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}

/* Metric kartlari */
[data-testid="stMetric"] {
    background: #1a2031;
    border: 0.5px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 16px 18px;
    transition: all 0.2s ease;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(77,138,255,0.25);
    transform: translateY(-1px);
}
[data-testid="stMetricLabel"] {
    color: rgba(255,255,255,0.5) !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 20px !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] {
    font-size: 11px !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background: #1a2031;
    border-radius: 12px;
    overflow: hidden;
    border: 0.5px solid rgba(255,255,255,0.07);
}

/* Filtre kart sarmalayicisi */
.ym-filter-card {
    background: #1a2031;
    border: 0.5px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 18px;
}

/* Section title */
.ym-section-title {
    font-size: 15px;
    font-weight: 600;
    color: #e8edf5;
    margin: 18px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Buttons (download, sil) */
.stDownloadButton button {
    background: linear-gradient(135deg, #4d8aff 0%, #2d5aaa 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: white !important;
    transition: all 0.2s ease;
}
.stDownloadButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(77,138,255,0.3) !important;
}

.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #e05c5c 0%, #b04545 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-weight: 600 !important;
}
.stButton button[kind="secondary"] {
    background: rgba(255,255,255,0.06) !important;
    border: 0.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: rgba(255,255,255,0.85) !important;
    font-weight: 500 !important;
}
.stButton button:hover {
    transform: translateY(-1px);
}

/* Expander */
[data-testid="stExpander"] {
    background: #1a2031 !important;
    border: 0.5px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    overflow: hidden;
    margin-top: 14px;
}
[data-testid="stExpander"] summary {
    padding: 14px 18px !important;
    color: #e8edf5 !important;
    font-weight: 500 !important;
}
[data-testid="stExpander"] summary:hover {
    background: rgba(255,255,255,0.03) !important;
}

/* Subheader */
[data-testid="stMarkdownContainer"] h3 {
    font-size: 16px !important;
    font-weight: 600 !important;
    color: rgba(255,255,255,0.9) !important;
    margin-bottom: 14px !important;
}

hr { border-color: rgba(255,255,255,0.06) !important; margin: 16px 0 !important; }

/* Info/Warning kutulari */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: 0.5px solid rgba(255,255,255,0.08) !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# TOPBAR
# ============================================================================
st.markdown("""
<div class="ym-topbar">
    <div class="ym-logo">
        <div class="ym-logo-icon">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <rect x="1" y="9" width="3" height="6" rx="1" fill="rgba(255,255,255,0.4)"/>
                <rect x="6" y="5" width="3" height="10" rx="1" fill="rgba(255,255,255,0.7)"/>
                <rect x="11" y="1" width="3" height="14" rx="1" fill="white"/>
            </svg>
        </div>
        <span class="ym-logo-name">Yapay<span class="ym-logo-dot">Musavir</span></span>
    </div>
    <div class="ym-topbar-right">
        <div class="ym-notif">
            <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M6.5 1a4 4 0 0 1 4 4v2.5l1 2H2l1-2V5a4 4 0 0 1 4-4ZM5 10.5a1.5 1.5 0 0 0 3 0" stroke="rgba(255,255,255,0.4)" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <div class="ym-notif-dot"></div>
        </div>
        <div class="ym-avatar">EM</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# NAV
# ============================================================================
nav_cols = st.columns(5)
with nav_cols[0]:
    st.page_link("app.py", label="Ana Sayfa", icon="🏠")
with nav_cols[1]:
    st.page_link("pages/1_Gider_Ekle.py", label="Gider Ekle", icon="💸")
with nav_cols[2]:
    st.page_link("pages/2_Gelir_Ekle.py", label="Gelir Ekle", icon="💰")
with nav_cols[3]:
    st.page_link("pages/3_Listele.py", label="Listele", icon="📋")
with nav_cols[4]:
    st.page_link("pages/4_AI_Asistan.py", label="AI Asistan", icon="🤖")


# ============================================================================
# HERO
# ============================================================================
st.markdown("""
<div class="ym-hero">
    <div class="ym-hero-title">
        Liste ve <span>Raporlar</span>
    </div>
    <div class="ym-hero-sub">
        Tum gider ve gelirleri goruntule, filtrele, Excel'e aktar.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# BODY
# ============================================================================
st.markdown('<div class="ym-body">', unsafe_allow_html=True)


def df_to_excel(df, sheet_name="Sheet1"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()


def format_para(deger):
    try:
        formatted = f"{float(deger):,.2f}"
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{formatted} TL"
    except (TypeError, ValueError):
        return ""


tab1, tab2 = st.tabs(["📥 Giderler", "📤 Gelirler"])


# ============================================================================
# TAB 1: GIDERLER
# ============================================================================

with tab1:
    st.markdown('<div class="ym-section-title">🔍 Filtreler</div>', unsafe_allow_html=True)

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

        toplam_kdv_haric = sum(float(g.tutar) for g in giderler)
        toplam_kdv = sum(float(g.kdv_tutari) for g in giderler)
        toplam_brut = sum(float(g.toplam_tutar) for g in giderler)
        kayit_sayisi = len(giderler)

        df_data_g = []
        for g in giderler:
            df_data_g.append({
                "ID": g.id,
                "Tarih": str(g.tarih),
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

    if df_data_g:
        st.markdown('<div class="ym-section-title" style="margin-top:24px;">📊 Ozet</div>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Kayit Sayisi", kayit_sayisi)
        col2.metric("Net Toplam", format_para(toplam_kdv_haric))
        col3.metric("KDV Toplam", format_para(toplam_kdv))
        col4.metric("Brut Toplam", format_para(toplam_brut))

        st.markdown('<div class="ym-section-title" style="margin-top:24px;">📋 Kayitlar</div>', unsafe_allow_html=True)

        df_giderler = pd.DataFrame(df_data_g)
        st.dataframe(df_giderler, use_container_width=True, hide_index=True)

        col1, col2 = st.columns([1, 3])
        with col1:
            excel_bytes = df_to_excel(df_giderler, "Giderler")
            st.download_button(
                label="📥 Excel Indir",
                data=excel_bytes,
                file_name=f"giderler_{date.today().isoformat()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_giderler"
            )

        with st.expander("🗑️ Gider Sil"):
            gider_secenekleri = {
                f"ID {row['ID']} | {row['Tarih']} | {row['Satici']} | {row['Toplam']}": row['ID']
                for row in df_data_g
            }

            secilen_label = st.selectbox(
                "Silinecek gideri secin:",
                options=list(gider_secenekleri.keys()),
                key="g_sil_secim"
            )

            secilen_id = gider_secenekleri[secilen_label]
            onay_key = f"onay_gider_{secilen_id}"

            col_sil, col_uyari = st.columns([1, 3])

            with col_sil:
                if st.session_state.get(onay_key, False):
                    if st.button("✅ Evet, Sil", type="primary", key=f"g_onay_{secilen_id}"):
                        db = get_db()
                        try:
                            basarili = gider_sil(db, int(secilen_id))
                            if basarili:
                                st.success(f"✅ Silindi (ID: {secilen_id})")
                                st.cache_data.clear()
                                st.session_state[onay_key] = False
                                st.rerun()
                            else:
                                st.error("❌ Silinemedi")
                        finally:
                            db.close()
                else:
                    if st.button("🗑️ Sil", type="secondary", key=f"g_sil_{secilen_id}"):
                        st.session_state[onay_key] = True
                        st.rerun()

            with col_uyari:
                if st.session_state.get(onay_key, False):
                    st.warning("⚠️ Bu islem geri alinamaz. Emin misiniz?")

    else:
        st.info("Bu kriterlere uyan gider bulunamadi.")


# ============================================================================
# TAB 2: GELIRLER
# ============================================================================

with tab2:
    st.markdown('<div class="ym-section-title">🔍 Filtreler</div>', unsafe_allow_html=True)

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
                "Tarih": str(g.tarih),
                "Musteri": g.musteri.ad if g.musteri else "",
                "Kategori": g.kategori.ad if g.kategori else "",
                "Tutar (Net)": format_para(g.tutar),
                "KDV %": f"%{float(g.kdv_orani):.0f}",
                "Toplam": format_para(g.toplam_tutar),
                "Net Tahsilat": format_para(g.net_tahsilat),
                "Tahsilat": "✅ Alindi" if g.odendi else "⏳ Bekliyor",
                "Aciklama": g.aciklama or "",
            })
    finally:
        db.close()

    if df_data_gl:
        st.markdown('<div class="ym-section-title" style="margin-top:24px;">📊 Ozet</div>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Kayit Sayisi", kayit_sayisi_gl)
        col2.metric("Brut Toplam", format_para(toplam_brut_gl))
        col4.metric(
            "Net Tahsilat",
            format_para(toplam_net),
            delta=f"-{bekleyen:,.2f} TL bekliyor" if bekleyen > 0 else None,
            delta_color="inverse"
        )

        st.markdown('<div class="ym-section-title" style="margin-top:24px;">📋 Kayitlar</div>', unsafe_allow_html=True)

        df_gelirler = pd.DataFrame(df_data_gl)
        st.dataframe(df_gelirler, use_container_width=True, hide_index=True)

        col1, col2 = st.columns([1, 3])
        with col1:
            excel_bytes_gl = df_to_excel(df_gelirler, "Gelirler")
            st.download_button(
                label="📥 Excel Indir",
                data=excel_bytes_gl,
                file_name=f"gelirler_{date.today().isoformat()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_gelirler"
            )

        with st.expander("🗑️ Gelir Sil"):
            gelir_secenekleri = {
                f"ID {row['ID']} | {row['Tarih']} | {row['Musteri']} | {row['Toplam']}": row['ID']
                for row in df_data_gl
            }

            secilen_label_gl = st.selectbox(
                "Silinecek geliri secin:",
                options=list(gelir_secenekleri.keys()),
                key="gl_sil_secim"
            )

            secilen_id_gl = gelir_secenekleri[secilen_label_gl]
            onay_key_gl = f"onay_gelir_{secilen_id_gl}"

            col_sil, col_uyari = st.columns([1, 3])

            with col_sil:
                if st.session_state.get(onay_key_gl, False):
                    if st.button("✅ Evet, Sil", type="primary", key=f"gl_onay_{secilen_id_gl}"):
                        db = get_db()
                        try:
                            gelir_obj = db.query(Gelir).filter(Gelir.id == secilen_id_gl).first()
                            if gelir_obj:
                                db.delete(gelir_obj)
                                db.commit()
                                st.success(f"✅ Silindi (ID: {secilen_id_gl})")
                                st.cache_data.clear()
                                st.session_state[onay_key_gl] = False
                                st.rerun()
                            else:
                                st.error("❌ Bulunamadi")
                        finally:
                            db.close()
                else:
                    if st.button("🗑️ Sil", type="secondary", key=f"gl_sil_{secilen_id_gl}"):
                        st.session_state[onay_key_gl] = True
                        st.rerun()

            with col_uyari:
                if st.session_state.get(onay_key_gl, False):
                    st.warning("⚠️ Bu islem geri alinamaz. Emin misiniz?")

    else:
        st.info("Bu kriterlere uyan gelir bulunamadi.")

st.markdown('</div>', unsafe_allow_html=True)
