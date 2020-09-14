import threading
import HotWord
import time

from Helper import get_module_logger
logger = get_module_logger(__name__)


class HotwordListener(threading.Thread):

    def __init__(self, group=None, args=(), kwargs=None, verbose=None):
        super(HotwordListener, self).__init__()
        self.hot_words = args[0]
        self.running = False
        self.listening = False
        logger.debug("__init__")

    def __detected_hotword(self):
        self.hot_words.put("mei-" + str(time.process_time()))

    def run(self):
        self.running = True
        while self.running:
            if self.listening:
                self.listening = False
                logger.info("Begin listening hot word")
                HotWord.start_listen("resources/models/mei.pmdl", self.__detected_hotword)
                logger.info("End listening hot word")
            time.sleep(.1)
        logger.info("terminated")

    def start_listen(self):
        logger.debug("start_listen")
        self.listening = True

    def stop_listen(self):
        logger.warning("stop_listen")
        HotWord.stop_listen()

    def terminate(self):
        HotWord.stop_listen()
        self.running = False
        logger.warn("terminating")
