"""
YapayMusavir - Ana Sayfa (Dark Mode)
"""

import sys
from pathlib import Path
from decimal import Decimal
from datetime import date
import calendar

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import plotly.graph_objects as go

from src.db.database import get_db
from src.db.crud import kategori_listele, musteri_listele, gider_listele, gelir_listele

st.set_page_config(
    page_title="YapayMusavir",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"] { display: none; }
[data-testid="stAppViewContainer"] { background: #0d1117; }

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
    width: 30px;
    height: 30px;
    background: #4d8aff;
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.ym-logo-name {
    font-size: 15px;
    font-weight: 600;
    color: #e8edf5;
    letter-spacing: -0.3px;
}
.ym-logo-dot { color: #4d8aff; }

.ym-nav {
    display: flex;
    align-items: center;
    gap: 2px;
}
.ym-nav a {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 12px;
    color: rgba(255,255,255,0.45);
    text-decoration: none;
    white-space: nowrap;
    transition: all 0.15s;
}
.ym-nav a:hover {
    background: rgba(255,255,255,0.06);
    color: rgba(255,255,255,0.85);
}
.ym-nav a.active {
    background: rgba(77,138,255,0.15);
    color: #4d8aff;
    font-weight: 500;
}

.ym-topbar-right {
    display: flex;
    align-items: center;
    gap: 8px;
}
.ym-notif {
    width: 28px;
    height: 28px;
    border-radius: 7px;
    background: rgba(255,255,255,0.06);
    border: 0.5px solid rgba(255,255,255,0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255,255,255,0.4);
    cursor: pointer;
    position: relative;
}
.ym-notif-dot {
    width: 6px;
    height: 6px;
    background: #4d8aff;
    border-radius: 50%;
    position: absolute;
    top: 4px;
    right: 4px;
    border: 1.5px solid #111827;
}
.ym-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #4d8aff;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 11px;
    font-weight: 600;
}

.ym-hero {
    background: #0f1d3a;
    padding: 32px 32px 28px;
    position: relative;
    overflow: hidden;
}
.ym-hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.07);
    border: 0.5px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 11px;
    color: rgba(255,255,255,0.5);
    margin-bottom: 14px;
}
.ym-hero-headline {
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}
.ym-hero-headline span { color: #6aaeff; }
.ym-hero-sub {
    font-size: 13px;
    color: rgba(255,255,255,0.38);
    line-height: 1.6;
    margin-bottom: 24px;
    max-width: 380px;
}
.ym-hero-stats {
    display: flex;
    gap: 0;
}
.ym-hstat {
    padding-right: 24px;
    margin-right: 24px;
    border-right: 0.5px solid rgba(255,255,255,0.1);
}
.ym-hstat:last-child {
    border-right: none;
    padding-right: 0;
    margin-right: 0;
}
.ym-hstat-val {
    font-size: 19px;
    font-weight: 600;
    color: #ffffff;
}
.ym-hstat-label {
    font-size: 11px;
    color: rgba(255,255,255,0.32);
    margin-top: 2px;
}

.ym-kdv-float {
    position: absolute;
    right: 32px;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255,255,255,0.05);
    border: 0.5px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 18px 22px;
    min-width: 210px;
}
.ym-kdv-label {
    font-size: 10px;
    color: rgba(255,255,255,0.32);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}
.ym-kdv-amount {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
}
.ym-kdv-period {
    font-size: 10px;
    color: rgba(255,255,255,0.28);
    margin-top: 3px;
}
.ym-kdv-row {
    display: flex;
    gap: 8px;
    margin-top: 12px;
}
.ym-kdv-mini {
    background: rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 7px 10px;
    flex: 1;
}
.ym-kdv-mini-label {
    font-size: 9px;
    color: rgba(255,255,255,0.28);
}
.ym-kdv-mini-val {
    font-size: 12px;
    color: rgba(255,255,255,0.8);
    font-weight: 600;
    margin-top: 2px;
}

.ym-body {
    padding: 22px 32px 32px;
    background: #0d1117;
}
.ym-section-head {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    color: rgba(255,255,255,0.3);
    margin-bottom: 12px;
    margin-top: 22px;
}
.ym-section-head:first-child { margin-top: 0; }
.ym-section-head svg { opacity: 0.5; }

.ym-cards {
    display: grid;
    grid-template-columns: repeat(4, minmax(0,1fr));
    gap: 10px;
}
.ym-card {
    background: #1a2031;
    border: 0.5px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 16px;
}
.ym-card-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 12px;
}
.ym-card-label {
    font-size: 11px;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    letter-spacing: 0.4px;
    margin-bottom: 5px;
}
.ym-card-val {
    font-size: 18px;
    font-weight: 700;
    color: #e8edf5;
}
.ym-card-badge {
    display: inline-flex;
    align-items: center;
    font-size: 10px;
    margin-top: 7px;
    padding: 2px 8px;
    border-radius: 20px;
    font-weight: 500;
}

.ym-charts {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}
.ym-chart-card {
    background: #1a2031;
    border: 0.5px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 16px 16px 8px;
}
.ym-chart-title {
    font-size: 12px;
    font-weight: 600;
    color: #e8edf5;
    margin-bottom: 4px;
}

/* === NAV (st.page_link) === */
.stMainBlockContainer > div:has([data-testid="stPageLink"]) {
    background: #0d1117;
    padding: 8px 24px 4px !important;
    border-bottom: 0.5px solid rgba(255,255,255,0.06);
    margin-top: 0 !important;
}
[data-testid="stPageLink"] {
    margin: 0 !important;
}
[data-testid="stPageLink"] {
    width: 100% !important;
}
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
/* Topbar'i sticky yapma — nav'i da topbar gibi davransin */
.ym-topbar { margin-bottom: 0 !important; }

</style>
""", unsafe_allow_html=True)


def fmt(tutar):
    if tutar is None:
        return "0,00 TL"
    try:
        f = f"{float(tutar):,.2f}"
        return f.replace(",", "X").replace(".", ",").replace("X", ".") + " TL"
    except:
        return "0,00 TL"


@st.cache_data(ttl=60)
def ozet_verileri_getir():
    db = get_db()
    try:
        giderler = gider_listele(db)
        gelirler = gelir_listele(db)
        musteriler = musteri_listele(db)
        tum_kategoriler = {k.id: k.ad for k in kategori_listele(db)}

        toplam_gider_brut = sum(Decimal(str(g.toplam_tutar)) for g in giderler)
        toplam_gelir_brut = sum(Decimal(str(g.toplam_tutar)) for g in gelirler)
        net_kar = (
            sum(Decimal(str(g.tutar)) for g in gelirler) -
            sum(Decimal(str(g.tutar)) for g in giderler)
        )

        bugun = date.today()
        ay_basi = date(bugun.year, bugun.month, 1)
        ay_sonu = date(bugun.year, bugun.month,
                       calendar.monthrange(bugun.year, bugun.month)[1])

        bu_ay_giderler = gider_listele(db, baslangic_tarihi=ay_basi, bitis_tarihi=ay_sonu)
        bu_ay_gelirler = gelir_listele(db, baslangic_tarihi=ay_basi, bitis_tarihi=ay_sonu)

        bu_ay_toplanan = sum(Decimal(str(g.kdv_tutari)) for g in bu_ay_gelirler)
        bu_ay_odenen = sum(Decimal(str(g.kdv_tutari)) for g in bu_ay_giderler)
        bu_ay_odenecek = bu_ay_toplanan - bu_ay_odenen

        kategori_gider = {}
        for g in giderler:
            ad = tum_kategoriler.get(g.kategori_id, "Diger")
            kategori_gider[ad] = kategori_gider.get(ad, 0) + float(g.toplam_tutar)

        musteri_gelir = {}
        for g in gelirler:
            musteri_gelir[g.musteri_id] = musteri_gelir.get(g.musteri_id, 0) + float(g.toplam_tutar)

        musteri_dict = {m.id: m.ad for m in musteriler}
        musteri_gelir_named = {
            musteri_dict.get(k, "Bilinmeyen"): v
            for k, v in sorted(musteri_gelir.items(), key=lambda x: -x[1])
        }

        return {
            "gider_sayisi": len(giderler),
            "gelir_sayisi": len(gelirler),
            "musteri_sayisi": len(musteriler),
            "toplam_gider_brut": toplam_gider_brut,
            "toplam_gelir_brut": toplam_gelir_brut,
            "net_kar": net_kar,
            "bu_ay_toplanan": bu_ay_toplanan,
            "bu_ay_odenen": bu_ay_odenen,
            "bu_ay_odenecek": bu_ay_odenecek,
            "bu_ay_ad": bugun.strftime("%B %Y"),
            "kategori_gider": kategori_gider,
            "musteri_gelir": musteri_gelir_named,
        }
    finally:
        db.close()


ozet = ozet_verileri_getir()
odenecek = ozet["bu_ay_odenecek"]

# ============================================================================
# TOPBAR
# ============================================================================
st.markdown(f"""
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
# NAV (st.page_link)
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
st.markdown(f"""
<div class="ym-hero">
    <div class="ym-hero-eyebrow">
        <svg width="11" height="11" viewBox="0 0 11 11" fill="none"><rect x="1" y="1" width="9" height="9" rx="2" stroke="rgba(255,255,255,0.5)" stroke-width="1.1"/><path d="M4 1v2M7 1v2M1 4.5h9" stroke="rgba(255,255,255,0.5)" stroke-width="1.1" stroke-linecap="round"/></svg>
        {ozet['bu_ay_ad']} &mdash; Aktif donem
    </div>
    <div class="ym-hero-headline">
        Vergini sen hesapla,<br>
        <span>surprize ugrama.</span>
    </div>
    <div class="ym-hero-sub">
        Tum gelir ve giderlerini tek yerden takip et.
        KDV borcunu aninda gor, Excel'e aktar.
    </div>
    <div class="ym-hero-stats">
        <div class="ym-hstat">
            <div class="ym-hstat-val">{fmt(ozet['toplam_gelir_brut'])}</div>
            <div class="ym-hstat-label">Toplam satis</div>
        </div>
        <div class="ym-hstat">
            <div class="ym-hstat-val">{fmt(ozet['toplam_gider_brut'])}</div>
            <div class="ym-hstat-label">Toplam gider</div>
        </div>
        <div class="ym-hstat">
            <div class="ym-hstat-val">{fmt(ozet['net_kar'])}</div>
            <div class="ym-hstat-label">Net kar</div>
        </div>
    </div>
    <div class="ym-kdv-float">
        <div class="ym-kdv-label">Tahmini KDV Borcu</div>
        <div class="ym-kdv-amount">{fmt(odenecek)}</div>
        <div class="ym-kdv-period">{ozet['bu_ay_ad']}</div>
        <div class="ym-kdv-row">
            <div class="ym-kdv-mini">
                <div class="ym-kdv-mini-label">Toplanan</div>
                <div class="ym-kdv-mini-val">{fmt(ozet['bu_ay_toplanan'])}</div>
            </div>
            <div class="ym-kdv-mini">
                <div class="ym-kdv-mini-label">Indirilecek</div>
                <div class="ym-kdv-mini-val">{fmt(ozet['bu_ay_odenen'])}</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# BODY
# ============================================================================
st.markdown('<div class="ym-body">', unsafe_allow_html=True)

# Metrik Kartlar
st.markdown("""
<div class="ym-section-head">
    <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><rect x="1" y="6" width="2.5" height="6" rx="0.5" fill="rgba(255,255,255,0.3)"/><rect x="5" y="3.5" width="2.5" height="8.5" rx="0.5" fill="rgba(255,255,255,0.3)"/><rect x="9" y="1" width="2.5" height="11" rx="0.5" fill="rgba(255,255,255,0.3)"/></svg>
    Genel Ozet
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="ym-cards">
    <div class="ym-card">
        <div class="ym-card-icon" style="background:rgba(92,184,92,0.15);">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M8 2v12M4 6l4-4 4 4" stroke="#5cb85c" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div class="ym-card-label">Toplam Satis</div>
        <div class="ym-card-val">{fmt(ozet['toplam_gelir_brut'])}</div>
        <span class="ym-card-badge" style="background:rgba(92,184,92,0.12);color:#5cb85c;">KDV dahil</span>
    </div>
    <div class="ym-card">
        <div class="ym-card-icon" style="background:rgba(224,92,92,0.15);">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M8 2v12M4 10l4 4 4-4" stroke="#e05c5c" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div class="ym-card-label">Toplam Gider</div>
        <div class="ym-card-val">{fmt(ozet['toplam_gider_brut'])}</div>
        <span class="ym-card-badge" style="background:rgba(224,92,92,0.12);color:#e05c5c;">KDV dahil</span>
    </div>
    <div class="ym-card">
        <div class="ym-card-icon" style="background:rgba(77,138,255,0.15);">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <circle cx="8" cy="8" r="6" stroke="#4d8aff" stroke-width="1.5"/>
                <path d="M8 5v3.5l2.5 1.5" stroke="#4d8aff" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
        </div>
        <div class="ym-card-label">Net Kar</div>
        <div class="ym-card-val">{fmt(ozet['net_kar'])}</div>
        <span class="ym-card-badge" style="background:rgba(77,138,255,0.12);color:#4d8aff;">KDV haric</span>
    </div>
    <div class="ym-card">
        <div class="ym-card-icon" style="background:rgba(212,160,23,0.15);">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <circle cx="6" cy="6" r="3" stroke="#d4a017" stroke-width="1.5"/>
                <circle cx="10.5" cy="6" r="3" stroke="#d4a017" stroke-width="1.5"/>
                <path d="M1 14c0-2.5 2-4 5-4h4c3 0 5 1.5 5 4" stroke="#d4a017" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
        </div>
        <div class="ym-card-label">Musteri Sayisi</div>
        <div class="ym-card-val">{ozet['musteri_sayisi']}</div>
        <span class="ym-card-badge" style="background:rgba(212,160,23,0.12);color:#d4a017;">aktif</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Grafikler
st.markdown("""
<div class="ym-section-head" style="margin-top:22px;">
    <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><circle cx="6.5" cy="6.5" r="5" stroke="rgba(255,255,255,0.3)" stroke-width="1.1"/><path d="M6.5 6.5L6.5 2" stroke="rgba(255,255,255,0.3)" stroke-width="1.1" stroke-linecap="round"/><path d="M6.5 6.5L10 8.5" stroke="rgba(255,255,255,0.3)" stroke-width="1.1" stroke-linecap="round"/></svg>
    Dagilim Grafikleri
</div>
<div class="ym-charts">
""", unsafe_allow_html=True)

PALETTE = ["#1a3a6e","#2d5aaa","#4d8aff","#6aaeff","#7ab8f0","#9ab8e0","#c0d4f0"]

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="ym-chart-card"><div class="ym-chart-title">Gider Dagilimi</div>', unsafe_allow_html=True)
    if ozet["kategori_gider"]:
        fig = go.Figure(data=[go.Pie(
            labels=list(ozet["kategori_gider"].keys()),
            values=list(ozet["kategori_gider"].values()),
            hole=0.55,
            marker=dict(
                colors=PALETTE[:len(ozet["kategori_gider"])],
                line=dict(color="#1a2031", width=2)
            ),
            textinfo="label+percent",
            textfont=dict(size=10, color="#e8edf5"),
        )])
        fig.update_layout(
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=8, b=8, l=8, r=8),
            height=190,
            annotations=[dict(
                text="Giderler",
                x=0.5, y=0.5,
                font=dict(size=11, color="#e8edf5"),
                showarrow=False
            )]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Henuz gider verisi yok.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="ym-chart-card"><div class="ym-chart-title">Musteri Bazli Gelir</div>', unsafe_allow_html=True)
    if ozet["musteri_gelir"]:
        isimler = list(ozet["musteri_gelir"].keys())
        tutarlar = list(ozet["musteri_gelir"].values())
        fig2 = go.Figure(data=[go.Bar(
            x=tutarlar,
            y=isimler,
            orientation='h',
            marker=dict(
                color=PALETTE[:len(isimler)],
                line=dict(width=0)
            ),
            text=[fmt(t) for t in tutarlar],
            textposition='outside',
            textfont=dict(size=10, color="rgba(255,255,255,0.5)"),
        )])
        fig2.update_layout(
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=8, b=8, l=8, r=90),
            height=190,
            xaxis=dict(visible=False, range=[0, max(tutarlar) * 1.35]),
            yaxis=dict(
                tickfont=dict(size=10, color="rgba(255,255,255,0.45)"),
                autorange="reversed",
                ticklen=0,
            ),
            bargap=0.45,
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Henuz gelir verisi yok.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Yenile + Disclaimer
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;margin-top:20px;padding-top:16px;border-top:0.5px solid rgba(255,255,255,0.06);">
    <span style="font-size:11px;color:rgba(255,255,255,0.2);">⚠️ Bu uygulama mali musavir yerine gecmez.</span>
</div>
""", unsafe_allow_html=True)

if st.button("🔄 Verileri Yenile", key="refresh"):
    st.cache_data.clear()
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
