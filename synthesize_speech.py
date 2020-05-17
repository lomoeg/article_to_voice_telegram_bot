import requests
import subprocess
import config


def get_IAM_token():
    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    data = "{\"yandexPassportOauthToken\":\"" + config.OAuth_token + "\"}"
    response = requests.post(url, data=data)
    return response.json()["iamToken"]


iam_token = get_IAM_token()

output = 'speech.ogg'


# Synthesize one block (5k symbols max) of speech from yandex.speechkit
def synthesize(folder_id, iam_token, article):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + iam_token,
    }

    data = {
        'text': article,
        'lang': 'ru-RU',
        'folderId': folder_id,
        'voice': 'filipp'
    }

    resp = requests.post(url, headers=headers, data=data, stream=True)

    if resp.status_code != 200:
        raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

    for chunk in resp.iter_content(chunk_size=None):
        yield chunk


# Synthesize full audio from chunks in ogg and convert it to mp3
def get_audio(text_blocks_array):
    with open(output, "wb") as f:
        for block in text_blocks_array:
            print(block)
            for audio_content in synthesize(config.folder_id, iam_token, block):
                f.write(audio_content)
            print("Block completed. len: " + str(len(block)))
    print('Audio in OGG format synthesized! Now convering to mp3...')

    subprocess.call("./ogg_to_mp3_converter.sh", shell=True)
    print("Done converting. For more info see previous logs.")