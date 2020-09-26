import Dialogflow
import queue
import signal
import Information
from Sub1 import Sub1
from Sub4 import Sub4
import Speaker
import UserListener
import UserProcessor

from Helper import get_module_logger
logger = get_module_logger(__name__)


class DialogueClient:
    _instance = None

    @staticmethod
    def get_instance():
        if DialogueClient._instance is None:
            DialogueClient()
        return DialogueClient._instance

    def __init__(self):
        if DialogueClient._instance is not None:
            raise Exception('only one instance can exist')
        else:
            self._id = id(self)
            self._user_listener = None
            self._user_processor = None
            self.user_words = queue.Queue(10)
            self.destinations = []
            self.sub1 = None
            self.sub4 = None
            DialogueClient._instance = self

    def __arrived_outdoor(self, key, value):
        if len(self.destinations) == 0:
            return

        dest = self.destinations.pop()
        Speaker.play("您已經抵達" + dest.name)
        count = len(self.destinations)
        if count > 0:
            next_dest = self.destinations[count - 1]
            Speaker.play("接下來我們將繼續前往" + next_dest.name)
            Speaker.play("現在開始請聽我的指示前進")
            Information.set_outdoor_destination(next_dest.coordinate)
        else:
            Speaker.play("您已經在室內")
            Information.set_return_dict("in_outdoor_status", True)
            self.standby()

    def __arrived_indoor(self, key, value):
        if Information.get_indoor_destination() is None:
            return
        # Speaker.play("您已經抵達" + dest.name)
        self.standby()

    def add_destination(self, dest):
        self.destinations.append(dest)
        Information.set_outdoor_destination(dest.coordinate)

    def ask_user(self, words):
        Dialogflow.send_text(words)

    def get_current_destination(self):
        if len(self.destinations) > 0:
            return self.destinations[-1]
        else:
            return None

    def get_id(self):
        return self._id

    def listen_user(self):
        self._user_listener.listen()

    def shutdown(self):
        self.sub4.terminate()
        self.sub1.terminate()
        Information.terminate()
        self._user_processor.terminate()
        self._user_listener.terminate()

    def start(self):
        self._user_listener = UserListener.UserListener(args=(self.user_words,))
        self._user_listener.start()

        self._user_processor = UserProcessor.UserProcessor(args=(self.user_words, self))
        self._user_processor.start()

        Information.subscribe('sub1_arrived', self.__arrived_outdoor, True)
        Information.subscribe('sub4_arrived', self.__arrived_indoor, True)
        Information.start()

        self.sub1 = Sub1()
        self.sub1.start()
        self.sub4 = Sub4()
        self.sub4.start()

        def signal_handler(signal, frame):
            self.shutdown()
        signal.signal(signal.SIGINT, signal_handler)

    def standby(self):
        logger.info("Standby")
        Speaker.play_async("如果需要我的協助再呼叫我。")
        self._user_listener.listen_hotword()


if __name__ == '__main__':
    DialogueClient.get_instance().start()
