import snowboydecoder
# import sys
# import threading

interrupted = False
# _detector = None

# def signal_handler(signal, frame):
#     global interrupted
#     interrupted = True
#
#


def interrupt_callback():
    global interrupted
    return interrupted


# if len(sys.argv) == 1:
#     print("Error: need to specify model name")
#     print("Usage: python demo.py your.model")
#     sys.exit(-1)

# model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
# signal.signal(signal.SIGINT, signal_handler)

# def start_detector(detector, detected_callback):
#     print('Hotword is detecting...')
#     detector.start(detected_callback=detected_callback,
#                    interrupt_check=interrupt_callback,
#                    sleep_time=0.03)
#     print('Hotword detector is terminated.')
#     detector.terminate()


def start_listen(model, detected_callback):
    global interrupted
    interrupted = False

    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
    detector.start(detected_callback=detected_callback,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)
    detector.terminate()
    # p1 = threading.Thread(target=start_detector, args=(detector, detected_callback))
    # p1.start()


def stop_listen():
    global interrupted
    interrupted = True
