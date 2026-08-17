import json
import os

CONFIG_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "SilkroadEventAlarm")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "language": "en",
    "autostart": False,
    "muted_events": [],
    "custom_sound_path": None,
}


def load_config():
    if not os.path.exists(CONFIG_PATH):
        return dict(DEFAULT_CONFIG)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        config = dict(DEFAULT_CONFIG)
        config.update(data)
        return config
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_CONFIG)


def save_config(config):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
