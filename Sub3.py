import threading
from dialogue import Helper
import signal
import time
from dialogue.DialogueClient import DialogueClient
from multiprocessing import Manager

logger = Helper.get_module_logger(__name__)


class Sub3(threading.Thread):
    def __init__(self, return_dict):
        super(Sub3, self).__init__()
        logger.debug("__init__")
        self.return_dict = return_dict
        self.dialogue_client = DialogueClient.get_instance()
        self.running = True
        return

    def run(self):
        self.dialogue_client.start(self.return_dict)
        while self.running:
            if self.dialogue_client.is_terminated:
                self.terminate()
            time.sleep(1)
        if not self.dialogue_client.is_terminated:
            self.dialogue_client.shutdown()
        logger.info("terminated")
        return

    def terminate(self):
        self.running = False
        logger.warn("terminating")


if __name__ == '__main__':
    manager = Manager()
    return_dict = manager.dict()
    sub3 = Sub3(return_dict)

    def signal_handler(signal, frame):
        sub3.terminate()
    signal.signal(signal.SIGINT, signal_handler)

    sub3.start()

    def shutdown():
        sub3.terminate()

    # threading.Timer(5, shutdown).start()


