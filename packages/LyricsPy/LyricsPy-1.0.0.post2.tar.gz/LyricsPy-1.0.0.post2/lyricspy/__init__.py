from bs4 import BeautifulSoup
from seleniumrequestshtml import Chrome
from selenium.webdriver.chrome.options import Options
from bingpy import Client
import re

options = Options()
options.add_argument("--headless")
webdriver = Chrome(chrome_options=options)
session = webdriver.requests_session

def letra(query, **kwargs):
    r = session.get(query)
    data = r.html.html
    return parse(data, query)


def auto(query, limit=4):
    result = []
    n = 0
    for i in Client().search(q='site:musixmatch.com ' + query):
        if re.match(r'^(https?://)?(musixmatch\.com/|(m\.|www\.)?musixmatch\.com/).+', i['url']) and not '/translation' in i['url'] and not '/artist' in i['url']:
            print(i['url'])
            try:
                a = letra(i['url'])
                result.append(a)
                n += 1
            except AttributeError:
                pass
            if n == limit:
                break

    return result

def parse(data, url):
    soup = BeautifulSoup(data, "html.parser")
    autor = soup.find('a', {'class':'mxm-track-title__artist mxm-track-title__artist-link'})
    b = ''
    x = soup.find_all('span', {'class':['lyrics__content__ok','lyrics__content__warning']})
    for i in x:
        b += i.get_text()
    musica = str(soup.find('h1', {'class': 'mxm-track-title__track'})).split('</small>')[1].replace('</h1>','')
    ret = {'autor': autor.get_text(), 'musica': musica, 'letra': b, 'link': url}
    return ret