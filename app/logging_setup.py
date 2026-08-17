import logging
import os
import sys
import threading

from .config import CONFIG_DIR

LOG_PATH = os.path.join(CONFIG_DIR, "app.log")


def setup_logging():
    """Frozen --windowed builds have no console (sys.stdout/stderr are None),
    so uncaught exceptions normally vanish silently. Log everything to a file
    instead, and hook both the main thread and background threads."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(threadName)s %(name)s: %(message)s",
    )

    def log_unhandled(exc_type, exc_value, exc_tb):
        logging.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_tb))

    def log_thread_unhandled(args):
        logging.critical(
            "Unhandled exception in thread %s",
            args.thread.name if args.thread else "?",
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
        )

    sys.excepthook = log_unhandled
    threading.excepthook = log_thread_unhandled
