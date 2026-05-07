"""
AI Asistan Sayfasi (Dark Mode UI).
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.agents.sql_agent import soru_sor


st.set_page_config(
    page_title="AI Asistan - YapayMusavir",
    page_icon="🤖",
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
    position: relative;
    overflow: hidden;
}
.ym-hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(77,138,255,0.15);
    border: 0.5px solid rgba(77,138,255,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 11px;
    color: #6aaeff;
    margin-bottom: 12px;
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
    max-width: 520px;
}

/* Body */
.ym-body { padding: 24px 32px 32px; }

/* Section title */
.ym-section-title {
    font-size: 13px;
    font-weight: 600;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
    letter-spacing: 0.7px;
    margin: 8px 0 14px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Ornek soru butonlari */
.stButton button {
    background: #1a2031 !important;
    border: 0.5px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    color: rgba(255,255,255,0.85) !important;
    padding: 16px 18px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
    height: auto !important;
    min-height: 60px;
    line-height: 1.4 !important;
}
.stButton button:hover {
    background: #1f2638 !important;
    border-color: rgba(77,138,255,0.4) !important;
    color: #ffffff !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(77,138,255,0.15);
}

/* Sohbeti temizle butonu - kirmizi */
.ym-clear-wrap .stButton button {
    background: rgba(224,92,92,0.1) !important;
    border: 0.5px solid rgba(224,92,92,0.3) !important;
    color: #ff8a8a !important;
    text-align: center !important;
    min-height: 42px !important;
    padding: 10px 16px !important;
    font-weight: 500 !important;
}
.ym-clear-wrap .stButton button:hover {
    background: rgba(224,92,92,0.18) !important;
    border-color: rgba(224,92,92,0.5) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px rgba(224,92,92,0.2) !important;
}

/* Chat mesajlari */
[data-testid="stChatMessage"] {
    background: #1a2031 !important;
    border: 0.5px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    margin-bottom: 10px !important;
}
[data-testid="stChatMessage"][data-testid*="user"] {
    background: linear-gradient(135deg, rgba(77,138,255,0.12) 0%, rgba(77,138,255,0.05) 100%) !important;
    border-color: rgba(77,138,255,0.25) !important;
}
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    background: #4d8aff !important;
}
[data-testid="stChatMessage"] p {
    color: #e8edf5 !important;
    line-height: 1.6 !important;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: #1a2031 !important;
    border: 0.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #4d8aff !important;
    box-shadow: 0 0 0 2px rgba(77,138,255,0.15) !important;
}
[data-testid="stChatInput"] textarea {
    color: #e8edf5 !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(255,255,255,0.3) !important;
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
    line-height: 1.7;
}
.ym-info-box strong { color: #6aaeff; }
.ym-info-box ul {
    margin: 6px 0 0 0;
    padding-left: 20px;
}

/* Uyari kutusu */
.ym-warning-box {
    background: rgba(212,160,23,0.08);
    border-left: 3px solid #d4a017;
    border-radius: 8px;
    padding: 14px 16px;
    margin-top: 18px;
    font-size: 12px;
    color: rgba(255,255,255,0.7);
    line-height: 1.6;
}
.ym-warning-box strong { color: #d4a017; }

/* Subheader */
[data-testid="stMarkdownContainer"] h3 {
    font-size: 16px !important;
    font-weight: 600 !important;
    color: rgba(255,255,255,0.9) !important;
    margin-bottom: 14px !important;
}

/* Bos chat placeholder */
.ym-empty-chat {
    background: #1a2031;
    border: 0.5px dashed rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 32px;
    text-align: center;
    color: rgba(255,255,255,0.4);
    font-size: 13px;
    margin-bottom: 18px;
}

hr { border-color: rgba(255,255,255,0.06) !important; margin: 16px 0 !important; }
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
    <div class="ym-hero-eyebrow">
        ✨ Yapay zeka destekli
    </div>
    <div class="ym-hero-title">
        AI <span>Asistan</span>
    </div>
    <div class="ym-hero-sub">
        Vergi ve fatura verilerin hakkinda dogal Turkce ile soru sor, anlik cevap al.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# BODY
# ============================================================================
st.markdown('<div class="ym-body">', unsafe_allow_html=True)


# Session state baslatma
if "chat_gecmisi" not in st.session_state:
    st.session_state.chat_gecmisi = []


# ============================================================================
# UST: ORNEK SORULAR + IPUCLARI (2 kolon)
# ============================================================================

ust_col1, ust_col2 = st.columns([2, 1])

with ust_col1:
    st.markdown('<div class="ym-section-title">💡 Ornek Sorular</div>', unsafe_allow_html=True)

    ornek_sorular = [
        "Toplam kac gider kaydim var?",
        "Toplam ne kadar harcama yaptim?",
        "En son eklenen 3 gider neydi?",
        "Hangi musterilerden gelir geldi?",
        "Yemek kategorisindeki harcamalar ne kadar?",
        "Toplam KDV ne kadar?",
    ]

    sg1, sg2, sg3 = st.columns(3)
    with sg1:
        if st.button(ornek_sorular[0], use_container_width=True, key="orn1"):
            st.session_state.son_soru = ornek_sorular[0]
        if st.button(ornek_sorular[3], use_container_width=True, key="orn4"):
            st.session_state.son_soru = ornek_sorular[3]
    with sg2:
        if st.button(ornek_sorular[1], use_container_width=True, key="orn2"):
            st.session_state.son_soru = ornek_sorular[1]
        if st.button(ornek_sorular[4], use_container_width=True, key="orn5"):
            st.session_state.son_soru = ornek_sorular[4]
    with sg3:
        if st.button(ornek_sorular[2], use_container_width=True, key="orn3"):
            st.session_state.son_soru = ornek_sorular[2]
        if st.button(ornek_sorular[5], use_container_width=True, key="orn6"):
            st.session_state.son_soru = ornek_sorular[5]

with ust_col2:
    st.markdown('<div class="ym-section-title">⚙️ Ayarlar</div>', unsafe_allow_html=True)

    st.markdown('<div class="ym-clear-wrap">', unsafe_allow_html=True)
    if st.button("🗑️ Sohbeti Temizle", use_container_width=True, key="clear_chat"):
        st.session_state.chat_gecmisi = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="ym-info-box">
        <strong>💡 Ipuclari</strong>
        <ul>
            <li>Dogal Turkce ile sor</li>
            <li>Tarih, kategori, musteri ile spesifik ol</li>
            <li>Cevap icin 30-60 saniye bekle</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# SOHBET ALANI
# ============================================================================

st.markdown('<div class="ym-section-title" style="margin-top:18px;">💬 Sohbet</div>', unsafe_allow_html=True)

# Mevcut sohbet bos mu?
if not st.session_state.chat_gecmisi:
    st.markdown("""
    <div class="ym-empty-chat">
        Henuz mesaj yok. Yukaridan ornek bir soru sec ya da asagidaki kutuya yaz.
    </div>
    """, unsafe_allow_html=True)
else:
    for mesaj in st.session_state.chat_gecmisi:
        if mesaj["rol"] == "kullanici":
            with st.chat_message("user"):
                st.write(mesaj["icerik"])
        else:
            with st.chat_message("assistant"):
                st.write(mesaj["icerik"])


# ============================================================================
# INPUT
# ============================================================================

soru_input = st.chat_input("Sorunuzu yazin...")

# Ornek butondan gelen soru varsa al
if "son_soru" in st.session_state:
    soru_input = st.session_state.son_soru
    del st.session_state.son_soru

if soru_input:
    st.session_state.chat_gecmisi.append({
        "rol": "kullanici",
        "icerik": soru_input
    })

    with st.chat_message("user"):
        st.write(soru_input)

    with st.chat_message("assistant"):
        with st.spinner("🤔 Dusunuyorum... (bu islem 30-60 saniye surebilir)"):
            try:
                cevap = soru_sor(soru_input)
            except Exception as e:
                cevap = f"❌ Bir hata olustu: {str(e)}"
        st.write(cevap)

    st.session_state.chat_gecmisi.append({
        "rol": "asistan",
        "icerik": cevap
    })


# Uyari kutusu
st.markdown("""
<div class="ym-warning-box">
    <strong>⚠️ Dikkat:</strong> AI cevaplari her zaman dogru olmayabilir.
    Onemli kararlar oncesi verileri Liste sayfasindan kontrol edin.
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
