from dialogue import Speaker
import dialogue.intents.NavStart as nav


def implement_intent(client, query_result):
    Speaker.play("好的，請繼續聽我的指示前進")
    client.add_destination(nav.get_ready_destination())
    client.standby()
