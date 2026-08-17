# Legend Event Alarm

Windows sistem tepsisinde (system tray) çalışan, Silkroad Online sunucu etkinlikleri için alarm uygulaması. Python ile yazıldı, GUI penceresi yok — sadece tray ikonu + menü.

- **GitHub (public):** https://github.com/eryukselaskar/legend-event-alarm
- **İndirilebilir exe:** https://github.com/eryukselaskar/legend-event-alarm/releases/latest
- **Durum:** Tamamlandı, yayında. Yeni istekler geldiğinde küçük iyileştirme/bugfix modunda çalışılıyor.

## Ne yapar

`silkroad_events.json` içindeki etkinlik saatlerine göre (sunucu saati UTC+3, otomatik olarak kullanıcının local saat dilimine çevrilir):

- Etkinlik başlamadan **10 dk, 5 dk ve 1 dk kala** bildirim + alarm sesi + ekranın ortasında küçük uyarı penceresi gösterir.
- Aynı tetikleme bir günde birden fazla kez çalmaz (fired-key seti ile engellenir).
- Gece yarısını geçen saatler doğru hesaplanır (bir önceki/sonraki sunucu gününü de tarar).

## Mimari / dosya haritası

```
main.py                 giriş noktası, EVENTS_PATH çözümü (PyInstaller frozen-aware)
silkroad_events.json    etkinlik verisi (isim, times, days) — server_timezone: UTC+3
app/
  config.py             %APPDATA%\SilkroadEventAlarm\config.json okuma/yazma
                         (language, autostart, muted_events, custom_sound_path)
  i18n.py                TR/EN çeviri sözlüğü, t(lang, key, **kwargs)
  events.py              JSON parse, gün eşleştirme (daily / daily_except_sunday / liste),
                         server_occurrences_near (±1 gün tarama, gece yarısı için),
                         next_upcoming_event (tray tooltip için, 1 haftaya kadar tarar),
                         todays_events_local (tray menüsü "Bugünkü Etkinlikler" için)
  scheduler.py           arka plan thread, 15 sn'de bir tick, OFFSETS=(10,5,1) dk kontrolü,
                         fired-key seti ile tekrar engelleme, get_muted() ile filtre,
                         on_tick callback (tray title güncellemesi için)
  sound.py               winsound.Beep varsayılan alarm; custom_path verilirse
                         winsound.PlaySound(...) ile kullanıcının .wav dosyasını çalar
  popup.py               PopupManager: kendi thread'inde hidden Tk root çalıştırır,
                         queue üzerinden thread-safe şekilde ekranın ortasında küçük
                         borderless/topmost uyarı penceresi gösterir (6 sn sonra kapanır);
                         ayrıca ask_wav_file() ile thread-safe dosya seçim diyaloğu sunar
  autostart.py            HKCU\...\Run registry key ile Windows başlangıcına ekle/çıkar
                         (admin gerektirmez, Task Scheduler değil registry kullanılıyor)
  icon.py                 PIL ile tray ikonunu programatik çizer (dış dosya bağımlılığı yok)
  tray.py                 TrayApp: pystray menüsü, tüm event handler'lar, _update_title()
.github/workflows/build.yml   tag push (v*) tetikler → PyInstaller ile onefile exe derler
                               → GitHub Release'e SilkroadEventAlarm.exe olarak yükler
```

## Tray menüsü içeriği

- **Bugünkü Etkinlikler** — saat sırasına göre, sessize alınanlar hariç
- **Language** — Türkçe / English (config'e kaydedilir, açılışta hatırlanır)
- **Windows ile Otomatik Başlat** — checkbox, registry Run key toggle
- **Mute Events / Etkinlikleri Sessize Al** — her etkinlik için ayrı checkbox
- **Alarm Sound / Alarm Sesi** — "Choose File..." (kullanıcı kendi .wav'ını seçer) / "Default"
- **Test Alarm** — menüden tıklanınca gerçek bir bildirim gibi tüm alarm zincirini tetikler
- **Exit / Çıkış**

Tray ikonunun üzerine gelince (tooltip) sıradaki etkinlik ve kalan süre görünür, örn:
`Silkroad Event Alarm | Next: Selketh & Neith (1h 18m)` — 15 saniyede bir güncellenir.

## Config dosyası

`%APPDATA%\SilkroadEventAlarm\config.json`:
```json
{
  "language": "en",
  "autostart": false,
  "muted_events": [],
  "custom_sound_path": null
}
```

## Geliştirme ortamı — ÖNEMLİ

Bu makinede PATH'teki `python` komutu Claude Code'un kendi ajan venv'ine
(`hermes-agent\venv`) işaret eder ve orada **pip yoktur**. Proje kendi
`.venv` klasörüne sahiptir, her zaman onu kullan:

```
.venv\Scripts\python main.py                    # çalıştır
.venv\Scripts\pip install -r requirements.txt    # bağımlılık kur
```

Bağımlılıklar: `pystray`, `plyer`, `Pillow` (bkz. `requirements.txt`).
`tkinter` stdlib ile gelir (popup penceresi için).

## Yeni sürüm yayınlama

```
git add -A && git commit -m "..."
git push origin master
git tag v1.0.x
git push origin v1.0.x
```

Tag push edilince GitHub Actions otomatik olarak Windows runner'da
`pyinstaller --onefile --windowed --name SilkroadEventAlarm --add-data "silkroad_events.json;." main.py`
komutunu çalıştırıp exe'yi Release'e ekler. Workflow'un `permissions: contents: write`
alması gerekiyor — yoksa "Resource not accessible by integration" hatası alınır (bir kere
bu hatayı yaşadık, düzeltildi).

## Etkinlik verisini güncelleme

`silkroad_events.json` düzenlenip commit/push/tag yapılırsa yeni exe otomatik bu güncel
veriyle derlenir. Format:
```json
{"name": "Etkinlik Adı", "times": ["19:30"], "days": "daily"}
```
`days`: `"daily"` | `"daily_except_sunday"` | `["friday","saturday","sunday"]` gibi liste.

## Bilinen kısıtlar / tasarım kararları

- Alarm sesi için sadece **.wav** destekleniyor (winsound.PlaySound mp3 çalamıyor,
  ekstra kütüphane eklememek için bilinçli tercih).
- `.venv/` ve `.claude/settings.local.json` `.gitignore` içinde, repoya girmez.
- Bu proje kendi bağımsız git deposuna sahip (`git init` bu klasörde ayrıca yapıldı) —
  üst dizindeki `C:\Users\Gaming\Projects` seviyesindeki büyük/karışık git deposuna
  hiç dahil değil, ondan tamamen izole.

## Konuşulan ama henüz yapılmayan fikirler

Şu an aktif bir TODO yok. Yeni istek gelirse önce bu dosyayı ve `README.md`'yi güncel tut.
