from flask import Flask, render_template
import requests
import freeGPT
from asyncio import run, create_task

async def main(text, text2, text3, text4, text5, title1, title2, title3, title4, title5):
    prompt = 'переведи на русский, перепиши текст уникальным и в дружелюбном и понятном для студента стиле' + title1
    prompt2 = 'переведи на русский, перепиши текст уникальным и в дружелюбном и понятном для студента стиле' + title2
    prompt3 = 'переведи на русский, перепиши текст уникальным и в дружелюбном и понятном для студента стиле' + title3
    prompt4 = 'переведи на русский, перепиши текст уникальным и в дружелюбном и понятном для студента стиле' + title4
    prompt5 = 'переведи на русский, перепиши текст уникальным и в дружелюбном и понятном для студента стиле' + title5
    prompt6 = 'переведи на русский' + text
    prompt7 = 'переведи на русский' + text2
    prompt8 = 'переведи на русский' + text3
    prompt9 = 'переведи на русский' + text4
    prompt10 = 'переведи на русский' + text5
    
    try:
            resp = await getattr(freeGPT, "gpt3").Completion().create(prompt)
            resp2 = await getattr(freeGPT, "gpt3").Completion().create(prompt2)
            resp3 = await getattr(freeGPT, "gpt3").Completion().create(prompt3)
            resp4 = await getattr(freeGPT, "gpt3").Completion().create(prompt4)
            resp5 = await getattr(freeGPT, "gpt3").Completion().create(prompt5)
            resp6 = await getattr(freeGPT, "gpt3").Completion().create(prompt6)
            resp7 = await getattr(freeGPT, "gpt3").Completion().create(prompt7)
            resp8 = await getattr(freeGPT, "gpt3").Completion().create(prompt8)
            resp9 = await getattr(freeGPT, "gpt3").Completion().create(prompt9)
            resp10 = await getattr(freeGPT, "gpt3").Completion().create(prompt10)
            return {'text': [resp, resp2, resp3, resp4, resp5], 'title': [resp6, resp7, resp8, resp9, resp10]}
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
    # res = [run(main(articles[0]['description'])), run(main(articles[1]['description'])), run(main(articles[2]['description'])), run(main(articles[3]['description'])), run(main(articles[4]['description']))]
    res = run(main(articles[0]['description'], articles[1]['description'], articles[2]['description'], articles[3]['description'], articles[4]['description'], articles[0]['title'], articles[1]['title'], articles[2]['title'], articles[3]['title'], articles[4]['title']))
    # Отображаем шаблон index.html и передаем список статей
    return render_template('index.html', articles=articles, res=res)

if __name__ == '__main__':
    app.run(debug=True)
