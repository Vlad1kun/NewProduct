import telebot
from asyncio import run, sleep
from freeGPT import gpt3

# Устанавливаем токен вашего бота
bot = telebot.TeleBot('6308503974:AAFWhjyFad6zuvljhsVN89eTJlyfKFtmREA')
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
            resp = await getattr(gpt3, 'Completion')().create(prompt=user_input)
            bot.reply_to(message, f'🤖: {resp}')
        except Exception as e:
            bot.reply_to(message, f'🤖: {e}')

    # Запускаем асинхронную функцию
    run(process_user_input())

# Запускаем бота
bot.polling()
