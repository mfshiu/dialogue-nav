from dialogue import Speaker
import dialogue.intents.NavStart as nav

from dialogue.Helper import get_module_logger
logger = get_module_logger(__name__)


def implement_intent(client, query_result):
    dest = nav.get_ready_destination()
    if dest is not None:
        Speaker.play("好的，現在開始請聽我的指示前進")
        client.add_destination(dest)
        nav.set_ready_destination(None)
    else:
        logger.error("No destination.")
    client.standby()
