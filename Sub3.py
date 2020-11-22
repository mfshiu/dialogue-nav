import threading
from dialogue import Helper
import signal
import time
import json
from dialogue.DialogueClient import DialogueClient
# from multiprocessing import Manager
# from dialogue.Sub1 import Sub1
from dialogue.Sub4 import Sub4
from dialogue import Information
from sub1_api import Sub1_api


logger = Helper.get_module_logger(__name__)


class Sub3(threading.Thread):
    def __init__(self, sub1, is_simulation=False):
        super(Sub3, self).__init__()
        logger.debug("__init__")

        Information.set_sub1(sub1)
        self.dialogue_client = DialogueClient.get_instance()
        self.running = True
        self.is_simulation = is_simulation
        self.sub4 = None

    def is_speaking(self):
        return Information.is_user_speaking()

    def run(self):
        self.dialogue_client.start()

        # if self.is_simulation:
        #     self.sub1 = Sub1()
        #     self.sub1.start()
        self.sub4 = Sub4(self.is_simulation)
        self.sub4.start()

        while self.running:
            if self.dialogue_client.is_terminated:
                self.terminate()
            time.sleep(1)
        if not self.dialogue_client.is_terminated:
            self.dialogue_client.shutdown()
        logger.info("terminated")
        return

    def update_kanbans(self, kanbans):
        Information.set_indoor_kanbans(json.loads(kanbans))

    def terminate(self):
        self.running = False
        self.sub4.terminate()
        # if self.is_simulation:
        #     self.sub1.terminate()
        logger.warning("terminating")


if __name__ == '__main__':
    # manager = Manager()
    # sub3 = Sub3(manager.dict(), is_simulation=False)
    sub3 = Sub3(Sub1_api(), is_simulation=True)

    def signal_handler(signal, frame):
        sub3.terminate()
    signal.signal(signal.SIGINT, signal_handler)

    sub3.start()

    def shutdown():
        sub3.terminate()

    # threading.Timer(5, shutdown).start()


