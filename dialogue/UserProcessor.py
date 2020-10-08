import os
import threading
import time
import random
from dialogue import Helper, Dialogflow
from dialogue import intents

logger = Helper.get_module_logger(__name__)


class UserProcessor(threading.Thread):
    def __init__(self, group=None, args=(), kwargs=None, verbose=None):
        super(UserProcessor, self).__init__()
        self.user_words = args[0]
        self.dialogue_client = args[1]
        self.running = True
        logger.debug("__init__")
        return

    def __start_dialogue(self, flac_file):
        # time.sleep(1)
        # self.dialogue_client.listen_user()
        resp = Dialogflow.send_voice(flac_file)
        # query_result = Dialogflow.__detect_intent_stream("vin-gmsx", "session1", flac_file, "zh-TW")
        logger.debug('Query text: {}'.format(resp.query_text))
        logger.debug('Detected intent: {} (confidence: {})'.format(
            resp.intent.action,
            resp.intent_detection_confidence))
        logger.debug('Fulfillment text: {}'.format(resp.fulfillment_text))

        action_module = Helper.get_module(intents.__name__, resp.action)
        # action_module = Helper.get_module("intents", resp.action)
        if action_module is not None:
            logger.debug('Found module: {}'.format(str(action_module)))
            action_module.implement_intent(self.dialogue_client, resp)
        else:
            logger.error('Cannot find module: {}'.format(resp.action))

        os.remove(flac_file)

    def run(self):
        while self.running:
            if not self.user_words.empty():
                audio_file = self.user_words.get()
                logger.debug('Getting %s: %s items in queue', str(audio_file), str(self.user_words.qsize()))
                self.__start_dialogue(audio_file)
            time.sleep(random.uniform(.01, .2))
        logger.info("terminated")
        return

    def terminate(self):
        self.running = False
        logger.warn("terminating")
