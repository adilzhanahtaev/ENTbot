import telebot  # Импортируем библиотеку для работы с Telegram Bot API
from telebot import types  # Импортируем типы для создания кнопок и других элементов интерфейса

print("Импорт завершен.")

# Токен бота (получен от @BotFather)
TOKEN = '8588285671:AAFdHiSaGaUXByDYLLNFtT-SkrSKhUdftY8'

print("Токен установлен.")

# Создание экземпляра бота с проверкой токена 
try:
    bot = telebot.TeleBot(TOKEN)
    print("Бот создан!")
    me = bot.get_me()
    print(f"Бот: @{me.username}")
except Exception as e:
    print(f"Ошибка: {e}")
    exit()

print("Бот запущен!")

# Функция для создания клавиатуры с кнопкой "Продолжим" в ui чате 
def create_continue_markup():
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Продолжим", callback_data="continue")
    markup.add(btn)
    return markup

# Функция для создания основной клавиатуры выбора
def create_main_markup():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🗣Получить дополнительную информацию", callback_data="consultation")
    btn2 = types.InlineKeyboardButton("📚Выбрать профильные предметы", callback_data="subjects")
    markup.add(btn1)
    markup.add(btn2)
    return markup

# Функция для создания клавиатуры с кнопкой выбора предметов
def create_select_subjects_markup():
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("📚Выбрать профильные предметы", callback_data="subjects")
    markup.add(btn)
    return markup

# Функция для создания клавиатуры предметов
def create_subjects_markup():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Математика + Информатика", callback_data="math + informatics")
    btn2 = types.InlineKeyboardButton("Физика + Математика", callback_data="physics + math")
    btn3 = types.InlineKeyboardButton("Химия + биология", callback_data="chemistry + biology")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = f"Привет ✋ {message.from_user.first_name}, я бот для подготовки к ЕНТ. Скажи, нужна ли тебе дополнительная информация или готов выбрать профильный предмет? 🙂"
    markup = create_continue_markup()
    bot.send_message(message.chat.id, text, reply_markup=markup)

# Обработчик команды /продолжим (для совместимости)
@bot.message_handler(commands=['продолжим'])
def send_continue(message):
    text = "Что тебя интересует?"
    markup = create_main_markup()
    bot.send_message(message.chat.id, text, reply_markup=markup)

# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        chat_id = call.message.chat.id if call.message else call.from_user.id
        if call.data == "continue":
            text = "Что тебя интересует?"
            markup = create_main_markup()
            bot.send_message(chat_id, text, reply_markup=markup)
        elif call.data == "consultation":
            text = """Я бот-помощник для подготовки к ЕНТ. 👋
Я знаю, как иногда бывает трудно заставить себя открыть учебники или тесты. Мысли «сделаю завтра» — наш главный враг.
Поэтому я буду твоим «будильником» и навигатором в мире подготовки. 🧭
Каждый день я буду присылать тебе:
📖 Важные темы и лайфхаки.
🔔 Мягкие напоминания, что пора уделить время учебе.
Я верю в тебя и буду рядом на каждом шагу до самого экзамена.
Погнали к заветным баллам? 🎈🌟"""
            markup = create_select_subjects_markup()
            bot.send_message(chat_id, text, reply_markup=markup)
        elif call.data == "subjects":
            text = "Выберите предметы"
            markup = create_subjects_markup()
            bot.send_message(chat_id, text, reply_markup=markup)
        # Здесь можно добавить обработку для других callback_data, например, "math + informatics"
    except Exception as e:
        print(f"Ошибка в handle_callback: {e}")

# Запуск бота с обработкой ошибок и перезапуском
while True:
    try:
        print("Запуск polling...")
        bot.polling(none_stop=True,)
    except Exception as e:
        print(f"Ошибка polling: {e}")
