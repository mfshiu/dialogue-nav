import Speaker
import time
import NavHelper as map
from Destination import Destination
import Information


def implement_intent(client, query_result):
    if Information.is_indoor():
        dest = Information.get_indoor_destination()
        if dest is not None:
            Information.stop_indoor_destination()
            msg = "好的，己停止前往" + Information.get_indoor_destination_text(dest)
            Speaker.play(msg)
    else:
        dest = client.get_current_destination()
        if dest is not None:
            Information.stop_outdoor_destination()
            msg = "好的，己停止前往" + dest.name
            Speaker.play(msg)
    client.standby()
