"""
Gelir Ekleme Sayfasi (Dark Mode UI).
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
.ym-logo {
    display: flex;
    align-items: center;
    gap: 9px;
    text-decoration: none;
}
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

.ym-topbar-right {
    display: flex; align-items: center; gap: 8px;
}
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

/* Nav (st.page_link) */
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
    text-align: center !important;
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

/* Section header */
[data-testid="stMarkdownContainer"] h3 {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: rgba(255,255,255,0.85) !important;
    margin-bottom: 14px !important;
    margin-top: 0 !important;
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

/* Expander (Yeni Musteri Ekle) */
[data-testid="stExpander"] {
    background: #1a2031 !important;
    border: 0.5px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    padding: 14px 18px !important;
    color: #e8edf5 !important;
    font-weight: 500 !important;
}
[data-testid="stExpander"] summary:hover {
    background: rgba(255,255,255,0.03) !important;
}

/* KDV ozet kutusu */
.ym-kdv-summary {
    background: linear-gradient(135deg, rgba(77,138,255,0.08) 0%, rgba(77,138,255,0.03) 100%);
    border: 0.5px solid rgba(77,138,255,0.2);
    border-radius: 12px;
    padding: 18px;
    margin-top: 12px;
}
.ym-kdv-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 10px 0;
    border-bottom: 0.5px solid rgba(255,255,255,0.06);
}
.ym-kdv-row:last-child { border-bottom: none; }
.ym-kdv-row-label {
    font-size: 12px;
    color: rgba(255,255,255,0.55);
    text-transform: uppercase;
    letter-spacing: 0.4px;
}
.ym-kdv-row-val {
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
}
.ym-kdv-row-val.accent { color: #6aaeff; }
.ym-kdv-row-val.success { color: #5cb85c; }

/* Submit button (form icindeki) */
.stFormSubmitButton button {
    background: linear-gradient(135deg, #4d8aff 0%, #2d5aaa 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: white !important;
    transition: all 0.2s ease;
    box-shadow: 0 4px 14px rgba(77,138,255,0.25);
}
.stFormSubmitButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(77,138,255,0.4) !important;
}

/* Normal button (Musteri Ekle) */
.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #4d8aff 0%, #2d5aaa 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: white !important;
    transition: all 0.2s ease;
}
.stButton button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(77,138,255,0.3) !important;
}

/* File uploader */
[data-testid="stFileUploader"] section {
    background: #0d1117 !important;
    border: 1px dashed rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
}

/* Checkbox */
[data-testid="stCheckbox"] label {
    color: rgba(255,255,255,0.85) !important;
}

/* Bilgi kutusu */
.ym-info-box {
    background: rgba(77,138,255,0.08);
    border-left: 3px solid #4d8aff;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 18px;
    font-size: 12px;
    color: rgba(255,255,255,0.75);
    line-height: 1.6;
}
.ym-info-box strong { color: #6aaeff; }

/* Section divider with icon */
.ym-section-title {
    font-size: 15px;
    font-weight: 600;
    color: #e8edf5;
    margin: 18px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
    padding-bottom: 10px;
    border-bottom: 0.5px solid rgba(255,255,255,0.06);
}

/* Divider sade */
hr { border-color: rgba(255,255,255,0.06) !important; margin: 20px 0 !important; }
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
        Gelir <span>ekle</span>
    </div>
    <div class="ym-hero-sub">
        Satis faturanizi sisteme kaydet, KDV otomatik hesaplansin.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# BODY
# ============================================================================
st.markdown('<div class="ym-body">', unsafe_allow_html=True)

# Bilgi kutusu
st.markdown("""
<div class="ym-info-box">
    💡 <strong>Tutari KDV dahil girin.</strong> Sistem KDV tutarini otomatik hesaplar.
    Ornek: 118 TL girersen → KDV: 10,73 TL, Net: 107,27 TL
</div>
""", unsafe_allow_html=True)


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


def fatura_dosyasi_kaydet(uploaded_file):
    upload_dir = PROJECT_ROOT / "data" / "uploads" / "gelirler"
    upload_dir.mkdir(parents=True, exist_ok=True)
    timestamp = date.today().strftime("%Y%m%d")
    filename = f"{timestamp}_{uploaded_file.name}"
    filepath = upload_dir / filename
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(filepath)


def fmt(sayi):
    try:
        formatted = f"{float(sayi):,.2f}"
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{formatted} TL"
    except (TypeError, ValueError):
        return "0,00 TL"


# ============================================================================
# MUSTERI YONETIMI
# ============================================================================
st.markdown('<div class="ym-section-title">👤 Musteri Yonetimi</div>', unsafe_allow_html=True)

with st.expander("➕ Yeni Musteri Ekle"):
    col1, col2 = st.columns(2)
    with col1:
        yeni_m_ad = st.text_input("Musteri Adi", key="new_m_name")
        yeni_m_vkn = st.text_input("VKN/TCKN", max_chars=11, key="new_m_vkn")
    with col2:
        yeni_m_email = st.text_input("E-posta", key="new_m_email")
        yeni_m_tel = st.text_input("Telefon", key="new_m_tel")

    if st.button("💾 Musteri Ekle", type="primary", key="btn_musteri_ekle"):
        if not yeni_m_ad or not yeni_m_ad.strip():
            st.error("❌ Musteri adi bos olamaz")
        else:
            db = get_db()
            try:
                yeni = musteri_ekle(
                    db=db,
                    ad=yeni_m_ad.strip(),
                    vkn_tckn=yeni_m_vkn.strip() if yeni_m_vkn else None,
                    email=yeni_m_email.strip() if yeni_m_email else None,
                    telefon=yeni_m_tel.strip() if yeni_m_tel else None,
                    yurtdisi=False
                )
                st.success(f"✅ Musteri eklendi: {yeni.ad}")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Hata: {e}")
            finally:
                db.close()


# ============================================================================
# GELIR FORMU
# ============================================================================
st.markdown('<div class="ym-section-title">📋 Satis Bilgileri</div>', unsafe_allow_html=True)

musteriler = musterileri_getir()

if not musteriler:
    st.warning("⚠️ Henuz musteri yok. Yukaridan yeni musteri ekleyin.")
    st.stop()

kategoriler = kategorileri_getir()
kategori_dict = {k.ad: k for k in kategoriler}
musteri_dict = {m.ad: m for m in musteriler}


with st.form("gelir_ekle_form", clear_on_submit=True):

    col1, col2 = st.columns([1.2, 1])

    # SOL: Satis bilgileri
    with col1:
        st.markdown("### 📋 Temel Bilgiler")

        tarih = st.date_input("Tarih *", value=date.today())

        musteri_secim = st.selectbox(
            "Musteri *",
            options=list(musteri_dict.keys())
        )
        secilen_musteri = musteri_dict[musteri_secim]

        kategori_adi = st.selectbox(
            "Kategori *",
            options=list(kategori_dict.keys()),
            help="KDV orani kategoriden otomatik gelir"
        )
        secilen_kategori = kategori_dict[kategori_adi]

        st.markdown("---")
        st.markdown("### 📝 Detay")

        aciklama = st.text_area(
            "Aciklama (opsiyonel)",
            placeholder="Satisin detayi, urun/hizmet adi...",
            height=100
        )

        odendi = st.checkbox("Tahsilat alindi mi?")
        odeme_tarihi = st.date_input(
            "Odeme Tarihi",
            value=date.today()
        )

        fatura_dosyasi = st.file_uploader(
            "Fatura Dosyasi (Opsiyonel)",
            type=["pdf", "jpg", "jpeg", "png"]
        )

    # SAG: Tutar bilgileri
    with col2:
        st.markdown("### 💰 Tutar Bilgileri")

        tutar = st.number_input(
            "Tutar (KDV dahil) *",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            help="Faturanin toplam tutari (KDV dahil)"
        )

        kdv_orani = st.number_input(
            "KDV Orani (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(secilen_kategori.kdv_orani),
            step=1.0,
            format="%.2f"
        )

        toplam = tutar
        kdv_tutari = toplam - (toplam / (1 + kdv_orani / 100)) if kdv_orani > 0 else 0
        kdv_haric = toplam - kdv_tutari

        st.markdown(f"""
        <div class="ym-kdv-summary">
            <div class="ym-kdv-row">
                <span class="ym-kdv-row-label">Satis Tutari (KDV dahil)</span>
                <span class="ym-kdv-row-val">{fmt(toplam)}</span>
            </div>
            <div class="ym-kdv-row">
                <span class="ym-kdv-row-label">KDV Tutari</span>
                <span class="ym-kdv-row-val accent">{fmt(kdv_tutari)}</span>
            </div>
            <div class="ym-kdv-row">
                <span class="ym-kdv-row-label">KDV Haric Net</span>
                <span class="ym-kdv-row-val success">{fmt(kdv_haric)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Submit
    submitted = st.form_submit_button(
        "💾 Satisi Kaydet",
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
                stopaj_orani=0,
                fatura_no=None,
                aciklama=aciklama.strip() if aciklama else None,
                odendi=odendi,
                odeme_tarihi=odeme_tarihi if odendi else None
            )

            st.success(f"✅ Satis basariyla kaydedildi! (ID: {yeni_gelir.id})")
            st.balloons()
            st.cache_data.clear()

        except Exception as e:
            st.error(f"❌ Kayit hatasi: {e}")
        finally:
            db.close()

st.markdown('</div>', unsafe_allow_html=True)
