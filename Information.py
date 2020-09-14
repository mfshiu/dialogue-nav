import threading
import time

from Helper import get_module_logger
logger = get_module_logger(__name__)

__source = dict()
__information = dict()
__callbacks = dict()
global __running
__running = False
logger.debug("__init__")


def __read_source():
    __source['gps'] = (25.0230239, 121.2210628)
    __source['time'] = time.process_time()
    return __source


def __run():
    global __running
    __running = True
    while __running:
        __update()
        time.sleep(1)

    logger.info("terminated")


def __update():
    callbacks = []

    source = __read_source()
    for key, value in source.items():
        if key not in __information or __information[key] != value:
            if key in __callbacks:
                cb = __callbacks[key]
                if 'any' == cb[1] or value == cb[1]:
                    callbacks.append((cb[0], key, value))
            __information[key] = value

    for c in callbacks:
        c[0](c[1], c[2])


def get_info(name):
    return __information[name]


def __set_info(name, value):
    __information[name] = value


def __test_walk():
    time.sleep(50)
    __source['sub1_arrived'] = True


def notify_destination(coordinate):
    __set_info('sub1_destination', coordinate)
    __set_info('sub1_arrived', False)

    # Test, arrived after 10 sesonds
    t = threading.Thread(target=__test_walk)
    t.start()


def start():
    t = threading.Thread(target=__run)
    t.start()


def subscribe(name, callback, value="any"):
    __callbacks[name] = (callback, value)
    logger.debug("subscribe(name, callback")


def terminate():
    global __running
    __running = False
    logger.warn("terminating")
