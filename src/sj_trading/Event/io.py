import threading

def start_io(closeEvent: threading.Event):
    while (1):
        closeEvent.wait(timeout=0.1)
        if closeEvent:
            break