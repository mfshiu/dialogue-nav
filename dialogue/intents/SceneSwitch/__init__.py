from dialogue import Speaker, Information


def implement_intent(client, query_result):
    target = query_result.parameters['scene']

    if len(target) == 0:
        msg = "我沒聽清楚要切換到哪個場景，請再說一遍。"
        Speaker.play(msg)
        client.listen_user()
    else:
        if "室內" == target:
            Information.set_indoor(True)
            Speaker.play("好的，已經切換到" + target)
        elif "室外" == target:
            Information.set_indoor(False)
            Speaker.play("好的，已經切換到" + target)
        else:
            Speaker.play("很抱歉，我還不知道怎麼切換到" + target)
        client.standby(True)
