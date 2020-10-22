import dialogflow_v2 as dialogflow
import os
from dialogue import Helper
from dialogue.Helper import get_module_logger
logger = get_module_logger(__name__)

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./dialogue/NCU-AI-5e22fe333aae.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./dialogue/vin-gmsx-ad3eb9c8c7e6.json"


def __detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    # print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        if Helper.is_debug():
            print('=' * 20)
            print('Query text: {}'.format(response.query_result.query_text))
            print('Detected intent: {} (confidence: {})\n'.format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence))
            print('Fulfillment text: {}\n'.format(
                response.query_result.fulfillment_text))

    return response.query_result


def __detect_intent_stream(project_id, session_id, audio_file_path,
                           language_code):
    logger.info('__detect_intent_stream: audio_file_path: %s', audio_file_path)

    """Returns the result of detect intent with streaming audio as input.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_FLAC
    sample_rate_hertz = 16000

    session_path = session_client.session_path(project_id, session_id)
    # print('Session path: {}\n'.format(session_path))

    def request_generator(audio_config, audio_file_path):
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        # The first request contains the configuration.
        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session_path, query_input=query_input)

        # Here we are reading small chunks of audio data from a local
        # audio file.  In practice these chunks should come from
        # an audio input device.
        with open(audio_file_path, 'rb') as audio_file:
            while True:
                chunk = audio_file.read(8192)
                # chunk = audio_file.read(4096)
                if not chunk:
                    break
                # The later requests contains audio data.
                yield dialogflow.types.StreamingDetectIntentRequest(
                    input_audio=chunk)

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)

    logger.debug("generate request...")
    requests = request_generator(audio_config, audio_file_path)
    logger.debug("send request...")
    responses = session_client.streaming_detect_intent(requests)
    logger.debug("responsed...")

    logger.debug('=' * 20)
    for response in responses:
        logger.debug('Intermediate transcript: "{}".'.format(
                response.recognition_result.transcript))
    # Note: The result from the last response is the final transcript along
    # with the detected content.
    query_result = response.query_result
    logger.debug('=' * 20)
    logger.debug('Query text: {}'.format(query_result.query_text))
    logger.debug('Detected intent: {} (confidence: {})\n'.format(
        query_result.intent.display_name,
        query_result.intent_detection_confidence))
    logger.debug('Fulfillment text: {}\n'.format(
        query_result.fulfillment_text))

    return query_result


LANGUAGE_CODE = "zh-TW"
PROJECT_ID = "vin-gmsx"
TEST_SESSION = "session1"


def send_text(text):
    return __detect_intent_texts(PROJECT_ID, TEST_SESSION, (text,), LANGUAGE_CODE)


def send_voice(voice_file):
    return __detect_intent_stream(PROJECT_ID, TEST_SESSION, voice_file, LANGUAGE_CODE)
