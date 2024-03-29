import os
import threading
import time
import dialogue.Helper as Helper
from threading import Timer
from dialogue.Helper import get_module_logger
logger = get_module_logger(__name__)

# global return_dict
# return_dict = None
__information = dict()
__callbacks = dict()
__locations = dict()
__running = False
__sub1 = None

logger.debug("__init__")


def __log_timer():
    logger.debug("Information values ==>")
    for key in __information:
        value = __information[key]
        logger.debug("%20s: %s", key, str(value))
    if __running:
        Timer(5, __log_timer).start()


def __user_not_speaking_count_timer():
    if __information['user_not_speaking_countdown'] > 0:
        __information['user_not_speaking_countdown'] -= 1
        if __information['user_not_speaking_countdown'] == 0:
            __set_user_speaking(False)

    if __running:
        Timer(1, __user_not_speaking_count_timer).start()


def __run():
    global __running
    __running = True
    Timer(3, __log_timer).start()
    Timer(1, __user_not_speaking_count_timer).start()
    while __running:
        __do_subscribe()
        time.sleep(1)

    logger.info("terminated")


def __check_callback(key, old_value, new_value):
    if key in __callbacks:
        if not Helper.is_equal(old_value, new_value):
            if key in __callbacks:
                cb = __callbacks[key]
                callback = cb[0]
                target_value = cb[1]
                if 'any' == target_value or Helper.is_equal(new_value, target_value):
                    callback(key, new_value)
            else:
                logger.error("No %s callback to run.", key)


def __do_subscribe():
    # old_value = __information["sub1_arrived"]
    old_value = __information["sub1_destination"] is None
    new_value = __sub1.is_arrived()
    __check_callback("sub1_arrived", old_value, new_value)
    # if not Helper.is_equal(old_value, new_value):
    #     if new_value:
    #         set_information("sub1_destination", None)
    #         __information["sub1_arrived"] = new_value


def get_indoor_destination():
    return get_information("sub4_destination")


def get_location():
    loc = None
    loc_data = __sub1.get_location()
    if loc_data is not None:
        loc = loc_data[0]
    return loc
    # return 25.0230239, 121.2210628
    # result = None
    # if "location" in __information:
    #     loc = __information["location"]
    #     if not loc is None:
    #         result = __information["location"][0]
    # return result


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


def is_awakable():
    return __sub1.is_awakable()


def is_indoor():
    return __sub1.is_indoor()


def is_user_speaking():
    return get_information("user_speaking")


def get_indoor_destination_text(name):
    logger.debug("get_indoor_destination_text, name: %s", str(name))
    names = {
        "exit_sign": "出口",
        "wc_sign": "廁所",
        "dangerous_sign": "危險",
        "elev_sign": "電梯",
        "sign": "標示",
        "platform": "月台",
        "gate": "入口",
        "0": "箭頭",
        "1": "電梯",
        "2": "感應",
        "3": "招牌",
        "4": "廁所",
        "5": "出口",
        "6": "入口",
        "7": "月台",
        "8": "中壢",
        "9": "台北",
        "99": "障礙物",
    }
    name = str(name)
    if name in names:
        return names[name]
    else:
        return "不明標示"


def parse_indoor_destination(destination_name):
    names = {
        "出口": "5",
        "廁所": "4",
        # "危險": "dangerous_sign",
        "電梯": "1",
        "月台": "7",
        "入口": "6",
        "中壢": "8",
        "台北": "9",
    }
    if destination_name in names:
        return names[destination_name]
    else:
        return None

def find_similar_location(name):
    threshold = 0.8
    s = 0
    name2, loc2 = None, None
    for k in __locations:
        s1 = Helper.similarity(name, k)
        if s1 >= threshold and s1 > s:
            s = s1
            loc2 = __locations[k]
            name2 = k

    return name2, loc2


# def find_similar_location(name, loc):
#     threshold = 0.8
#     loc0 = loc
#     s = 0
#     for k in __locations:
#         s1 = Helper.similarity(name, k)
#         if s1 >= threshold and s1 > s:
#             d = Helper.distance(loc0, __locations[k])
#             if d < 3000:
#                 s = s1
#                 loc = __locations[k]
#                 name = k
#
#     return name, loc

def load_locations(loc_path):
    rows = [
        # '24.960162, 121.166425, 7-ELEVEN 雙嶺門市',
        # '24.960022, 121.166404, 全家便利商店-中壢過嶺店',
        # '25.006505, 121.472863, 全家便利商店小和漢陽店',
        #'25.02303280351437, 121.22138864824944, 全家便利商店 大園領航店', # yen use
        '25.023037874095653, 121.22137852000279, 全家便利商店 大園領航店',
        '25.023851116389658, 121.22121641510186, 捷運領航站',  # '25.0241316, 121.22154358333333, 捷運領航站',
        '25.020353, 121.222749, 7-ELEVEN 城邑門市'
    ]

    #        '25.023026704865906, 121.2214073580765, 全家便利商店 大園領航店',
    #    '25.023851116389658, 121.22121641510186, 捷運領航站',    # '25.0241316, 121.22154358333333, 捷運領航站',
    #    '25.020353, 121.222749, 7-ELEVEN 城邑門市'
    # Kevin set GPS point:
    # A17 family: 25.023074566666665, 121.22144731666667
    # A17 Mrt: 25.0241316, 121.22154358333333

    # ver1:
    #       '25.023101667, 121.2214175, 全家便利商店 大園領航店',
    #   '25.0241316, 121.22154358333333, 捷運領航站'
    for row in rows:
        print('load_locations, row: %s' % (row,))
        aaa = [x.strip() for x in row.split(',')]
        if len(aaa) == 3:
            if aaa[2]:
                __locations[aaa[2]] = (float(aaa[0]), float(aaa[1]))

# def load_locations(loc_path):
#     if os.path.isfile(loc_path):
#         with open(loc_path, 'r') as fp:
#             rows = fp.readlines()
#         for row in rows:
#             aaa = [x.strip() for x in row.split(',')]
#             if len(aaa) == 3:
#                 if aaa[2]:
#                     __locations[aaa[2]] = (float(aaa[0]), float(aaa[1]))


#
def set_indoor_destination(dest):
    set_information('sub4_destination', dest)
    set_information('sub4_arrived', False)


def stop_indoor_destination():
    set_information('sub4_destination', None)
    set_information('sub4_arrived', True)


def set_outdoor_destination(coordinate, dest_type):
    if coordinate:
        dest = (coordinate[0], coordinate[1], dest_type)
        # set_information('sub1_arrived', False)
        set_information('sub1_destination', dest)
        __sub1.set_destination(dest)
        # set_information('sub1_arrived', False)
    else:
        set_information('sub1_destination', None)
        __sub1.set_destination(None)


def set_sub1(sub1):
    global __sub1
    __sub1 = sub1


def __set_user_speaking(is_speaking):
    set_information('user_speaking', is_speaking)
    __sub1.set_user_speaking(is_speaking)


# User will set to speaking immediately but stop speaking after 10 seconds
def set_user_speaking(is_speaking, shut_up_after_seconds=30):
    if is_speaking:
        __information['user_not_speaking_countdown'] = 0
        __set_user_speaking(True)
    else:
        if is_indoor():
            __set_user_speaking(False)
        else:
            __information['user_not_speaking_countdown'] = shut_up_after_seconds


def stop_outdoor_destination():
    set_information('sub1_destination', None)
    # set_information('sub1_arrived', True)


def set_indoor(indoor):
    __sub1.set_indoor(indoor)


def get_indoor_kanbans():
    return get_information("kanban_indoor")


def set_indoor_kanbans(kanbans):
    logger.debug("set_indoor_kanbans: %s", str(kanbans))
    set_information("kanban_indoor", kanbans)


def set_information(name, value):
    original_value = None
    if name in __information:
        original_value = __information[name]
    __information[name] = value
    __check_callback(name, original_value, value)


def start():
    # Initialize data
    # __information['sub1_arrived'] = True
    __information['sub1_destination'] = None
    __information['sub4_arrived'] = True
    __information['sub4_destination'] = None
    __information['user_speaking'] = False
    __information['user_not_speaking_countdown'] = 0
    # set_indoor(True)

    load_locations('./dialogue/data/location.txt')

    t = threading.Thread(target=__run)
    t.start()


def subscribe(name, callback, value="any"):
    logger.debug("Subscribe %s to callback: %s", name, str(callback))
    __callbacks[name] = (callback, value)
    # logger.debug("subscribe(name=%s, callback", name)


def terminate():
    global __running
    __running = False
    logger.warn("terminating")
