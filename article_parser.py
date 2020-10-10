from newspaper import Article
from config import folder
from url_validate import base64_encoded_url


# Extract article in text format from html page
def get_clean_article(url):
    f_out = open(folder + base64_encoded_url(url) + ".txt", 'w')
    article = Article(url)

    article.download()
    article.parse()

    print(article.text, file=f_out)
    f_out.close()

    return {'text_blocks': divide_text(article.text), 'title': article.title, 'sitename': article.source_url}


# Divide large text into parts <5000 symbols (naive implementation)
# Return array of text parts of len < 5000 symbols
def divide_text(text):
    if len(text) <= 5000:
        return [text]
    else:
        divided_text_array = []
        idx = 0
        while idx < len(text):
            part = text[idx:idx+5000]
            # Find the last meaningful end of sentence
            end_of_block = max(part.rfind('. '), part.rfind('? '), part.rfind('! '))
            if end_of_block != -1:
                divided_text_array.append(part[:end_of_block+2])
                idx += end_of_block + 2
            else:
                divided_text_array.append(part)
                idx += 5000
    return divided_text_array


# get_clean_article("https://rb.ru/opinion/proptech-against-crisis/")
# print(divide_text())