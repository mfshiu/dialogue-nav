from dialogue import Speaker, Information, Helper

logger = Helper.get_module_logger(__name__)


def implement_intent(client, query_result):
    kanbans = Information.get_indoor_kanbans()

    all_kanbans = []
    for k in kanbans:
        if 'name' in k:
            all_kanbans.append(Information.get_indoor_destination_text(k["name"]))
    # all_kanbans = [Information.get_indoor_destination_text(k["name"]) for k in kanbans]

    if len(all_kanbans) == 0:
        msg = "前方看不見任何標示，請轉頭看看四週"
    else:
        if len(all_kanbans) == 1:
            msg = "前面的指標只有一個" + all_kanbans[0] + "標示"
        else:
            msg = "前面的指標有" + ",".join(all_kanbans[:-1])
            msg += "和" + all_kanbans[-1]
        msg += ", 請告訴我你想去的地方"

    Speaker.play(msg)
    client.listen_user()
