"""
CRUD fonksiyonlarini test scripti.

Ornek musteri, gider ve gelir ekler, sonra listeler.
"""

import sys
from pathlib import Path
from datetime import date, timedelta

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.db.database import get_db
from src.db.crud import (
    kategori_listele,
    musteri_ekle, musteri_listele,
    gider_ekle, gider_listele,
    gelir_ekle, gelir_listele
)


def test_crud():
    """CRUD fonksiyonlarini test et."""
    
    db = get_db()
    
    try:
        print("=" * 70)
        print("YapayMusavir - CRUD Test")
        print("=" * 70)
        print()
        
        # ====================================================================
        # 1. Kategorileri listele
        # ====================================================================
        print("📋 ADIM 1: Kategoriler")
        print("-" * 70)
        
        gider_kategorileri = kategori_listele(db, tip="gider")
        gelir_kategorileri = kategori_listele(db, tip="gelir")
        
        print(f"Gider kategorileri: {len(gider_kategorileri)}")
        print(f"Gelir kategorileri: {len(gelir_kategorileri)}")
        print()
        
        # ====================================================================
        # 2. Musteri ekle
        # ====================================================================
        print("👤 ADIM 2: Musteri Ekle")
        print("-" * 70)
        
        musteri = musteri_ekle(
            db=db,
            ad="TechCorp Ltd",
            vkn_tckn="1234567890",
            email="info@techcorp.com",
            yurtdisi=False
        )
        print(f"✅ Musteri eklendi: {musteri.ad} (ID: {musteri.id})")
        print()
        
        # ====================================================================
        # 3. Gider ekle
        # ====================================================================
        print("💸 ADIM 3: Gider Ekle")
        print("-" * 70)
        
        # Yazilim kategorisini bul
        yazilim_kat = next((k for k in gider_kategorileri if "Yazilim" in k.ad), None)
        
        if yazilim_kat:
            gider = gider_ekle(
                db=db,
                tarih=date.today() - timedelta(days=5),
                satici="GitHub Inc",
                kategori_id=yazilim_kat.id,
                tutar=990.00,  # KDV haric
                kdv_orani=yazilim_kat.kdv_orani,  # Kategoriden otomatik
                aciklama="GitHub Pro yillik abonelik",
                odeme_yontemi="kredi karti"
            )
            
            print(f"✅ Gider eklendi:")
            print(f"   Satici: {gider.satici}")
            print(f"   Tutar: {gider.tutar:.2f} TL")
            print(f"   KDV (%{gider.kdv_orani}): {gider.kdv_tutari:.2f} TL")
            print(f"   Toplam: {gider.toplam_tutar:.2f} TL")
        else:
            print("⚠️  Yazilim kategorisi bulunamadi")
        print()
        
        # ====================================================================
        # 4. Gelir ekle
        # ====================================================================
        print("💰 ADIM 4: Gelir Ekle")
        print("-" * 70)
        
        # Yazilim hizmeti (yurtici) kategorisini bul
        yazilim_hizmet_kat = next(
            (k for k in gelir_kategorileri if "Yazilim Hizmeti (Yurtici)" in k.ad), 
            None
        )
        
        if yazilim_hizmet_kat:
            gelir = gelir_ekle(
                db=db,
                tarih=date.today() - timedelta(days=3),
                musteri_id=musteri.id,
                kategori_id=yazilim_hizmet_kat.id,
                tutar=15000.00,  # KDV haric
                kdv_orani=yazilim_hizmet_kat.kdv_orani,
                stopaj_orani=yazilim_hizmet_kat.stopaj_orani,
                fatura_no="2026/001",
                aciklama="Web uygulama gelistirme projesi",
                odendi=True,
                odeme_tarihi=date.today()
            )
            
            print(f"✅ Gelir eklendi:")
            print(f"   Musteri: {gelir.musteri.ad}")
            print(f"   Fatura No: {gelir.fatura_no}")
            print(f"   Tutar: {gelir.tutar:.2f} TL")
            print(f"   KDV (%{gelir.kdv_orani}): {gelir.kdv_tutari:.2f} TL")
            print(f"   Toplam: {gelir.toplam_tutar:.2f} TL")
            print(f"   Stopaj (%{gelir.stopaj_orani}): -{gelir.stopaj_tutari:.2f} TL")
            print(f"   Net Tahsilat: {gelir.net_tahsilat:.2f} TL")
        else:
            print("⚠️  Yazilim hizmeti kategorisi bulunamadi")
        print()
        
        # ====================================================================
        # 5. Listeleme
        # ====================================================================
        print("📊 ADIM 5: Listeleme ve Ozet")
        print("-" * 70)
        
        tum_giderler = gider_listele(db)
        tum_gelirler = gelir_listele(db)
        
        toplam_gider = sum(g.toplam_tutar for g in tum_giderler)
        toplam_gelir = sum(g.net_tahsilat for g in tum_gelirler)
        
        print(f"Toplam Gider Sayisi: {len(tum_giderler)}")
        print(f"Toplam Gelir Sayisi: {len(tum_gelirler)}")
        print()
        print(f"Toplam Gider Tutari: {toplam_gider:,.2f} TL")
        print(f"Toplam Net Gelir: {toplam_gelir:,.2f} TL")
        print(f"Kar/Zarar: {toplam_gelir - toplam_gider:,.2f} TL")
        print()
        
        # ====================================================================
        # 6. Musteriler
        # ====================================================================
        print("👥 ADIM 6: Tum Musteriler")
        print("-" * 70)
        
        musteriler = musteri_listele(db)
        for m in musteriler:
            print(f"  - {m.ad} (ID: {m.id})")
        
        print()
        print("=" * 70)
        print("✅ Test tamamlandi!")
        print("=" * 70)
    
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_crud()
