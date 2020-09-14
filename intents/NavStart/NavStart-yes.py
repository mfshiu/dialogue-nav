import Speaker
import Destination
import intents.NavStart as nav


def implement_intent(client, query_result):
    Speaker.play("好的，現在開始請聽我的指示前進")
    # Destinations.add(Destinations.Destination(nav.destination))
    client.add_destination(nav.destination)
    client.listen_hotword()
