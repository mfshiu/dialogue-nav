import Speaker


def implement_intent(dialogue_client, query_result):
    if query_result.fulfillment_text:
        Speaker.play(query_result.fulfillment_text)
        Speaker.play("請您再說一遍。")
        dialogue_client.listen_user()
    else:
        Speaker.play("如果需要我的協助再呼叫我。")
        dialogue_client.listen_hotword()
