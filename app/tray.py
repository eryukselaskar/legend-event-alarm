from datetime import datetime, timezone

import pystray
from plyer import notification

from . import autostart
from . import events as events_mod
from .config import load_config, save_config
from .i18n import t
from .icon import make_icon_image
from .popup import PopupManager
from .scheduler import Scheduler
from .sound import play_alarm_beep


class TrayApp:
    def __init__(self, events):
        self.events = events
        self.config = load_config()
        self.icon = pystray.Icon(
            "SilkroadEventAlarm",
            make_icon_image(),
            t(self.config["language"], "app_title"),
        )
        self.icon.menu = pystray.Menu(lambda: self._build_menu())
        self.popup = PopupManager()
        self.scheduler = Scheduler(
            self.events,
            lambda: self.config["language"],
            self._notify,
            get_muted=lambda: set(self.config["muted_events"]),
            on_tick=self._update_title,
        )

    def _language(self):
        return self.config["language"]

    def _notify(self, title, message):
        notification.notify(title=title, message=message, app_name=title, timeout=10)
        self.popup.show(title, message)
        play_alarm_beep(self.config.get("custom_sound_path"))

    def _today_event_items(self):
        now_server = datetime.now(timezone.utc).astimezone(events_mod.SERVER_TZ)
        muted = set(self.config["muted_events"])
        today = events_mod.todays_events_local(self.events, now_server, muted)
        if not today:
            return [pystray.MenuItem(t(self._language(), "no_events_today"), None, enabled=False)]
        return [
            pystray.MenuItem(f"{local_dt.strftime('%H:%M')}  {name}", None, enabled=False)
            for local_dt, name in today
        ]

    def _mute_event_items(self):
        muted = set(self.config["muted_events"])

        def make_handler(name):
            def handler(icon, item):
                muted = set(self.config["muted_events"])
                muted.symmetric_difference_update({name})
                self.config["muted_events"] = sorted(muted)
                save_config(self.config)
            return handler

        return [
            pystray.MenuItem(
                event["name"], make_handler(event["name"]),
                checked=lambda item, n=event["name"]: n not in set(self.config["muted_events"]),
            )
            for event in self.events
        ]

    def _set_language(self, lang):
        def handler(icon, item):
            self.config["language"] = lang
            save_config(self.config)
            self._update_title()
        return handler

    def _test_alarm(self, icon, item):
        lang = self._language()
        self._notify(t(lang, "app_title"), t(lang, "test_alarm_message"))

    def _choose_sound(self, icon, item):
        path = self.popup.ask_wav_file(t(self._language(), "menu_choose_sound"))
        if path:
            self.config["custom_sound_path"] = path
            save_config(self.config)

    def _use_default_sound(self, icon, item):
        self.config["custom_sound_path"] = None
        save_config(self.config)

    def _toggle_autostart(self, icon, item):
        enabled = not autostart.is_enabled()
        autostart.set_enabled(enabled)
        self.config["autostart"] = enabled
        save_config(self.config)

    def _update_title(self):
        lang = self._language()
        muted = set(self.config["muted_events"])
        now_utc = datetime.now(timezone.utc)
        upcoming = events_mod.next_upcoming_event(self.events, now_utc, muted)
        if upcoming:
            name, event_dt = upcoming
            minutes_left = int((event_dt - now_utc).total_seconds() // 60)
            if minutes_left < 60:
                remaining = f"{minutes_left}m"
            elif minutes_left < 1440:
                hours, minutes = divmod(minutes_left, 60)
                remaining = f"{hours}h {minutes}m"
            else:
                remaining = f"{minutes_left // 1440}d"
            title = f"{t(lang, 'app_title')} | {t(lang, 'tray_next')}: {name} ({remaining})"
        else:
            title = t(lang, "app_title")
        self.icon.title = title[:128]

    def _exit(self, icon, item):
        self.scheduler.stop()
        icon.stop()

    def _build_menu(self):
        lang = self._language()
        return pystray.Menu(
            pystray.MenuItem(t(lang, "menu_today"), pystray.Menu(*self._today_event_items())),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                t(lang, "menu_language"),
                pystray.Menu(
                    pystray.MenuItem(
                        t(lang, "menu_turkish"),
                        self._set_language("tr"),
                        checked=lambda item: self._language() == "tr",
                        radio=True,
                    ),
                    pystray.MenuItem(
                        t(lang, "menu_english"),
                        self._set_language("en"),
                        checked=lambda item: self._language() == "en",
                        radio=True,
                    ),
                ),
            ),
            pystray.MenuItem(
                t(lang, "menu_autostart"),
                self._toggle_autostart,
                checked=lambda item: autostart.is_enabled(),
            ),
            pystray.MenuItem(t(lang, "menu_mute_events"), pystray.Menu(*self._mute_event_items())),
            pystray.MenuItem(
                t(lang, "menu_alarm_sound"),
                pystray.Menu(
                    pystray.MenuItem(t(lang, "menu_choose_sound"), self._choose_sound),
                    pystray.MenuItem(
                        t(lang, "menu_default_sound"),
                        self._use_default_sound,
                        checked=lambda item: not self.config.get("custom_sound_path"),
                        radio=True,
                    ),
                ),
            ),
            pystray.MenuItem(t(lang, "menu_test_alarm"), self._test_alarm),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(t(lang, "menu_exit"), self._exit),
        )

    def run(self):
        self.config["autostart"] = autostart.is_enabled()
        self.popup.start()
        self._update_title()
        self.scheduler.start()
        self.icon.run()
