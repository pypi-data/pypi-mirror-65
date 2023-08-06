import logging
from queue import Queue
from threading import Thread


class UILoop:
    def __init__(self):
        self.queue = Queue(32)
        pass

    def add_event(self, fun, args=()):
        logging.info("add event")
        if fun is not None:
            self.queue.put((fun, args))

    def pop_event(self):
        while True:
            try:
                logging.info("deal with event")
                val = self.queue.get(True)
                val[0](*val[1])
            except KeyboardInterrupt:
                logging.info("ui loop stop")
            finally:
                del val

    def run(self):
        loop = Thread(target=self.pop_event)
        loop.setDaemon(True)
        loop.start()
