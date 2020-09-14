import Speaker
import Destination
import intents.NavStart as nav


def implement_intent(client, query_result):
    dest = client.get_current_destination()
    if dest:
        Speaker.play_async("好的，我們繼續聽前往" + dest.name)
    client.listen_hotword()
