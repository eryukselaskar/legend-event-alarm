# Legend Event Alarm

Silkroad Online etkinlikleri için Windows sistem tepsisinde çalışan alarm uygulaması. Etkinlik başlamadan 10, 5 ve 1 dakika kala bildirim + sesli alarm + ekranda küçük bir uyarı gösterir.

## İndir ve Kullan

En son sürümü [Releases](../../releases/latest) sayfasından indirin (`SilkroadEventAlarm.exe`), çift tıklayın. Kurulum gerekmez, sistem tepsisinde ikon olarak çalışır.

## Özellikler

- 10 dk / 5 dk / 1 dk kala bildirim + alarm sesi
- Ekranın ortasında küçük uyarı penceresi
- Türkçe / English dil desteği (sistem tepsisi menüsünden değiştirilir)
- Sunucu saati (UTC+3) otomatik olarak bilgisayarınızın saat dilimine çevrilir
- Bugünkü etkinlikler listesi (tray menüsünden)
- İstenmeyen etkinlikleri sessize alma
- Kendi `.wav` dosyanızı alarm sesi olarak ayarlama
- Windows ile otomatik başlatma
- Test Alarm ile bildirimleri deneme

## Kaynaktan Çalıştırma

```
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python main.py
```

## Etkinlikleri Güncelleme

`silkroad_events.json` dosyasını düzenleyerek etkinlik saatlerini/günlerini değiştirebilirsiniz.

## Lisans

MIT — bkz. [LICENSE](LICENSE)
