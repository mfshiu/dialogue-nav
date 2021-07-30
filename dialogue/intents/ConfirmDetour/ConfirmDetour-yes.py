from dialogue import Speaker
import dialogue.intents.NavStart as nav


def implement_intent(client, query_result):
    Speaker.play("好的，請繼續聽我的指示前進")
    dest = nav.get_ready_destination()
    if dest:
        client.add_destination(dest)
    else:
        Speaker.play("很抱欺我不知道要如何前往。")
    client.standby()
