Windows'ta çalışan, sistem tepsisinde (system tray) yaşayan bir Silkroad Online event alarm uygulaması yapmak istiyorum.

Gereksinimler:

* Python kullan (pystray + plyer veya winsound ile bildirim/ses)
* Ekteki silkroad\_events.json dosyasını events datası olarak kullan (server saati UTC+3)
* Uygulama, bilgisayarın kendi saat dilimini otomatik algılayıp UTC+3'e çevirerek doğru zamanda alarm çalsın

Bildirim zamanlaması (her event için üç ayrı bildirim):

* Event başlamadan 10 dakika önce: "X starts in 10 minutes" (bildirim + kısa alarm sesi)
* Event başlamadan 5 dakika önce: "5 minutes left until X" (bildirim + kısa alarm sesi)
* Event tam başladığı anda: "X has started" (bildirim + alarm sesi)

Dil desteği:

* Uygulamanın varsayılan dili İngilizce olsun
* Sistem tepsisi menüsünden Türkçe / English seçilebilsin (Language submenu)
* Seçilen dil bir ayar dosyasına (config.json veya settings.json) kaydedilsin, uygulama kapanıp açılınca hatırlansın
* Türkçe metinler için örnek:

  * "X 10 dakika sonra başlıyor"
  * "X için 5 dakika kaldı"
  * "X başladı"

"days" alanına göre tekrar mantığı:

* "daily" -> her gün
* "daily\_except\_sunday" -> Pazar hariç her gün
* \["friday","saturday","sunday"] gibi liste -> sadece o günler

Sistem tepsisi menüsü şunları içersin:

* Bugünkü eventler (liste halinde, saat sırasına göre)
* Language (Türkçe / English)
* Windows ile otomatik başlat (checkbox/toggle - açık/kapalı durumu görünsün, tıklanınca Task Scheduler veya startup klasörü kaydını otomatik oluştursun/kaldırsın)
* Çıkış / Exit

Diğer teknik detaylar:

* Basit bir ana pencere GUI şart değil, sistem tepsisi yeterli
* Alarm sesi için winsound.Beep kullan veya basit gömülü bir .wav ile yap, dışarıdan dosya bağımlılığı olmasın
* Aynı bildirimin (10dk/5dk/0dk) bir event için günde birden fazla kez tekrar tekrar gönderilmemesine dikkat et (her tetiklenme sadece bir kez çalışsın)
* Gece yarısını geçen saatler (örn. 22:00, 23:00 gibi eventlerin 10/5 dakika öncesi hesaplamaları) ve saat dilimi dönüşümü dikkatli test edilsin
* Kod sağlam ve hatasız çalışsın, config dosyası (dil + otomatik başlatma tercihi) kullanıcı klasöründe saklansın

