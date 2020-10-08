from dialogue import snowboydecoder

# import sys
# import threading

interrupted = False
listening = False


def interrupt_callback():
    global interrupted
    return interrupted


def is_listening():
    global listening
    return listening


def start_listen(model, detected_callback):
    if is_listening():
        print('Warning: Hotword detector is listening.')
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
    global interrupted
    interrupted = True
