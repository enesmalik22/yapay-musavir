"""
Veritabanini ilk kez kurma scripti.

Yapilan isler:
1. Veritabani dosyasini olusturur (yoksa)
2. Tum tablolari kurar (Kategori, Musteri, Gider, Gelir, VergiDonemi)
3. JSON'dan varsayilan kategorileri yukler

Kullanim:
    python scripts/init_db.py
"""

import json
import sys
from pathlib import Path

# Proje kok dizinini Python path'ine ekle (src/ importlari icin)
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.db.database import init_db, get_db, DB_PATH
from src.db.models import Kategori


def kategorileri_yukle():
    """data/tax_rules/2026.json'dan varsayilan kategorileri DB'ye yukler."""
    
    json_path = PROJECT_ROOT / "data" / "tax_rules" / "2026.json"
    
    if not json_path.exists():
        print(f"❌ Vergi kurallari dosyasi bulunamadi: {json_path}")
        return
    
    with open(json_path, "r", encoding="utf-8") as f:
        vergi_kurallari = json.load(f)
    
    db = get_db()
    
    try:
        # Mevcut kategori var mi kontrol et
        mevcut_sayi = db.query(Kategori).count()
        if mevcut_sayi > 0:
            print(f"ℹ️  Veritabaninda zaten {mevcut_sayi} kategori var. Atlaniyor.")
            return
        
        # JSON'daki kategorileri DB'ye ekle
        eklenen = 0
        for kat_data in vergi_kurallari["varsayilan_kategoriler"]:
            kategori = Kategori(
                ad=kat_data["ad"],
                tip=kat_data["tip"],
                kdv_orani=kat_data.get("kdv_orani", 20),
                stopaj_orani=kat_data.get("stopaj_orani", 0),
                dusulebilir=kat_data.get("dusulebilir", True),
                aciklama=kat_data.get("aciklama", "")
            )
            db.add(kategori)
            eklenen += 1
        
        db.commit()
        print(f"✅ {eklenen} kategori veritabanina eklendi.")
    
    except Exception as e:
        db.rollback()
        print(f"❌ Hata: {e}")
        raise
    finally:
        db.close()


def main():
    """Ana kurulum akisi."""
    
    print("=" * 60)
    print("YapayMusavir - Veritabani Kurulumu")
    print("=" * 60)
    print()
    
    # 1. Tablolari olustur
    print("📦 Adim 1: Tablolar olusturuluyor...")
    init_db()
    print()
    
    # 2. Kategorileri yukle
    print("📥 Adim 2: Varsayilan kategoriler yukleniyor...")
    kategorileri_yukle()
    print()
    
    # 3. Ozet
    db = get_db()
    try:
        kategori_sayisi = db.query(Kategori).count()
        gider_kategori = db.query(Kategori).filter(Kategori.tip == "gider").count()
        gelir_kategori = db.query(Kategori).filter(Kategori.tip == "gelir").count()
        
        print("=" * 60)
        print("✅ Kurulum tamamlandi!")
        print(f"   Veritabani: {DB_PATH}")
        print(f"   Toplam kategori: {kategori_sayisi}")
        print(f"   - Gider kategorisi: {gider_kategori}")
        print(f"   - Gelir kategorisi: {gelir_kategori}")
        print("=" * 60)
    finally:
        db.close()


if __name__ == "__main__":
    main()
