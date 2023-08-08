import telebot
from flask import Flask, request

from freeGPT import gpt3

# Создаем экземпляр Flask приложения
app = Flask(__name__)

# Устанавливаем токен вашего бота
bot = telebot.TeleBot('6308503974:AAFWhjyFad6zuvljhsVN89eTJlyfKFtmREA')


# Обработчик для webhook, принимает POST запросы от Telegram
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return '', 200


# Функция для обработки команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, 'Привет! Я бот, работающий на модели GPT-3.5 Turbo.')


# Функция для обработки всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text

    # Асинхронная функция для выполнения запроса к модели GPT-3.5 Turbo
    async def process_user_input():
        try:
            # Выполняем запрос к модели GPT-3.5 Turbo
            resp = await getattr(gpt3.Completion(), 'create')(prompt=user_input)
            print(f'🤖: {resp.choices[0].text}')  # Выводим сообщение в консоль
            bot.reply_to(message, f'🤖: {resp.choices[0].text}')
        except Exception as e:
            print(f'🤖: {e}')  # Выводим сообщение об ошибке в консоль
            bot.reply_to(message, f'🤖: {e}')

    # Запускаем асинхронную функцию
    gpt3.setup()
    gpt3.get_engine('text-davinci-003')
    gpt3.load_model('gpt-3.5-turbo')
    app.bot = bot
    app.user_input = user_input
    app.loop = asyncio.get_event_loop()
    app.loop.create_task(process_user_input())

    return '', 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)
