from dialogue import Speaker, NavHelper, Information, Helper
from dialogue.Destination import Destination

logger = Helper.get_module_logger(__name__)


def __find_place(place):
    max_meters = 3000
    name, coord, dist = NavHelper.get_nearest_place(place)
    if name is None:
        return None

    name2, coord2 = Information.find_similar_location(name)
    if name2:
        d = NavHelper.get_walking_distance(coord2)
        if d <= max_meters:
            name, coord, dist = name2, coord2, d

    if dist <= max_meters:
        return Destination(name, coord, dist)
    else:
        return None


def __process_indoor(client, target):
    dest = Information.parse_indoor_destination(target)
    if dest is None:
        Speaker.play("很抱歉，目前我還不知道怎麼帶你去" + target)
        client.standby(True)
    else:
        Speaker.play("好的，我現在開始找尋附近的" + target)
        Information.set_indoor_destination(dest)
        client.standby()


def __process_outdoor(client, target):
    msg = "好的，我現在為您找尋附近的" + target
    Speaker.play(msg)
    dest = __find_place(target)
    if dest:
        current_dest = client.get_current_destination()
        if current_dest:
            Speaker.play("最近的{}是{}，距離{}公尺。".format(target, dest.name, dest.distance))
            msg = "但是您正在前往{}的路上，確定要先去{}嗎？".format(current_dest.name, target)
            client.ask_user(msg)
            Speaker.play(msg)
            # Speaker.play("您正在前往{}的途中".format(current_dest.name))
            # Speaker.play("最近的{}是{}，距離{}公尺，在去{}之前要先過去那裡嗎？".format(target, d.name, d.distance, current_dest.name))
        else:
            Speaker.play("最近的{}是{}，距離{}公尺，要我帶您過去嗎？".format(target, dest.name, dest.distance))
        set_ready_destination(dest)
        client.listen_user()
    else:
        Speaker.play("很抱歉，我找不到附近的{}，".format(target))
        client.standby()


def get_ready_destination():
    global destination
    return destination


def set_ready_destination(dest):
    global destination
    destination = dest


def implement_intent(client, query_result):
    kanbans = Information.get_indoor_kanbans()

    all_kanbans = [Information.get_indoor_destination_text(k["name"]) for k in kanbans]

    if len(all_kanbans) == 0:
        msg = "前方看不見任何標示，請轉頭看看四週"
    else:
        if len(all_kanbans) == 1:
            msg = "前面的指標只有一個" + all_kanbans[0] + "標示"
        else:
            msg = "前面的指標有" + ",".join(all_kanbans[:-1])
            msg += "和" + all_kanbans[-1]
        msg += ", 請告訴我你想去的地方"

    Speaker.play(msg)
    client.listen_user()
