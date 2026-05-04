"""
YapayMusavir veritabani modelleri.
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Numeric, Date, DateTime,
    Boolean, Text, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Kategori(Base):
    __tablename__ = "kategoriler"

    id = Column(Integer, primary_key=True)
    ad = Column(String(100), nullable=False, unique=True)
    tip = Column(String(10), nullable=False)
    kdv_orani = Column(Numeric(5, 2), nullable=False, default=20.00)
    stopaj_orani = Column(Numeric(5, 2), default=0)
    dusulebilir = Column(Boolean, default=True)
    aciklama = Column(Text)
    olusturma_tarihi = Column(DateTime, default=datetime.utcnow)

    giderler = relationship("Gider", back_populates="kategori")
    gelirler = relationship("Gelir", back_populates="kategori")

    def __repr__(self):
        return f"<Kategori(id={self.id}, ad='{self.ad}')>"


class Musteri(Base):
    __tablename__ = "musteriler"

    id = Column(Integer, primary_key=True)
    ad = Column(String(200), nullable=False)
    vkn_tckn = Column(String(11))
    adres = Column(Text)
    email = Column(String(150))
    telefon = Column(String(20))
    yurtdisi = Column(Boolean, default=False)
    notlar = Column(Text)
    olusturma_tarihi = Column(DateTime, default=datetime.utcnow)

    gelirler = relationship("Gelir", back_populates="musteri")

    def __repr__(self):
        return f"<Musteri(id={self.id}, ad='{self.ad}')>"


class Gider(Base):
    __tablename__ = "giderler"

    id = Column(Integer, primary_key=True)
    tarih = Column(Date, nullable=False)
    satici = Column(String(200), nullable=False)
    satici_vkn = Column(String(11))
    kategori_id = Column(Integer, ForeignKey("kategoriler.id"), nullable=False)
    tutar = Column(Numeric(12, 2), nullable=False)
    kdv_orani = Column(Numeric(5, 2), nullable=False)
    kdv_tutari = Column(Numeric(12, 2), nullable=False)
    toplam_tutar = Column(Numeric(12, 2), nullable=False)
    aciklama = Column(Text)
    odeme_yontemi = Column(String(30))
    fatura_no = Column(String(50))
    fatura_dosyasi = Column(String(500))
    olusturma_tarihi = Column(DateTime, default=datetime.utcnow)

    kategori = relationship("Kategori", back_populates="giderler")

    def __repr__(self):
        return f"<Gider(id={self.id}, tarih={self.tarih})>"


class Gelir(Base):
    __tablename__ = "gelirler"

    id = Column(Integer, primary_key=True)
    fatura_no = Column(String(50))
    tarih = Column(Date, nullable=False)
    musteri_id = Column(Integer, ForeignKey("musteriler.id"), nullable=False)
    kategori_id = Column(Integer, ForeignKey("kategoriler.id"), nullable=False)
    tutar = Column(Numeric(12, 2), nullable=False)
    kdv_orani = Column(Numeric(5, 2), nullable=False)
    kdv_tutari = Column(Numeric(12, 2), nullable=False)
    stopaj_orani = Column(Numeric(5, 2), default=0)
    stopaj_tutari = Column(Numeric(12, 2), default=0)
    toplam_tutar = Column(Numeric(12, 2), nullable=False)
    net_tahsilat = Column(Numeric(12, 2), nullable=False)
    aciklama = Column(Text)
    odendi = Column(Boolean, default=False)
    odeme_tarihi = Column(Date)
    olusturma_tarihi = Column(DateTime, default=datetime.utcnow)

    musteri = relationship("Musteri", back_populates="gelirler")
    kategori = relationship("Kategori", back_populates="gelirler")

    def __repr__(self):
        return f"<Gelir(id={self.id}, fatura_no='{self.fatura_no}')>"


class VergiDonemi(Base):
    __tablename__ = "vergi_donemleri"

    id = Column(Integer, primary_key=True)
    yil = Column(Integer, nullable=False)
    donem = Column(String(20), nullable=False)
    baslangic_tarihi = Column(Date, nullable=False)
    bitis_tarihi = Column(Date, nullable=False)
    toplam_gelir = Column(Numeric(14, 2), default=0)
    toplam_gider = Column(Numeric(14, 2), default=0)
    hesaplanan_kdv = Column(Numeric(12, 2), default=0)
    hesaplanan_stopaj = Column(Numeric(12, 2), default=0)
    beyanname_durumu = Column(String(20), default="hazirlaniyor")
    notlar = Column(Text)
    olusturma_tarihi = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<VergiDonemi(yil={self.yil}, donem='{self.donem}')>"
