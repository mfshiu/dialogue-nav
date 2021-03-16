from dialogue import Speaker
import dialogue.intents.NavStart as nav

from dialogue.Helper import get_module_logger
logger = get_module_logger(__name__)


def implement_intent(client, query_result):
    Speaker.play("好的，如有需要再呼叫我")
    client.standby()
