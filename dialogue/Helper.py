import logging
import sys


def is_arrived(curr, dest):
    lan1 = round(curr[0], 5)
    lnt1 = round(curr[1], 5)
    lan2 = round(dest[0], 5)
    lnt2 = round(dest[1], 5)
    return lan1 == lan2 and lnt1 == lnt2

# def find_places(place)
#     places = gmaps.places(query='7-ELEVEN', radius='300', language='zh-TW')
#     print(places)
#     first = places['results'][0]
#
#     print(first['name'])
#     print(first['geometry']['location']['lat'])
#     print(first['geometry']['location']['lng'])

def get_module_logger(mod_name):
    logging.getLogger().handlers.clear()

    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-20s %(levelname)-8s %(message)s') # , "%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


helper_logger = get_module_logger(__name__)


def get_module(package_name, module_name):
    import importlib

    full_module_name = package_name + "." + module_name
    try:
        module = importlib.import_module(full_module_name)
    except:
        helper_logger.error("Cannot get module from: %s", full_module_name)
        from dialogue.intents.input import unknown
        module = unknown
    finally:
        return module


def is_debug():
    gettrace = getattr(sys, 'gettrace', None)
    return gettrace is not None


def is_equal(a, b):
    if a is None or b is None:
        return a is None and b is None
    if type(a) != type(b):
        return False
    if hasattr(a, '__len__'):
        if len(a) != len(b):
            return False
        return str(a) == str(b)
    return a == b
