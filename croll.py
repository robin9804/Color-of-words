import requests
from bs4 import BeautifulSoup

# 조선일보 url
url1 = 'https://www.chosun.com/'

# 특정 사이트에 접속하는 요청 객체 생성,
r1 = requests.get(url1)

# BeatifulSoup 객체 생성
soup = BeautifulSoup(r1.content, "html.parser", from_encoding='utf-8')

h2 = soup.select('h2')
print(h2[0].text) # h2의 글자만 추출한 것


class Crolling:
    def __init__(self, url):
        self.url = url
        self.request = requests.get(self.url)
        self.soup = BeautifulSoup(self.request.content, "html.parser", from_encoding='utf-8') # BeatifulSoup 객체

    def get_title(self):
        k = self.soup.select('a')
        title = []
        for i in range(len(k)):
            title.append(k[i])
        return title

    def make_sentence(self, sen):
        sentence = ''
        for i in range(len(sen)):
            sentence.join(sen[i])
        return sentence


