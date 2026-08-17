import logging
import queue
import threading
import tkinter as tk
from tkinter import filedialog

log = logging.getLogger(__name__)

DISPLAY_MS = 6000
POLL_MS = 200
WIDTH = 340
HEIGHT = 110


class PopupManager:
    """Runs a hidden Tk root on its own thread and shows small, centered,
    borderless alert windows on demand. Thread-safe via a queue."""

    def __init__(self):
        self._queue = queue.Queue()
        self._root = None
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self._thread.start()

    def show(self, title, message):
        self._queue.put((title, message))

    def ask_wav_file(self, title):
        """Blocks the calling thread; runs the file dialog on the Tk thread."""
        result = queue.Queue()

        def task():
            path = filedialog.askopenfilename(
                title=title,
                filetypes=[("WAV audio", "*.wav"), ("All files", "*.*")],
            )
            result.put(path)

        self._root.after(0, task)
        return result.get()

    def _run(self):
        try:
            self._root = tk.Tk()
            self._root.withdraw()
        except tk.TclError:
            log.exception("Failed to initialize Tk; popups disabled")
            return
        self._poll()
        self._root.mainloop()

    def _poll(self):
        try:
            while True:
                title, message = self._queue.get_nowait()
                try:
                    self._show_popup(title, message)
                except tk.TclError:
                    log.exception("Failed to show popup")
        except queue.Empty:
            pass
        self._root.after(POLL_MS, self._poll)

    def _show_popup(self, title, message):
        win = tk.Toplevel(self._root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        try:
            win.attributes("-alpha", 0.96)
        except tk.TclError:
            pass

        screen_w = win.winfo_screenwidth()
        screen_h = win.winfo_screenheight()
        x = (screen_w - WIDTH) // 2
        y = (screen_h - HEIGHT) // 2
        win.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

        frame = tk.Frame(win, bg="#1e1e28", highlightbackground="#ffc800", highlightthickness=2)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame, text=title, fg="#ffc800", bg="#1e1e28",
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(14, 4))
        tk.Label(
            frame, text=message, fg="#f2f2f2", bg="#1e1e28",
            font=("Segoe UI", 10), wraplength=WIDTH - 30, justify="center",
        ).pack(pady=(0, 10), padx=10)

        win.bind("<Button-1>", lambda e: win.destroy())
        win.after(DISPLAY_MS, win.destroy)
