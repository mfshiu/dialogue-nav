import threading
import time
import dialogue.Helper as Helper
from threading import Timer
import copy

from dialogue.Helper import get_module_logger
logger = get_module_logger(__name__)

global return_dict
return_dict = None
__information = dict()
__changed = dict()
__callbacks = dict()
__running = False
logger.debug("__init__")


def __log_timer():
    logger.debug("Information values ==>")
    for key in __information:
        value = __information[key]
        logger.debug("%20s: %s", key, str(value))
    if __running:
        Timer(5, __log_timer).start()


def __run():
    global __running
    __running = True
    Timer(3, __log_timer).start()
    while __running:
        __update_from()
        __update_to()
        time.sleep(1)

    logger.info("terminated")


def __update_from():
    callbacks = []
    global return_dict
    if return_dict is None:
        return

    # Store changed values to new_values
    dic = copy.deepcopy(return_dict)
    new_values = {}
    for key in __information:
        if key in dic:
            value = dic[key]
            if not Helper.is_equal(__information[key], value):
                new_values[key] = value

    # Append callback and update information
    for key in new_values:
        value = new_values[key]
        if key in __callbacks:
            cb = __callbacks[key]
            if 'any' == cb[1] or Helper.is_equal(value, cb[1]):
                callbacks.append((cb[0], key, value))
        logger.debug("Information is changed. Key: %s, %s -> %s"
                     % (key, str(__information[key]), str(value)))
        __information[key] = value

    # Raise callback
    for c in callbacks:
        c[0](c[1], c[2])


def __update_to():
    global return_dict
    for key in __changed:
        try:
            return_dict[key] = __changed[key]
        except:
            logger.error("Update return_dict error, key: %s, new value: %s",
                         key, str(__changed[key]))
    __changed.clear()


def get_indoor_destination():
    return get_information("sub4_destination")


def get_location():
    # return 25.0230239, 121.2210628
    result = None
    if "location" in __information:
        loc = __information["location"]
        if not loc is None:
            result = __information["location"][0]
    return result


def get_outdoor_destination():
    return get_information("sub1_destination")


def get_information(name):
    try:
        if name in __information:
            return __information[name]
        else:
            return None
    except:
        logger.error("get_information error. name: %s", name)


def is_indoor():
    return get_information("in_outdoor_status")


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
    set_information('sub4_destination', dest)
    set_information('sub4_arrived', False)


def stop_indoor_destination():
    set_information('sub4_destination', None)
    set_information('sub4_arrived', True)


def set_outdoor_destination(coordinate, dest_type):
    set_information('sub1_destination', (coordinate[0], coordinate[1], dest_type))
    set_information('sub1_arrived', False)


def set_user_speaking(is_speaking):
    set_information('user_speaking', is_speaking)


def stop_outdoor_destination():
    set_information('sub1_destination', None)
    set_information('sub1_arrived', True)


def set_indoor_kanbans(kanbans):
    set_information("kanban_indoor", kanbans)


def set_information(name, value):
    try:
        __information[name] = value
        __changed[name] = value
    except:
        logger.error("set_information error. name: %s, value: %s", name, str(value))


def start(source_return_dict):
    global return_dict
    return_dict = source_return_dict

    set_information('awakable', True)
    set_information('in_outdoor_status', True)
    set_information('kanban_indoor', None)
    set_information('location', None)
    set_information('sub1_arrived', True)
    set_information('sub1_destination', None)
    set_information('sub4_arrived', True)
    set_information('sub4_destination', None)
    set_information('user_speaking', False)

    t = threading.Thread(target=__run)
    t.start()


def subscribe(name, callback, value="any"):
    __callbacks[name] = (callback, value)
    logger.debug("subscribe(name=%s, callback", name)


def terminate():
    global __running
    __running = False
    logger.warn("terminating")
