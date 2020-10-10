from newspaper import Article


# Extract article in text format from html page
def get_clean_article(url):
    f_out = open("article.txt", 'w')
    article = Article(url)

    article.download()
    article.parse()

    print(article.text, file=f_out)
    f_out.close()
    return {'text_blocks': divide_text(article.text), 'title': article.title, 'sitename': article.source_url}


# Divide large text into parts <5000 symbols (naive implementation)
# Return array of text parts of len < 5000 symbols
def divide_text(text):
    # text_blocks_count = ceil(len(text) / 5000)
    f_0 = open("full_parts.txt", 'w')
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
            print(part[:end_of_block+2], file=f_0)
    f_0.close()
    return divided_text_array