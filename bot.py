import telebot
import config
import synthesize_speech
from url_validate import *
from article_parser import get_clean_article


bot = telebot.TeleBot(config.tg_bot_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, {name}!\n\n Я умею переводить статьи в аудиофайлы. '
                                      'Пока что у меня есть ограничение - не больше 5000 символов.\n'
                                      'Некоторые статьи могут быть обрезаны до этого порога. \n'
                     .format(name=message.from_user.first_name))


@bot.message_handler(commands=['getaudio'])
def getaudio_message(message):
    msg = bot.send_message(message.chat.id, 'Отправь мне ссылку на статью')
    bot.register_next_step_handler(msg, get_audiofile)


def get_audiofile(message):
    url = message.text
    try:
        if is_valid_url(url):
            bot.reply_to(message, 'Супер! Синтезирую речь..\nЭто может занять несколько минут.')

            # Get dict with extracted article data
            article = get_clean_article(url)

            # Encode url to base64 (to avoid problems with filenames with '/' in unix)
            audio_name = base64_encoded_url(url)

            # Synthesize audiofile in mp3 format
            synthesize_speech.get_audio(audio_name + ".ogg", article['text_blocks'])
            bot.send_message(message.chat.id, 'Речь синтезирована, загружаю аудиофайл.')

            audiofile = open(config.folder + audio_name + ".mp3", 'rb')

            au = bot.send_audio(message.chat.id, audiofile,
                                None,
                                'something',
                                article['title'],
                                article['sitename'])
            audiofile.close()
        else:
            bot.reply_to(message, 'Прости, это не похоже на ссылку. А может просто сайт недоступен.')
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так.')
        print(str(e))


if __name__ == '__main__':
    bot.polling(none_stop=True)