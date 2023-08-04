from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import time
from threading import Thread

app = Flask(__name__)

class Parser:
    def __init__(self, url, tag1, class1, absoLink, tag2, selector, id2):
        self.url = url
        self.tag1 = tag1
        self.class1 = class1
        self.absoLink = absoLink
        self.tag2 = tag2
        self.id2 = id2
        self.last_link = None
        self.selector = selector
        self.headers = {
            'User-Agent': 'My User Agent 1.0',
            'From': 'youremail@domain.example'
        }
        self.entries = []

    def get_links(self):
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all(self.tag1, class_=self.class1)]
        return links

    def get_info(self, link):
        response = requests.get(self.absoLink + link, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find(self.tag2, {self.selector: self.id2})
        return body.text

    def track_new_entries(self):
        while True:
            links = self.get_links()
            if links and links[0] != self.last_link:
                link = links[0]
                info = self.get_info(link)
                # print(f'New entry: {link}\n{info}')
                self.entries.append((link, info))
                self.last_link = link

            if len(self.entries) > 5:
                self.entries.pop(0)

            time.sleep(10)

parsers = [
    Parser('https://ria.ru/world/?ysclid=lkwmy2hseb929872560', 'a', 'list-item__title color-font-hover-only', '', 'div', 'class','article__body'),
    Parser('http://vlad2kun.pythonanywhere.com/', 'a', 'root', '', 'div', 'id','content'),
    Parser('https://openai.com/blog', 'a', 'cursor-pointer', 'https://openai.com', 'div', 'id','content'),
    Parser('https://vc.ru/tag/%D0%BD%D0%B5%D0%B9%D1%80%D0%BEсет%D0%B8?ysclid=lkvplwc01x448651742', 'a', 'content-link', '', 'div', 'class' ,'content'),
    Parser('https://neurosciencenews.com/neuroscience-terms/neural-networks/', 'a', 'read-more', '', 'div', 'class','entry-content'),
    Parser('https://aibusiness.com/ml/neural-networks', 'a', 'ArticlePreview-Title', 'https://aibusiness.com', 'div', 'class','ContentModule-Wrapper'),
    Parser('https://www.forbes.ru/tegi/neyroseti', 'a', 'ulGT3', 'https://www.forbes.ru', 'div', 'class','hfH2h')
]

for parser in parsers:
    t = Thread(target=parser.track_new_entries)
    t.start()

@app.route('/')
def news():
    entries = []
    for parser in parsers:
        entries.extend(parser.entries)
    entries.sort(key=lambda x: x[0], reverse=True)
    return render_template('news.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
