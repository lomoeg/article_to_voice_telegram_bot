import requests
import subprocess
import config


def get_IAM_token():
    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    data = "{\"yandexPassportOauthToken\":\"" + config.OAuth_token + "\"}"
    response = requests.post(url, data=data)
    return response.json()["iamToken"]


iam_token = get_IAM_token()


# Synthesize one block (5k symbols max) of speech from yandex.speechkit
def synthesize(folder_id, iam_token, article_block_text):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + iam_token,
    }

    data = {
        'text': article_block_text,
        'lang': 'ru-RU',
        'folderId': folder_id,
        'voice': 'zahar'
    }

    resp = requests.post(url, headers=headers, data=data, stream=True)

    if resp.status_code != 200:
        raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

    for chunk in resp.iter_content(chunk_size=None):
        yield chunk


# Synthesize full audio from chunks in ogg and convert it to mp3
def get_audio(audio_name, text_blocks_array):

    with open(config.folder + audio_name, "wb") as f:
        for text_block in text_blocks_array:
            for audio_content in synthesize(config.folder_id, iam_token, text_block):
                f.write(audio_content)
            print("Block completed. len: " + str(len(text_block)))
    print('Audio in OGG format synthesized! Now convering to mp3...')

    subprocess.call("./ogg_to_mp3_converter.sh " + audio_name, shell=True)
    print("Done converting. For more info see previous logs.")