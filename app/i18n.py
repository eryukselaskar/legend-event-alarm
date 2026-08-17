TRANSLATIONS = {
    "en": {
        "app_title": "Silkroad Event Alarm",
        "notify_10": "{name} starts in 10 minutes",
        "notify_5": "5 minutes left until {name}",
        "notify_1": "1 minute left until {name}",
        "menu_today": "Today's Events",
        "menu_language": "Language",
        "menu_turkish": "Türkçe",
        "menu_english": "English",
        "menu_autostart": "Start with Windows",
        "menu_test_alarm": "Test Alarm",
        "menu_mute_events": "Mute Events",
        "menu_alarm_sound": "Alarm Sound",
        "menu_choose_sound": "Choose File...",
        "menu_default_sound": "Default",
        "menu_exit": "Exit",
        "no_events_today": "No events today",
        "test_alarm_message": "This is a test alarm",
        "tray_next": "Next",
    },
    "tr": {
        "app_title": "Silkroad Event Alarm",
        "notify_10": "{name} 10 dakika sonra başlıyor",
        "notify_5": "{name} için 5 dakika kaldı",
        "notify_1": "{name} için 1 dakika kaldı",
        "menu_today": "Bugünkü Etkinlikler",
        "menu_language": "Dil",
        "menu_turkish": "Türkçe",
        "menu_english": "English",
        "menu_autostart": "Windows ile Otomatik Başlat",
        "menu_test_alarm": "Test Alarm",
        "menu_mute_events": "Etkinlikleri Sessize Al",
        "menu_alarm_sound": "Alarm Sesi",
        "menu_choose_sound": "Dosya Seç...",
        "menu_default_sound": "Varsayılan",
        "menu_exit": "Çıkış",
        "no_events_today": "Bugün etkinlik yok",
        "test_alarm_message": "Bu bir test alarmıdır",
        "tray_next": "Sıradaki",
    },
}


def t(lang, key, **kwargs):
    lang = lang if lang in TRANSLATIONS else "en"
    text = TRANSLATIONS[lang].get(key, key)
    return text.format(**kwargs) if kwargs else text
