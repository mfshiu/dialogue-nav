from dialogue import snowboydecoder

from dialogue.Helper import get_module_logger
logger = get_module_logger(__name__)

interrupted = False
listening = False


def interrupt_callback():
    global interrupted
    return interrupted


def is_listening():
    global listening
    return listening


def start_listen(model, detected_callback):
    logger.info("Start listen")
    if is_listening():
        logger.warning('Hotword detector is listening.')
        return

    global interrupted
    interrupted = False
    global listening
    listening = True

    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
    detector.start(detected_callback=detected_callback,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

    detector.terminate()
    listening = False
    print('Hotword detector is terminated.')
    # p1 = threading.Thread(target=start_detector, args=(detector, detected_callback))
    # p1.start()


def stop_listen():
    logger.debug("Stop listen")
    global interrupted
    interrupted = True
