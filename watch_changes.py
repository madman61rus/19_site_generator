import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    DIRECTORYTOWATCH = "articles"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORYTOWATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            subprocess.call(['python3.5','site_generator.py'])
            print('Ok')
        elif event.event_type == 'modified':
            subprocess.call(['python3.5', 'site_generator.py'])
            print('Ok')


if __name__ == '__main__':
    w = Watcher()
    w.run()