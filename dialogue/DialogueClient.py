import queue
from dialogue import Speaker, UserListener, Information, UserProcessor, Dialogflow, NavHelper

from dialogue.Helper import get_module_logger
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
            self.is_terminated = True
            self.user_words = queue.Queue(10)
            self.destinations = []
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
            Information.set_indoor(True)
            self.standby(True)

    def __arrived_indoor(self, key, value):
        if Information.get_indoor_destination() is None:
            return
        # Speaker.play("您已經抵達" + dest.name)
        self.standby(True)

    def add_destination(self, dest):
        self.destinations.append(dest)
        dest_type = NavHelper.parse_destination_type(dest.name)
        Information.set_outdoor_destination(dest.coordinate, dest_type)

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
        Speaker.play("我會想你的")
        Information.terminate()
        self._user_processor.terminate()
        self._user_listener.terminate()
        self.is_terminated = True

    def start(self):
        Speaker.play_async("HI，我叫小美，你好。")

        self._user_listener = UserListener.UserListener(args=(self.user_words,))
        self._user_listener.start()

        self._user_processor = UserProcessor.UserProcessor(args=(self.user_words, self))
        self._user_processor.start()

        Information.subscribe('sub1_arrived', self.__arrived_outdoor, True)
        Information.subscribe('sub4_arrived', self.__arrived_indoor, True)
        Information.start()

        self.is_terminated = False
        # Speaker.play_async("歡迎使用視障者的智慧伙伴，我叫小美，請呼叫我的名字，我可以帶你去想去的地方。")

    def standby(self, prompt=False):
        logger.info("Standby")
        if prompt:
            Speaker.play_async("如果需要協助再呼叫我。")
        self._user_listener.listen_hotword()


if __name__ == '__main__':
    DialogueClient.get_instance().start()
