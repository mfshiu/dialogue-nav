import time
# import logging
import Dialogflow
import queue
import signal
import HotwordListener
import HotwordProcessor
import Information
import Speaker
import UserListener
import UserProcessor


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
            self._procs = None
            self.__destinations = []
            DialogueClient._instance = self

    def __arrived(self, key, value):
        dest = self.__destinations.pop()
        Speaker.play("您已經抵達" + dest.name)
        count = len(self.__destinations)
        if count > 0:
            next_dest = self.__destinations[count-1]
            Speaker.play("接下來我們將繼續前往" + next_dest.name)
            Speaker.play("現在開始請聽我的指示前進")
            Information.notify_destination(dest.coordinate)
        else:
            self.standby()

    def __hotword_callback(self, item):
        print("hotword_callback: " + str(item))
        self._procs[0].stop_listen()
        time.sleep(.1)
        self.listen_user()

    def __test_time(self, key, value):
        print(".", end="")

    def add_destination(self, dest):
        self.__destinations.append(dest)
        Information.notify_destination(dest.coordinate)

    def ask_user(self, words):
        Dialogflow.send_text(words)

    def get_current_destination(self):
        if len(self.__destinations) > 0:
            return self.__destinations[-1]
        else:
            return None

    def get_id(self):
        return self._id

    def get_proc(self, num):
        return self._procs[num]

    def listen_user(self):
        self._procs[2].start_record(5)

    def listen_hotword(self):
        self._procs[0].start_listen()

    def shutdown(self):
        for p in self._procs:
            p.terminate()

    def start(self):
        hot_words = queue.Queue(10)
        user_words = queue.Queue(10)

        p1 = HotwordListener.HotwordListener(args=(hot_words,))
        p2 = HotwordProcessor.HotwordProcessor(args=(hot_words, self.__hotword_callback))
        p3 = UserListener.UserListener(args=(user_words,))
        p4 = UserProcessor.UserProcessor(args=(user_words, self))
        self._procs = [p1, p2, p3, p4]

        def signal_handler(signal, frame):
            self.shutdown()

        signal.signal(signal.SIGINT, signal_handler)

        for p in self._procs:
            p.start()
            time.sleep(.5)

        Information.subscribe('sub1_arrived', self.__arrived, True)
        # Information.subscribe('time', self.__test_time)
        Information.start()

        p1.start_listen()

    def standby(self):
        Speaker.play("如果需要我的協助再呼叫我。")
        self.listen_hotword()


if __name__ == '__main__':
    DialogueClient.get_instance().start()
