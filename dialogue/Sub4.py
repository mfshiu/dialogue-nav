import threading
import time
import json
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
        return

    def cancel_destination(self):
        dest = Information.get_information('sub4_destination')
        if dest is not None:
            Speaker.play("己停止前往" + dest)
        Information.set_information("sub4_arrived", True)

    def gen_direction_text(self, direction):
        directions = {
            "front": "前",
            "front_right": "右前",
            "right": "右",
            "back_right": "右後",
            "back": "後",
            "back_left": "左後",
            "left": "左",
            "front_left": "左前",
        }
        return directions[direction]

    def get_kanban(self, kanban_name):
        viewed_kanbans = Information.get_indoor_kanbans()
        if viewed_kanbans is None:
            return None
        for kanban in viewed_kanbans:
            logger.debug("Kanban: %s", str(kanban))
            if kanban_name == k["name"]:
                return kanban
        return None

    def speak_kanban(self, kanban):
        msg = ""    # msg = format("%s方%s公尺處，有一個%s標示指向%s方")
        if kanban["user_direction"] is not None:
            msg += self.gen_direction_text(kanban["user_direction"]) + "方"
        if kanban["distance"] is not None:
            msg += str(kanban["distance"]) + "公尺處"
        if kanban["name"] is not None:
            msg += "有一個" + Information.get_indoor_destination_text(kanban["name"]) + "標示"
        if kanban["direction"] is not None:
            msg += "指向" + self.gen_direction_text(kanban["direction"]) + "方"
        Speaker.play_async(msg)

    def update_sim_kanbans(self):
        if not Information.is_indoor():
            return  # Not indoor, don't update

        self.sim_kanbans_index += 1
        if self.sim_kanbans_index >= len(self.sim_kanbans):
            self.sim_kanbans_index = 0
        kanban = self.sim_kanbans[self.sim_kanbans_index]
        Information.set_information("kanban_indoor", kanban)
        # logger.debug("Viewed kanbans: %s", json.dumps(kanban))

    def walk_timer(self):
        arrived = Information.get_information('sub4_arrived')
        if not arrived:
            dest = Information.get_information('sub4_destination')
            kanban_name = Information.get_indoor_destination_text(dest)
            kanban = self.get_kanban(dest)
            if kanban is not None:
                distance = kanban["distance"]
                if distance is not None:
                    if float(distance) < 1.5:
                        logger.warn("Arrived.")
                        Speaker.play("您已經抵達" + kanban_name)
                        Information.set_information("sub4_arrived", True)
                    else:
                        self.speak_kanban(kanban)
                else:
                    self.speak_kanban(kanban)
            else:
                Speaker.play_async("我看不見有關" + kanban_name + "的標示")

        # if self.running:
        #     Timer(10, self.walk_timer).start()

    def run(self):
        while self.running:
            if self.is_simulation:
                self.update_sim_kanbans()
            self.walk_timer()
            time.sleep(8)
        logger.info("terminated")
        return

    def terminate(self):
        self.running = False
        logger.warn("terminating")

    def read_sim_kanbans(self):
        kanbans = [
            [
                {
                    "name": "exit_sign",
                    "direction": "front_left",
                    "user_direction": "front",
                    "distance": 5.2
                },
                {
                    "name": "wc_sign",
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
                    "name": "wc_sign",
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
                    "name": "wc_sign",
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
                    "name": "wc_sign",
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
                    "name": "wc_sign",
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

