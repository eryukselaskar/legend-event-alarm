import os
import winsound


def play_alarm_beep(custom_path=None):
    if custom_path and os.path.isfile(custom_path):
        try:
            winsound.PlaySound(custom_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            return
        except RuntimeError:
            pass
    for _ in range(3):
        winsound.Beep(1046, 250)
