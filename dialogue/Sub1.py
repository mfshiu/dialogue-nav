import threading
from threading import Timer
from dialogue import Helper, Information
import time

logger = Helper.get_module_logger(__name__)


class Sub1(threading.Thread):
    def __init__(self):
        super(Sub1, self).__init__()
        logger.debug("__init__")
        self.current_location = (0, 0)
        self.destination = (0, 0)
        self.locations = self.__read_locations()
        self.running = True
        return

    def __walk_timer(self):
        # arrived = Information.get_information('sub1_arrived')
        dest = Information.get_information('sub1_destination')
        # 如果還沒到且目的地不同，就會前進
        if dest is not None:
            # dest = Information.get_information('sub1_destination')
            if not Helper.is_arrived(self.current_location, dest):
                if len(self.locations) > 0:
                    self.current_location = self.locations.pop(0)
                    Information.set_information("location", self.current_location)
                    logger.debug("walk to: %s", str(self.current_location))
            if Helper.is_arrived(self.current_location, dest):
                logger.warn("Arrived.")
                Information.set_information('sub1_destination', None)
                # Information.set_information("sub1_arrived", True)

        if self.running:
            Timer(5, self.__walk_timer).start()

    def run(self):
        self.__walk_timer()
        while self.running:
            time.sleep(.1)
        logger.info("terminated")
        return

    def terminate(self):
        self.running = False
        logger.warn("terminating")

    def __read_locations(self):
        return [
            (25.019588, 121.22174166666667, True),
            (25.019588, 121.22174166666667, True),
            (25.019581166666665, 121.22174833333334, True),
            (25.019581166666665, 121.22174833333334, True),
            (25.019581166666665, 121.22174833333334, True),
            (25.0195735, 121.22175366666667, True),
            (25.0195735, 121.22175366666667, True),
            (25.0195735, 121.22175366666667, True),
            (25.019567, 121.2217595, True),
            (25.019567, 121.2217595, True),
            (25.019567, 121.2217595, True),
            (25.019567, 121.2217595, True),
            (25.023061, 121.2214232, True),  # 全家
            (25.019560, 121.221770, True),
            (25.019560, 121.221770, True),
            (25.0240057, 121.2210846, True)  # A17
        ]

