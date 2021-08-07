from datetime import datetime
import threading
import time
from dialogue import Speaker, Helper, Information

logger = Helper.get_module_logger(__name__)
#


class Sub4(threading.Thread):
    def __init__(self, is_simulation):
        super(Sub4, self).__init__()
        logger.debug("__init__")
        self.current_location = (0, 0)
        self.is_simulation = is_simulation
        if self.is_simulation:
            self.sim_kanbans_index = 0
            self.sim_kanbans = self.read_sim_kanbans()
        self.running = True
        self.last_kanban_msg = ""
        self.last_kanban_msg_time = datetime.now()
        return

    def cancel_destination(self):
        dest = Information.get_information('sub4_destination')
        if dest is not None:
            self.play_sound("己停止前往" + dest)
        Information.set_information("sub4_arrived", True)


    def gen_direction_text(self, direction):
        directions = {
            "front": "前方",
            "front_right": "右前方",
            "right": "右方",
            "back_right": "右後方",
            "back": "後方",
            "back_left": "左後方",
            "left": "左方",
            "front_left": "左前方",
            "1": "一點鐘方向",
            "2": "兩點鐘方向",
            "3": "三點鐘方向",
            "4": "四點鐘方向",
            "5": "五點鐘方向",
            "6": "六點鐘方向",
            "7": "七點鐘方向",
            "8": "八點鐘方向",
            "9": "九點鐘方向",
            "10": "十點鐘方向",
            "11": "十一點鐘方向",
            "12": "十二點鐘方向",
        }
        key = str(direction)
        if key in directions:
            return directions[str(direction)]
        else:
            return "不明方向"

    def play_sound(self, msg, play_async=False):
        # logger.debug("play_sound: 0")
        now = datetime.now()
        if msg == self.last_kanban_msg:
            # logger.debug("play_sound: 1")
            diff = now - self.last_kanban_msg_time
            if diff.total_seconds() < 8:
                logger.warning("Skip message: " + msg)
                return

        self.last_kanban_msg = msg
        self.last_kanban_msg_time = now

        if not Speaker.is_playing():
            if play_async:
                Speaker.play_async(msg)
            else:
                Speaker.play(msg)

    def get_kanban(self, kanban_name):
        viewed_kanbans = Information.get_indoor_kanbans()
        if viewed_kanbans is None:
            return None
        for kanban in viewed_kanbans:
            logger.debug("Kanban: %s", str(kanban))
            if kanban_name == str(kanban["name"]):
                return kanban
        return None

    def speak_kanban(self, kanban):
        if Information.is_user_speaking():
            return

        msg = ""    # msg = format("%s方%s公尺處，有一個%s標示指向%s方")
        if kanban["user_direction"] is not None:
            msg += self.gen_direction_text(kanban["user_direction"])
        if kanban["distance"] is not None:
            msg += str(kanban["distance"]) + "步左右"
        if kanban["name"] is not None:
            msg += "有一個" + Information.get_indoor_destination_text(kanban["name"])
        if "direction" in kanban and kanban["direction"] is not None:
            msg += "指向" + self.gen_direction_text(kanban["direction"])

        logger.info(msg)
        self.play_sound(msg)
        # Speaker.play(msg)

    def speak_obstacle(self, kanban):
        msg = ""    # 前方N公尺處有障礙物，請轉向N點鐘方向
        if kanban["distance"] is not None:
            msg += "前方%s步左右有障礙物" % (str(kanban["distance"]),)
        else:
            msg += "前方有障礙物"

        if kanban["user_direction"] is not None:
            msg += "請轉向%s" % (self.gen_direction_text(kanban["user_direction"]),)

        logger.info(msg)
        self.play_sound(msg)
        # Speaker.play(msg)

    def update_sim_kanbans(self):
        logger.debug("update_sim_kanbans: 0")
        if not Information.is_indoor():
            return  # Not indoor, don't update

        self.sim_kanbans_index += 1
        if self.sim_kanbans_index >= len(self.sim_kanbans):
            self.sim_kanbans_index = 0
        kanban = self.sim_kanbans[self.sim_kanbans_index]
        Information.set_information("kanban_indoor", kanban)
        # logger.debug("Viewed kanbans: %s", json.dumps(kanban))

    def walk_timer(self):
        # logger.debug("walk_timer begin")
        arrived = Information.get_information('sub4_arrived')
        if not arrived:
            dest = Information.get_information('sub4_destination')
            kanban_name = Information.get_indoor_destination_text(dest)
            kanban = self.get_kanban(dest)
            if kanban is not None:
                distance = kanban["distance"]
                if distance is not None:
                    if float(distance) <= 0:
                        logger.warn("Arrived.")
                        self.play_sound("您已經抵達" + kanban_name)
                        Information.set_information("sub4_arrived", True)
                    else:
                        self.speak_kanban(kanban)
                else:
                    self.speak_kanban(kanban)
            else:
                # logger.debug("walk_timer 1, is_user_speaking: %s" % (Information.is_user_speaking(),))
                if not Information.is_user_speaking():
                    # logger.debug("walk_timer 2")
                    self.play_sound("我看不見有關" + kanban_name + "的標示", True)

            obstacle = self.get_kanban("99")
            if obstacle is not None:
                self.speak_obstacle(obstacle)

        # if self.running:
        #     Timer(10, self.walk_timer).start()

    def run(self):
        while self.running:
            if self.is_simulation:
                self.update_sim_kanbans()
            self.walk_timer()
            time.sleep(1)
        logger.info("terminated")
        return

    def terminate(self):
        self.running = False
        logger.warn("terminating")

    def read_sim_kanbans(self):
        kanbans = [
            [
                {
                    "name": 6,
                    "direction": 2,
                    "user_direction": 2,
                    "distance": 5
                },
                {
                    "name": "4",
                    "direction": "right",
                    "user_direction": "front",
                    "distance": 3.3
                },
                {
                    "name": "platform",
                    "direction": "right",
                    "user_direction": "front",
                    "distance": 0.3
                }
            ],
            [
                {
                    "name": "4",
                    "direction": "right",
                    "user_direction": "front",
                    "distance": 2.5
                },
                {
                    "name": "dangerous_sign",
                    "direction": "left",
                    "user_direction": "front_right",
                    "distance": 6.1
                },
                {
                    "name": "platform",
                    "direction": "front_right",
                    "user_direction": "front",
                    "distance": 2.3
                }
            ],
            [
                {
                    "name": "4",
                    "direction": "back_right",
                    "user_direction": "front_left",
                    "distance": 5.0
                },
                {
                    "name": "exit_sign",
                    "direction": "left",
                    "user_direction": "front",
                    "distance": 1.3
                },
                {
                    "name": "platform",
                    "direction": "right",
                    "user_direction": "front_left",
                    "distance": 4.1
                }
            ],
            [
                {
                    "name": "4",
                    "direction": "front_left",
                    "user_direction": "front",
                    "distance": 4.3
                },
                {
                    "name": "elev_sign",
                    "direction": "down",
                    "user_direction": "left",
                    "distance": 6.1
                },
                {
                    "name": "dangerous_sign",
                    "direction": "back_right",
                    "user_direction": "front-left",
                    "distance": 4.2
                }
            ],
            [
                {
                    "name": "exit_sign",
                    "direction": "front",
                    "user_direction": "front",
                    "distance": 5.6
                },
                {
                    "name": "dangerous_sign",
                    "direction": "back_left",
                    "user_direction": "front",
                    "distance": 3.7
                },
                {
                    "name": "platform",
                    "direction": "back_right",
                    "user_direction": "front",
                    "distance": 2.3
                }
            ],
            [
                {
                    "name": "4",
                    "direction": "front",
                    "user_direction": "front",
                    "distance": 0.5
                },
                {
                    "name": "exit_sign",
                    "direction": "left",
                    "user_direction": "front",
                    "distance": 7.3
                },
                {
                    "name": "platform",
                    "direction": "right",
                    "user_direction": "front_left",
                    "distance": 7.8
                }
            ],
        ]
        return kanbans

