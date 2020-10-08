from dialogue import Speaker


def implement_intent(dialogue_client, query_result):
    Speaker.play("關機後系統就不會再回應了，要重新啟動才行，您確定嗎？")
    dialogue_client.listen_user()
