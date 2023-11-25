import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def on_change():
    print("Restarting waitress...")
    subprocess.run(["pkill", "-f", "waitress"])

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory or event.src_path.endswith(".py"):
            on_change()

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(MyHandler(), path=Path(".").resolve(), recursive=True)
    observer.start()

    try:
        subprocess.run(["waitress-serve", "--host=0.0.0.0", "--port=8000", "app:app"], check=True)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
