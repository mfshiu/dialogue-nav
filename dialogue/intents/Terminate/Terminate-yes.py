from dialogue import Speaker


def implement_intent(dialogue_client, query_result):
    Speaker.play("好的，我關機了，再見。")
    dialogue_client.shutdown()
