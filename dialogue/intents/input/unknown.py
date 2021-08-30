from dialogue import Speaker


def implement_intent(dialogue_client, query_result):
    if query_result.fulfillment_text:
        if query_result.fulfillment_text:
            Speaker.play(query_result.fulfillment_text)
        else:
            Speaker.play("請您再說一遍。")
        dialogue_client.listen_user()
    else:
        dialogue_client.standby()
