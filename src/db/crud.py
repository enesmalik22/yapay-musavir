"""
CRUD fonksiyonlari - Create, Read, Update, Delete

Veritabani islemleri icin merkezi API. UI, agent ve testler buradan cagirir.
"""

from datetime import date
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session

from src.db.models import Kategori, Musteri, Gider, Gelir


# ============================================================================
# KATEGORI ISLEMLERI
# ============================================================================

def kategori_listele(db: Session, tip: Optional[str] = None) -> List[Kategori]:
    """
    Kategorileri listele.
    
    Args:
        db: Veritabani session
        tip: 'gider' veya 'gelir' filtreleme icin (opsiyonel)
    
    Returns:
        Kategori listesi
    """
    query = db.query(Kategori)
    if tip:
        query = query.filter(Kategori.tip == tip)
    return query.order_by(Kategori.ad).all()


def kategori_getir(db: Session, kategori_id: int) -> Optional[Kategori]:
    """Belirli bir kategoriyi ID ile getir."""
    return db.query(Kategori).filter(Kategori.id == kategori_id).first()


# ============================================================================
# MUSTERI ISLEMLERI
# ============================================================================

def musteri_ekle(
    db: Session,
    ad: str,
    vkn_tckn: Optional[str] = None,
    adres: Optional[str] = None,
    email: Optional[str] = None,
    telefon: Optional[str] = None,
    yurtdisi: bool = False,
    notlar: Optional[str] = None
) -> Musteri:
    """Yeni musteri ekle."""
    musteri = Musteri(
        ad=ad,
        vkn_tckn=vkn_tckn,
        adres=adres,
        email=email,
        telefon=telefon,
        yurtdisi=yurtdisi,
        notlar=notlar
    )
    db.add(musteri)
    db.commit()
    db.refresh(musteri)
    return musteri


def musteri_listele(db: Session) -> List[Musteri]:
    """Tum musterileri listele."""
    return db.query(Musteri).order_by(Musteri.ad).all()


def musteri_getir(db: Session, musteri_id: int) -> Optional[Musteri]:
    """Belirli bir musteriyi ID ile getir."""
    return db.query(Musteri).filter(Musteri.id == musteri_id).first()


# ============================================================================
# GIDER ISLEMLERI
# ============================================================================

def gider_ekle(
    db: Session,
    tarih: date,
    satici: str,
    kategori_id: int,
    tutar: float,
    kdv_orani: float,
    satici_vkn: Optional[str] = None,
    aciklama: Optional[str] = None,
    odeme_yontemi: Optional[str] = None,
    fatura_no: Optional[str] = None,
    fatura_dosyasi: Optional[str] = None
) -> Gider:
    """
    Yeni gider ekle.
    
    KDV tutari ve toplam otomatik hesaplanir.
    """
    tutar = Decimal(str(tutar))
    kdv_orani = Decimal(str(kdv_orani))

    kdv_tutari = tutar * (kdv_orani / Decimal("100"))
    toplam_tutar = tutar + kdv_tutari
    
    gider = Gider(
        tarih=tarih,
        satici=satici,
        satici_vkn=satici_vkn,
        kategori_id=kategori_id,
        tutar=tutar,
        kdv_orani=kdv_orani,
        kdv_tutari=kdv_tutari,
        toplam_tutar=toplam_tutar,
        aciklama=aciklama,
        odeme_yontemi=odeme_yontemi,
        fatura_no=fatura_no,
        fatura_dosyasi=fatura_dosyasi
    )
    db.add(gider)
    db.commit()
    db.refresh(gider)
    return gider


def gider_listele(
    db: Session,
    baslangic_tarihi: Optional[date] = None,
    bitis_tarihi: Optional[date] = None,
    kategori_id: Optional[int] = None
) -> List[Gider]:
    """
    Giderleri listele (opsiyonel filtrelerle).
    
    Args:
        db: Veritabani session
        baslangic_tarihi: Bu tarihten sonraki giderler
        bitis_tarihi: Bu tarihten onceki giderler
        kategori_id: Belirli kategoriye ait giderler
    """
    query = db.query(Gider)
    
    if baslangic_tarihi:
        query = query.filter(Gider.tarih >= baslangic_tarihi)
    if bitis_tarihi:
        query = query.filter(Gider.tarih <= bitis_tarihi)
    if kategori_id:
        query = query.filter(Gider.kategori_id == kategori_id)
    
    return query.order_by(Gider.tarih.desc()).all()


def gider_sil(db: Session, gider_id: int) -> bool:
    """Gideri sil. Basarili ise True doner."""
    gider = db.query(Gider).filter(Gider.id == gider_id).first()
    if gider:
        db.delete(gider)
        db.commit()
        return True
    return False


# ============================================================================
# GELIR ISLEMLERI
# ============================================================================

def gelir_ekle(
    db: Session,
    tarih: date,
    musteri_id: int,
    kategori_id: int,
    tutar: float,
    kdv_orani: float,
    stopaj_orani: float = 0,
    fatura_no: Optional[str] = None,
    aciklama: Optional[str] = None,
    odendi: bool = False,
    odeme_tarihi: Optional[date] = None
) -> Gelir:
    """
    Yeni gelir ekle.
    
    KDV, stopaj ve net tahsilat otomatik hesaplanir.
    """
    tutar = Decimal(str(tutar))
    kdv_orani = Decimal(str(kdv_orani))

    kdv_tutari = tutar * (kdv_orani / Decimal("100"))
    toplam_tutar = tutar + kdv_tutari
    stopaj_tutari = tutar * (stopaj_orani / 100)
    net_tahsilat = toplam_tutar - stopaj_tutari
    
    gelir = Gelir(
        tarih=tarih,
        musteri_id=musteri_id,
        kategori_id=kategori_id,
        fatura_no=fatura_no,
        tutar=tutar,
        kdv_orani=kdv_orani,
        kdv_tutari=kdv_tutari,
        stopaj_orani=stopaj_orani,
        stopaj_tutari=stopaj_tutari,
        toplam_tutar=toplam_tutar,
        net_tahsilat=net_tahsilat,
        aciklama=aciklama,
        odendi=odendi,
        odeme_tarihi=odeme_tarihi
    )
    db.add(gelir)
    db.commit()
    db.refresh(gelir)
    return gelir


def gelir_listele(
    db: Session,
    baslangic_tarihi: Optional[date] = None,
    bitis_tarihi: Optional[date] = None,
    musteri_id: Optional[int] = None,
    odendi: Optional[bool] = None
) -> List[Gelir]:
    """Gelirleri listele (opsiyonel filtrelerle)."""
    query = db.query(Gelir)
    
    if baslangic_tarihi:
        query = query.filter(Gelir.tarih >= baslangic_tarihi)
    if bitis_tarihi:
        query = query.filter(Gelir.tarih <= bitis_tarihi)
    if musteri_id:
        query = query.filter(Gelir.musteri_id == musteri_id)
    if odendi is not None:
        query = query.filter(Gelir.odendi == odendi)
    
    return query.order_by(Gelir.tarih.desc()).all()


def gelir_odendi_isaretle(db: Session, gelir_id: int, odeme_tarihi: date) -> Optional[Gelir]:
    """Geliri 'odendi' olarak isaretle."""
    gelir = db.query(Gelir).filter(Gelir.id == gelir_id).first()
    if gelir:
        gelir.odendi = True
        gelir.odeme_tarihi = odeme_tarihi
        db.commit()
        db.refresh(gelir)
    return gelir
