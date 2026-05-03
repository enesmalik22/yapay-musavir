# YapayMüşavir

Türkiye'deki freelancer'lar ve küçük işletmeler için fatura yönetimi ve vergi hazırlığı asistanı. Faturalarınızı yüklersiniz, AI okuyup kategorize eder, dönem geldiğinde tek tıkla rapor çıkarırsınız.

Tüm yapay zeka işlemleri lokal olarak çalışır — finansal verileriniz bilgisayarınızdan çıkmaz.

> **Durum:** Aktif geliştirme aşamasında. Manuel fatura girişi ve temel raporlama çalışıyor; otomatik PDF/görsel fatura okuma ve gelişmiş analiz üzerinde çalışıyorum.

## Neden bu projeyi yapıyorum

Türkiye'de 2.5 milyondan fazla freelancer var. Çoğu aylık 500-1500 TL muhasebeci ücreti ödüyor, faturalarını klasörde topluyor, beyanname dönemi panik yaşıyor. Üstelik küçük tutarlı KDV iadelerini de kaçırıyorlar.

Bu boşluğu doldurmak istedim. Aynı zamanda LangChain, lokal LLM'ler ve veri mühendisliği konularında gerçek bir uygulama geliştirmek için iyi bir fırsat oldu.

## Ne yapar

- Fatura yakalar: PDF e-faturaları yüklersin veya kasa fişini fotoğraflarsın
- AI okur: Tarih, satıcı, tutar, KDV bilgilerini otomatik çıkarır
- Kategorize eder: Vergi mevzuatına göre gider türünü belirler
- Hesaplar: KDV özeti, gelir vergisi tahmini, KDV iade hakkı
- Sorgular: "Eylül ayında yemek harcaması ne kadardı?" gibi doğal dil soruları
- Raporlar: Aylık, çeyreklik, yıllık raporlar; muhasebeciye gönderilebilir formatta export

## Nasıl çalışıyor

Yüklediğin fatura SQLite veritabanına işleniyor. Sen bir soru sorduğunda LangChain agent'ı şunları yapıyor:

1. Veritabanı şemasını okuyor
2. Soruna uygun SQL sorgusunu yazıyor
3. Sorguyu çalıştırıyor
4. Sonucu Türkçe açıklıyor ve ilgili grafiği üretiyor

LLM olarak Llama 3.1 (8B) kullanıyorum, Ollama üzerinden çalışıyor. M-serisi Mac'lerde GPU hızlandırması ile yeterince hızlı çalışıyor.

## Kurulum

Ön gereksinimler: Python 3.10+, Ollama (https://ollama.com), 8 GB+ RAM.

    git clone git@github.com:enesmalik22/yapay-musavir.git
    cd yapay-musavir

    python3 -m venv venv
    source venv/bin/activate

    pip install -r requirements.txt

    ollama pull llama3.1:8b

    cp .env.example .env

    streamlit run src/ui/app.py

İlk çalıştırmada model belleğe yüklenirken 10-30 saniye gecikme olur. Sonraki sorgular hızlıdır.

## Örnek sorular

- Eylül ayında ne kadar yemek harcaması yaptım?
- Bu çeyrekte KDV iade hakkım ne?
- En çok hangi kategoride harcıyorum?
- Ödenmemiş faturalarım hangileri?
- 2025'te kestiğim faturaların toplamı ne?

## Klasör yapısı

    src/
      ocr/             – PDF ve görsel fatura okuma
      classification/  – Vergi kategorisi belirleme
      tax_engine/      – KDV ve gelir vergisi hesaplama
      db/              – Şema ve veritabanı işlemleri
      agents/          – LangChain agent'ları
      reports/         – Rapor üretici
      ui/              – Streamlit arayüzü
    tests/             – pytest
    data/
      sample_invoices/ – Örnek anonim faturalar
      tax_rules/       – Vergi mevzuatı tanımları
    docs/              – Mimari ve API dokümanları

## Durum

- [x] Proje iskeleti ve mimari
- [ ] SQLite şema (faturalar, gelir, müşteriler, kategoriler)
- [ ] Manuel fatura girişi
- [ ] Streamlit arayüzü
- [ ] PDF e-fatura okuyucu
- [ ] LLM ile akıllı kategorizasyon
- [ ] KDV ve gelir vergisi hesaplama motoru
- [ ] Görsel fatura/fiş OCR
- [ ] Doğal dil sorgulama
- [ ] Beyanname-hazır PDF rapor
- [ ] Excel export
- [ ] Test kapsama

İşaretsiz olanlar henüz yapılmadı, ilerledikçe güncelliyorum.

## Önemli not

Bu uygulama mali müşavir yerine geçmez. Yapılan hesaplamalar tahmini niteliktedir, beyanname için resmi muhasebe danışmanlığı gereklidir. Asıl amacı muhasebecinizle iletişiminizi kolaylaştırmak ve verilerinizi düzenli tutmaktır.

## Lisans

MIT

## İletişim

Enes Ozata — enesozata0@gmail.com — [@enesmalik22](https://github.com/enesmalik22)
