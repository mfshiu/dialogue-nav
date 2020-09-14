import time
import logging
import queue
import signal
import HotwordListener
import HotwordProcessor
import UserListener
import UserProcessor
import threading
from DialogueClient import DialogueClient

# logger = logging.getLogger(__name__)
from Helper import get_module_logger
logger = get_module_logger(__name__)


def thread1(p3):
    p3.start_record(2)


if __name__ == '__main__':
    # import logging
    # from logging.config import fileConfig
    # fileConfig('logging.conf')

    logger.debug("__main__")
    hot_words = queue.Queue(10)

    p1 = HotwordListener.HotwordListener(args=(hot_words,))
    p3 = UserListener.UserListener(args=(hot_words,))
    p4 = UserProcessor.UserProcessor(args=(hot_words, p3))
    p1.start()
    time.sleep(1)
    p3.start()
    time.sleep(1)
    p4.start()
    time.sleep(1)

    def signal_handler(signal, frame):
        print("signal_handler")
        p1.terminate()

    signal.signal(signal.SIGINT, signal_handler)

    logger.debug("start test")
    # p1.start_listen()
    # time.sleep(5)
    # p1.stop_listen()
    # time.sleep(5)
    # for i in range(5):
    #     t = threading.Thread(target=thread1, args=(p3, ))
    #     t.start()
    #     # p3.start_record()
    #     time.sleep(1)
    # p1.start_listen()
    # time.sleep(5)
    # p1.stop_listen()
    # time.sleep(5)
    # t = threading.Thread(target=thread1, args=(p3,))
    # t.start()
    # p3.start_record()

    dc = DialogueClient.get_instance()
    dc.start()

    # time.sleep(20)
    # p1.terminate()
    # p3.terminate()
    # p4.terminate()
