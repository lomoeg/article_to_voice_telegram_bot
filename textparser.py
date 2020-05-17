import requests
from readability import Document
from bs4 import BeautifulSoup
import html2text


# get clear text
def get_text(url):
    f_out = open("article.txt", 'w')
    rs = requests.get(url)
    doc = Document(rs.text)
    sum = doc.summary()
    res = html2text.html2text(sum)
    print(res, file=f_out)
    f_out.close()
    return res


# Trying to get site title
def get_site_name(url):
    domain = url.split("//")[-1].split("/")[0]
    return domain

# Get site title
def get_title(url):
    rs = requests.get(url)
    doc = Document(rs.text)
    return doc.title()


url = 'https://www.forbes.ru/obshchestvo/394385-dolzhny-li-universitety-zarabatyvat-koncepciya-troynoy-spirali-v-rossiyskih'

get_text(url)
print(get_site_name(url))

# url = 'https://vc.ru/tribuna/70439-speechki-servis-avtomaticheskogo-sozdaniya-audioversiy-statey'
# html_text = get_text(url)