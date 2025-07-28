# YouTube Transcript Extractor

Bu proje, YouTube videolarından altyazı çıkarmak ve temiz, zamanlı transkriptler oluşturmak için iki farklı araç sunar.

## 🚀 Özellikler

- YouTube videolarından otomatik altyazı indirme
- VTT dosyalarını temizleyip timestamp'li transkript oluşturma  
- HTML etiketlerini ve gereksiz karakterleri temizleme
- Çoklu dil desteği
- Bot korumasına karşı çözümler
- Yerel VTT dosyaları ile çalışma imkanı

## 📁 Dosyalar

1. **`youtube_transcript_extractor.py`** - Ana YouTube altyazı çıkarıcı
2. **`local_transcript_processor.py`** - Yerel VTT dosyası işleyici
3. **`sample_transcript.vtt`** - Örnek VTT dosyası
4. **`requirements.txt`** - Gerekli Python paketleri

## 🛠️ Kurulum

```bash
# Gerekli paketleri yükle
pip install -r requirements.txt

# Alternatif (sistem paketleri ile)
pip install --break-system-packages yt-dlp
```

## 📝 Kullanım

### 1. YouTube'dan Doğrudan İndirme

```bash
# Basit kullanım
python3 youtube_transcript_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Browser cookies ile (bot koruması için)
python3 youtube_transcript_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID" --cookies

# Test videoları ile deneme
python3 youtube_transcript_extractor.py --test
```

### 2. Yerel VTT Dosyası İşleme

```bash
# Belirli VTT dosyası
python3 local_transcript_processor.py sample_transcript.vtt

# Mevcut dizindeki VTT dosyalarını ara
python3 local_transcript_processor.py
```

### 3. Python Kodu İçinde Kullanım

```python
from youtube_transcript_extractor import generate_transcript_with_time

# YouTube URL ile
generate_transcript_with_time("https://www.youtube.com/watch?v=VIDEO_ID")

# Cookies ile
generate_transcript_with_time("https://www.youtube.com/watch?v=VIDEO_ID", use_cookies=True)
```

## 🔧 İşleyiş

1. **İndirme**: YouTube'dan VTT formatında altyazı indirir
2. **Temizleme**: HTML etiketleri, gereksiz karakterler ve tekrarları kaldırır
3. **Formatlama**: `[timestamp] metin` formatında düzenler
4. **Kaydetme**: `timestamped_transcript.txt` dosyasına kaydeder

## 📊 Çıktı Formatı

```
[00:00:00,160 --> 00:00:02,230] I paid the best builders in Minecraft to
[00:00:02,240 --> 00:00:03,750] build some of the coolest things you
[00:00:03,760 --> 00:00:06,150] have ever seen and to hide secret rooms
```

## ⚠️ Sorun Giderme

### YouTube Bot Koruması
Eğer "Sign in to confirm you're not a bot" hatası alıyorsanız:

1. **Cookies kullanın**:
   ```bash
   python3 youtube_transcript_extractor.py "URL" --cookies
   ```

2. **Farklı videolar deneyin**:
   - Daha eski videolar
   - Daha popüler videolar
   - Eğitim kanallarından videolar

3. **Yerel VTT kullanın**:
   - Manuel olarak VTT dosyası indirin
   - `local_transcript_processor.py` kullanın

### VTT Dosyası Bulunamadı
- Video'da altyazı olmayabilir
- Farklı dil kodu deneyin (`tr`, `es`, vb.)
- Otomatik altyazı açık olup olmadığını kontrol edin

## 🌐 Dil Desteği

```python
# Türkçe altyazı
generate_transcript_with_time(url, lang="tr")

# İspanyolca altyazı  
generate_transcript_with_time(url, lang="es")

# Fransızca altyazı
generate_transcript_with_time(url, lang="fr")
```

## 📈 Örnek Kullanım Senaryoları

- **Eğitim**: Video derslerden not çıkarma
- **Araştırma**: Konuşma analizı
- **Çeviri**: Farklı dillerde içerik çevirisi
- **Erişebilirlik**: İşitme engelli kullanıcılar için
- **SEO**: Video içerik optimizasyonu

## 🔒 Yasal Uyarı

Bu araç sadece kişisel ve eğitim amaçlı kullanım içindir. YouTube'un kullanım şartlarına uygun olarak kullanın. Telif hakkı bulunan içerikleri uygun izinler olmadan kullanmayın.

## 📞 Destek

Sorunlar için:
1. GitHub Issues kullanın
2. yt-dlp dokümantasyonunu kontrol edin
3. YouTube'un güncel bot koruma politikalarını takip edin

## 📜 Lisans

Bu proje eğitim amaçlı oluşturulmuştur. Kullanırken YouTube ve yt-dlp lisanslarına uygun hareket edin.

---

**Not**: YouTube'un bot koruma sistemleri sürekli güncelleniyor. Bazen manuel çözümler gerekebilir.