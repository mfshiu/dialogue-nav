import Speaker


def implement_intent(dialogue_client, query_result):
    Speaker.play("好的")
    dialogue_client.standby()
