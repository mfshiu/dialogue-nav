import threading
import time

from dialogue.Helper import get_module_logger
logger = get_module_logger(__name__)

return_dict = dict()
__information = dict()
__callbacks = dict()
__running = False
logger.debug("__init__")


def __run():
    global __running
    __running = True
    while __running:
        __update()
        time.sleep(1)

    logger.info("terminated")


def __update():
    callbacks = []
    for key, value in return_dict.items():
        if key not in __information or __information[key] != value:
            if key in __callbacks:
                cb = __callbacks[key]
                if 'any' == cb[1] or value == cb[1]:
                    callbacks.append((cb[0], key, value))
            __information[key] = value

    for c in callbacks:
        c[0](c[1], c[2])


def get_indoor_destination():
    return get_return_dict("sub4_destination")


def get_outdoor_destination():
    return get_return_dict("sub1_destination")


def get_info(name):
    return __information[name]


def get_return_dict(name):
    return return_dict[name]


def is_indoor():
    return get_return_dict("in_outdoor_status")


def get_indoor_destination_text(name):
    names = {
        "exit_sign": "出口",
        "wc_sign": "廁所",
        "dangerous_sign": "危險",
        "elev_sign": "電梯",
        "sign": "",
        "platform": "月台",
    }
    if name in names:
        return names[name]
    else:
        return "不明"


def parse_indoor_destination(destination_name):
    names = {
        "出口": "exit_sign",
        "廁所": "wc_sign",
        "危險": "dangerous_sign",
        "電梯": "elev_sign",
        "月台": "platform",
    }
    if destination_name in names:
        return names[destination_name]
    else:
        return None


def set_indoor_destination(dest):
    set_return_dict('sub4_destination', dest)
    set_return_dict('sub4_arrived', False)


def stop_indoor_destination():
    set_return_dict('sub4_destination', None)
    set_return_dict('sub4_arrived', True)


def set_outdoor_destination(coordinate):
    set_return_dict('sub1_destination', coordinate)
    set_return_dict('sub1_arrived', False)


def stop_outdoor_destination():
    set_return_dict('sub1_destination', None)
    set_return_dict('sub1_arrived', True)


def set_return_dict(name, value):
    return_dict[name] = value


def start():
    # init return_dict
    set_return_dict('sub1_destination', (0, 0))
    set_return_dict('sub1_arrived', True)
    set_return_dict('sub4_destination', None)
    set_return_dict('sub4_arrived', True)
    set_return_dict('in_outdoor_status', False)

    t = threading.Thread(target=__run)
    t.start()


def subscribe(name, callback, value="any"):
    __callbacks[name] = (callback, value)
    logger.debug("subscribe(name, callback")


def terminate():
    global __running
    __running = False
    logger.warn("terminating")