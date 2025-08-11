import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, path, callback):
        self.path = str(Path(path).resolve())
        self.callback = callback

    def on_modified(self, event):
        event_path = str(Path(event.src_path).resolve())
        if event_path == self.path:
            self.callback()


def start_file_watcher(path, on_file_change=None):
    def on_change():
        if on_file_change:
            on_file_change()

    abs_path = str(Path(path).resolve())
    dir_path = str(Path(abs_path).parent)
    event_handler = FileChangeHandler(abs_path, on_change)
    observer = Observer()
    observer.schedule(event_handler, path=dir_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
