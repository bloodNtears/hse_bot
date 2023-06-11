"""This is telegram bot for training hard."""

import sqlite3
from time import sleep
from datetime import time
from config import *

# Create an instance of the bot
bot = telebot.TeleBot("")

# Global variable to store the user's training schedule
training_schedule = {}
db = sqlite3.connect('reminder.db')
cur = db.cursor()
try:
    query = '''DROP TABLE IF EXISTS 'Chats';
    DROP TABLE IF EXISTS 'Reminders';
    CREATE TABLE 'Chats' (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER
    );

    CREATE TABLE 'Reminders' (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        day TEXT,
        time TEXT,
        remind_in INTEGER,
        FOREIGN KEY (chat_id) REFERENCES Chats(chat_id)
    );
    '''
    statements = query.split(';')
    for statement in statements:
        cur.execute(statement.strip())
    db.commit()
    db.close()
except Exception as e:
    print(e)


@bot.message_handler(commands=['start'])
def start(message):
    """Function handling start command."""
    bot.send_message(
        message.chat.id,
        "Привет! Это %Лютое название% бот! "
        "Я буду Вашим помощником в достижении спортивных целей. Надеюсь, мы подружимся!",
        reply_markup=menu_markup)


@bot.message_handler(func=lambda message: message.text.lower()
                     in ['выбрать упражнение', 'выбрать план', 'составить расписание', 'удалить напоминания'])
def handle_menu_message(message):
    """Function menu commands."""
    if message.text.lower() == 'выбрать упражнение':
        choose_exercise(message)
    elif message.text.lower() == 'выбрать план':
        choose_workout_plan(message)
    elif message.text.lower() == 'составить расписание':
        create_schedule(message)
    elif message.text.lower() == 'удалить напоминания':
        print("HUII")
        delete_reminders(message)


def delete_reminders(message):
    chat_id = message.chat.id
    db = sqlite3.connect('reminder.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM Chats WHERE chat_id = ?", (chat_id,))
    result = cur.fetchone()
    print(result)
    if result is None:
        bot.send_message(chat_id, "У вас нет активных напоминаний!")
    else:
        cur.execute("DELETE FROM 'Reminders' WHERE chat_id = ?", (chat_id,))
        cur.execute("DELETE FROM 'Chats' WHERE chat_id = ?", (chat_id,))
        bot.send_message(chat_id, "Напоминания удалены.")
    db.commit()
    db.close()


def choose_exercise(message):
    """Function sends body_markup keyboard."""
    bot.send_message(
        message.chat.id,
        "Пожалуйста, выберите область группы мышц",
        reply_markup=body_markup)


def choose_upper_body_muscle(message):
    """Function sends upper_body_markup keyboard."""
    bot.send_message(
        message.chat.id,
        "Пожалуйста, выберите группу мышц верха тела",
        reply_markup=upper_body_markup)


def choose_lower_body_muscle(message):
    """Function sends lower_body_markup keyboard."""
    bot.send_message(
        message.chat.id,
        "Пожалуйста, выберите группу мышц низа тела",
        reply_markup=lower_body_markup)


def choose_workout_plan(message):
    """Function sends workout_markup keyboard."""
    bot.send_message(
        message.chat.id,
        "Пожалуйста, выберите сколько дней в неделю вы готовы заниматься",
        reply_markup=workout_markup)


def create_schedule(message):
    """Function sends schedule_markup keyboard."""
    bot.send_message(
        message.chat.id,
        "Пожалуйста, выберите день или нажмите \"Готово✅\", если вы закончили.",
        reply_markup=schedule_markup)


@bot.message_handler(
    func=lambda message: message.text.lower() in [
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
        "воскресенье"])
def handle_day(message):
    """Function handles day message."""
    global last_day
    last_day = message.text
    training_schedule[last_day] = None
    bot.send_message(
        message.chat.id,
        "Пожалуйста, укажите время начала тренировки в формате hh:mm",
        reply_markup=remove_keyboard_markup)


# bot.reply_to(message, "Пожалуйста, укажите время начала тренировки в формате hh:mm",
# 			 reply_markup=types.ReplyKeyboardRemove)


@bot.message_handler(regexp=r'\d{2}:\d{2}')
def handle_start_time(message):
    """Function handles day message."""
    time_str = message.text
    try:
        print(last_day, time(int(time_str[:2]), int(time_str[3:])))
        training_schedule[last_day] = message.text
        create_schedule(message)
    except ValueError:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, укажите корректное время начала тренировки в формате hh:mm",
            reply_markup=remove_keyboard_markup)


@bot.message_handler(func=lambda message: message.text.lower() == "готово✅")
def hande_schedule_finish(message):
    """Function handles schedule finishing message."""
    if not training_schedule:
        bot.send_message(
            message.chat.id,
            "Ваше расписание пока пустое. Пожалуйста, выберите хотя бы один день.",
            reply_markup=schedule_markup)
    else:
        order = [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
            "Воскресенье"]
        sorted_schedule = dict(
            sorted(
                training_schedule.items(),
                key=lambda item: order.index(
                    item[0])))
        msg = ""
        for key, value in sorted_schedule.items():
            msg += f"{key}:\n{value}\n\n"
        bot.send_message(
            message.chat.id,
            msg,
            reply_markup=remove_keyboard_markup)
        bot.send_message(
            message.chat.id,
            "Хотите установить напоминания о тренировках?",
            reply_markup=reminder_markup)


@bot.message_handler(func=lambda message: message.text.lower()
                     in ["да, за 30 минут", "да, за 1 час", "нет"])
def handle_reminder(message):
    """Function handles reminder options."""
    match message.text.lower():
        case 'да, за 30 минут':
            set_reminder(30, message.chat.id)
            bot.send_message(
                message.chat.id,
                "Хорошо! Буду напоминать о тренировках за 30 минут до начала!",
                reply_markup=menu_markup)
        case 'да, за 1 час':
            set_reminder(60, message.chat.id)
            bot.send_message(
                message.chat.id,
                "Хорошо! Буду напоминать о тренировках за 1 час до начала!",
                reply_markup=menu_markup)
        case 'нет':
            bot.send_message(
                message.chat.id,
                "Надеюсь, вы не забудете о тренировках!",
                reply_markup=menu_markup)


def set_reminder(minutes, chat_id):
    """Function sets reminder."""
    db = sqlite3.connect('reminder.db')
    cur = db.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO 'Chats' (chat_id) VALUES (?)", (chat_id,))
    cur.execute("DELETE FROM 'Reminders' WHERE chat_id = ?", (chat_id,))
    db.commit()
    for day, start_time in training_schedule.items():
        cur.execute(
            "INSERT INTO 'Reminders' (chat_id, day, time, remind_in) VALUES (?, ?, ?, ?)",
            (chat_id,
             day,
             start_time,
             minutes))
    db.commit()
    db.close()


@bot.message_handler(func=lambda message: message.text.lower()
                     in ['верх тела', 'низ тела'])
def handle_choose_muscle(message):
    """Function handles group of muscles options."""
    if message.text.lower() == 'верх тела':
        choose_upper_body_muscle(message)
    elif message.text.lower() == 'низ тела':
        choose_lower_body_muscle(message)


@bot.message_handler(func=lambda message: message.text.lower()
                     in ['грудь', 'бицепс', 'трицепс', 'плечи', 'спина', 'пресс'])
def handle_upper_body(message):
    """Function handles upper_body options."""
    match message.text.lower():
        case 'грудь':
            msg = "💪🏻Упражнения на грудь:\n\n"
            msg += parse_exercises(chest_exercises)
            bot.send_message(
                message.chat.id,
                msg,
                reply_markup=menu_markup,
                disable_web_page_preview=True)
        case 'бицепс':
            msg = "💪🏻Упражнения на бицепс:\n\n"
            msg += parse_exercises(biceps_exercises)
            bot.send_message(
                message.chat.id,
                msg,
                reply_markup=menu_markup,
                disable_web_page_preview=True)
        case 'трицепс':
            msg = "💪🏻Упражнения на трицепс:\n\n"
            msg += parse_exercises(triceps_exercises)
            bot.send_message(
                message.chat.id,
                msg,
                reply_markup=menu_markup,
                disable_web_page_preview=True)
        case 'плечи':
            msg = "💪🏻Упражнения на плечи:\n\n"
            msg += parse_exercises(shoulders_exercises)
            bot.send_message(
                message.chat.id,
                msg,
                reply_markup=menu_markup,
                disable_web_page_preview=True)
        case 'спина':
            msg = "💪🏻Упражнения на спину:\n\n"
            msg += parse_exercises(back_exercises)
            bot.send_message(
                message.chat.id,
                msg,
                reply_markup=menu_markup,
                disable_web_page_preview=True)
        case 'пресс':
            msg = "💪🏻Упражнения на пресс:\n\n"
            msg += parse_exercises(abdominals_exercises)
            bot.send_message(
                message.chat.id,
                msg,
                reply_markup=menu_markup,
                disable_web_page_preview=True)
    bot.send_message(
        message.chat.id,
        "Как я могу вам ещё помочь?",
        reply_markup=menu_markup)


@bot.message_handler(
    func=lambda message: message.text.lower() in [
        'икры',
        'передняя поверхность бедра',
        'задняя поверхность бедра',
        'ягодицы'])
def handle_lower_body(message):
    """Function handles lower_body options."""
    match message.text.lower():
        case 'икры':
            msg = "💪🏻Упражнения на икры:\n\n"
            msg += parse_exercises(calves_exercises)
            bot.send_message(
                message.chat.id,
                msg,
                reply_markup=menu_markup,
                disable_web_page_preview=True)
        case 'передняя поверхность бедра':
            msg = "💪🏻Упражнения на переднюю поверхность бедра:\n\n"
            msg += parse_exercises(quads_exercises)
            bot.send_message(
                message.chat.id,
                msg,
                reply_markup=menu_markup,
                disable_web_page_preview=True)
        case 'задняя поверхность бедра':
            msg = "💪🏻Упражнения на заднюю поверхность бедра:\n\n"
            msg += parse_exercises(hamstrings_exercises)
            bot.send_message(
                message.chat.id,
                msg,
                reply_markup=menu_markup,
                disable_web_page_preview=True)
        case 'ягодицы':
            msg = "💪🏻Упражнения на ягодицы:\n\n"
            msg += parse_exercises(glutes_exercises)
            bot.send_message(
                message.chat.id,
                msg,
                reply_markup=menu_markup,
                disable_web_page_preview=True)
    bot.send_message(
        message.chat.id,
        "Как я могу вам ещё помочь?",
        reply_markup=menu_markup)


@bot.message_handler(func=lambda message: message.text.lower()
                     in ['2 дня', '3 дня', '4 дня', '5 дней'])
def handle_workout_plan(message):
    """Function handles workout_plan options."""
    match message.text.lower():
        case '2 дня':
            bot.send_media_group(message.chat.id, two_days_media)
        case '3 дня':
            bot.send_media_group(message.chat.id, three_days_media)
        case '4 дня':
            bot.send_media_group(message.chat.id, four_days_media)
        case '5 дней':
            bot.send_media_group(message.chat.id, five_days_media)
    bot.send_message(
        message.chat.id,
        "Как я могу вам ещё помочь?",
        reply_markup=menu_markup)


while True:
    try:
        print("Started")
        bot.polling(none_stop=True)
    except Exception as e:
        sleep(3)
        print(e)
