from flask import Flask, render_template
import requests
import freeGPT
from asyncio import run

async def main(text):
    prompt = 'переведи текст на руский и сделай текст уникальным, в дружелюбном стиле и понятным для студента, если текст незакончен и написано читать далее то удали это: ' + text #ты Журналист с опытом 10 лет работы,перепиши этот текст красиво,добавь смайлики,если текст заканчиваеться на прочитать далее или что в таком духе то закончи его, передай глвную суть в 50 слов,переведи на русский язык, пиши в дружелюбном и понятном для студента стиле:
    try:
            resp = await getattr(freeGPT, "gpt3").Completion().create(prompt)
            return f" {resp}"
    except Exception as e:
            print(f"🤖: {e}")

async def translate(text):
    prompt = 'переведи текст на руский' + text 
    try:
            resp = await getattr(freeGPT, "gpt3").Completion().create(prompt)
            return f" {resp}"
    except Exception as e:
            print(f"🤖: {e}")




app = Flask(__name__)
api_key = '093960e94efb4e6b98d7d0f62b042be8'  # Замените YOUR_NEWS_API_KEY на ваш собственный ключ News API
news_api_url = 'https://newsapi.org/v2/everything'
news_params = {
    'q': 'openai',    # Ваш запрос
    'sortBy': 'publishedAt',
    'apiKey': api_key,
}

def get_news():
    # Отправляем GET-запрос к News API
    response = requests.get(news_api_url, params=news_params)
    
    # Получаем ответ в формате JSON
    data = response.json()
    
    # Создаем пустой список для хранения статей
    articles = []
    
    # Итерируемся по статьям в данных от News API
    for article in data['articles']:
        # Проверяем, есть ли ключ 'description' и является ли описание непустым
        if 'description' in article and article['description']:
            # Проверяем, заканчивается ли описание точкой
            if article['description'][-1] == '.':
                # Если все проверки пройдены, добавляем статью в список
                articles.append(article)
    
    # Возвращаем только пять последних статей
    return articles[:5]

@app.route('/')
def index():
    # Получаем новости при обращении к странице
    articles = get_news()
    desq = [run(main(articles[0]['description'])), run(main(articles[1]['description'])), run(main(articles[2]['description'])), run(main(articles[3]['description'])), run(main(articles[4]['description']))]
    titles = [run(translate(articles[0]['title'])), run(translate(articles[1]['title'])), run(translate(articles[2]['title'])), run(translate(articles[3]['title'])), run(translate(articles[4]['title']))]
    
    # Отображаем шаблон index.html и передаем список статей
    return render_template('index.html', articles=articles, titles=titles, desq=desq)

if __name__ == '__main__':
    app.run(debug=True)
