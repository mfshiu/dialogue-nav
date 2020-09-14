import Information
import time


def callback01(name, value):
    print("%s is changed to: %s" % (name, value))


Information.subscribe('time', callback01)
Information.start()

time.sleep(10)
Information.terminate()
