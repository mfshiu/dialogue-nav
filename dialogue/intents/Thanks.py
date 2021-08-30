from dialogue import Speaker, Helper


logger = Helper.get_module_logger(__name__)


def implement_intent(client, resp):
    logger.debug("query_result: %s" % (resp,))
    msg = None
    if resp.fulfillment_text:
        msg = resp.fulfillment_text
    if msg:
        Speaker.play(msg)
    client.standby()

