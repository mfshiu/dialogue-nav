import Speaker


def implement_intent(dialogue_client, query_result):
    Speaker.play("好的，如果需要我的協助再呼叫我。")
    dialogue_client.listen_hotword()
