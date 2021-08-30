from dialogue import Speaker, Helper


logger = Helper.get_module_logger(__name__)


def implement_intent(client, resp):
    logger.debug("query_result: %s" % (resp,))
    if resp.fulfillment_text:
        msg = resp.fulfillment_text
    else:
        msg = "其實我也不清楚創新是什麼"
    Speaker.play(msg)
    client.listen_user()
    client.standby()

