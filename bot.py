import telebot
from telebot import types

TOKEN = '8642199341:AAEpu60eX_2PgOnuSENDohFCtg0WU5EKesI'
ADMIN_ID = 997602481  # Ваш Telegram ID

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения состояний и выигрышей пользователей
user_data = {}

# Словарь расшифровки кодов призов
PRIZES_MAP = {
    "win_pack": "🎁 Бесплатная упаковка",
    "win_greens": "🌿 Эвкалипт и зелень",
    "win_card": "💌 Красивая открытка",
    "win_disc10": "🏷️ Скидка 10%",
    "win_ribbon": "🎀 Премиум-лента",
    "win_topper": "🪵 Топпер на выбор",
    "win_flowers": "💐 +3 цветка в подарок",
    "win_bonus500": "🪙 500 бонусов"
}

@bot.message_handler(commands=['start'])
def start_quiz(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}

    # Проверяем, перешел ли пользователь по ссылке с призом (например, /start win_pack)
    args = message.text.split()
    prize_text = "Не выбран"
    
    if len(args) > 1 and args[1] in PRIZES_MAP:
        prize_text = PRIZES_MAP[args[1]]
        user_data[chat_id]['prize'] = prize_text
        greeting = f"🎉 Поздравляем! Ваш приз **«{prize_text}»** закрепился за вашим аккаунтом!\n\nДавайте подберем букет за 3 шага:"
    else:
        user_data[chat_id]['prize'] = "Без приза"
        greeting = "Здравствуйте! Давайте подберем идеальный букет всего за 3 шага:"

    # Шаг 1: Выбор повода
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('🎂 День рождения', '❤️ Романтика', '💐 Просто так', '🎉 Праздник')
    
    bot.send_message(chat_id, greeting, parse_mode="Markdown", reply_markup=markup)
    bot.register_next_step_handler(message, process_occasion)

def process_occasion(message):
    chat_id = message.chat.id
    user_data[chat_id]['occasion'] = message.text

    # Шаг 2: Выбор даты
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Сегодня', 'Завтра', 'Указать дату')
    
    bot.send_message(chat_id, "📅 На какую дату нужен букет?", reply_markup=markup)
    bot.register_next_step_handler(message, process_date)

def process_date(message):
    chat_id = message.chat.id
    user_data[chat_id]['date'] = message.text

    # Шаг 3: Выбор бюджета
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('до 3 000 ₽', '3 000 – 7 000 ₽', 'от 7 000 ₽')
    
    bot.send_message(chat_id, "💰 Укажите ваш ориентировочный бюджет:", reply_markup=markup)
    bot.register_next_step_handler(message, process_budget)

def process_budget(message):
    chat_id = message.chat.id
    user_data[chat_id]['budget'] = message.text

    data = user_data[chat_id]
    username = f"@{message.from_user.username}" if message.from_user.username else "Не указан"
    name = message.from_user.first_name

    # Сообщение клиенту
    bot.send_message(
        chat_id, 
        "✅ Отлично! Заявка принята.\n\nНаш флорист уже подбирает варианты под ваши критерии и свяжется с вами в течение 5–10 минут!",
        reply_markup=types.ReplyKeyboardRemove()
    )

    # Карточка заявки для администратора с информацией о призе
    admin_card = (
        f"🔔 **Новая заявка из бота Florista!**\n\n"
        f"👤 **Клиент:** {name} ({username})\n"
        f"🎯 **Повод:** {data.get('occasion')}\n"
        f"📅 **Дата:** {data.get('date')}\n"
        f"💰 **Бюджет:** {data.get('budget')}\n"
        f"🎁 **Выигранный приз:** {data.get('prize')}"
    )

    bot.send_message(ADMIN_ID, admin_card, parse_mode="Markdown")

print("Бот Florista с поддержкой призов запущен...")
bot.infinity_polling()