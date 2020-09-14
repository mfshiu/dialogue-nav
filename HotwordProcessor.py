import threading
import time
import random
import Speaker

from Helper import get_module_logger
logger = get_module_logger(__name__)


class HotwordProcessor(threading.Thread):
    def __init__(self, group=None, args=(), kwargs=None, verbose=None):
        super(HotwordProcessor, self).__init__()
        self.hot_words = args[0]
        self.hotword_callback = args[1]
        self.running = True
        logger.debug("__init__")
        return

    def run(self):
        while self.running:
            if not self.hot_words.empty():
                item = self.hot_words.get()
                print('Getting ' + str(item)
                      + ' : ' + str(self.hot_words.qsize()) + ' items in queue')

                logger.debug("__detected_hotword")
                Speaker.play_sound("./resources/where_to_go.mp3")

                self.hotword_callback(item)
                time.sleep(random.uniform(.01, .2))
        logger.info("terminated")
        return

    def terminate(self):
        self.running = False
        logger.warn("terminating")
