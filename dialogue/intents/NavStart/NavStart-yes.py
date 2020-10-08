from dialogue import Speaker
import dialogue.intents.NavStart as nav

from dialogue.Helper import get_module_logger
logger = get_module_logger(__name__)


def implement_intent(client, query_result):
    if nav.destination is not None:
        Speaker.play("好的，現在開始請聽我的指示前進")
        client.add_destination(nav.destination)
    else:
        logger.error("No destination.")
    client.standby()
