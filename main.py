import os
import sys

BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.events import load_events
from app.tray import TrayApp

EVENTS_PATH = os.path.join(BASE_DIR, "silkroad_events.json")


def main():
    events = load_events(EVENTS_PATH)
    app = TrayApp(events)
    app.run()


if __name__ == "__main__":
    main()
