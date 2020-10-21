from dialogue import Speaker


def implement_intent(client, query_result):
    dest = client.get_current_destination()
    if dest:
        Speaker.play_async("好的，我們繼續前往" + dest.name)
    client.standby()
