import random

import telebot
from telebot import types
import json
from datetime import date, timedelta

TOKEN = '7163273145:AAGozp6Y-yb2CvgrxzupoYtcFnsqYaHQP-o'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Бот для записи на процедуры запущен')


def generate_date_schedule():
    keyboard = types.InlineKeyboardMarkup()

    # Получаем кнопки для указанной даты
    days = []

    for i in range(7):
        days.append(date.today() + timedelta(days=3 + i))

    # Создаем кнопки и добавляем их на клавиатуру
    for button_text in days:
        callback_data = f"day:{button_text}"
        button = types.InlineKeyboardButton(text=str(button_text), callback_data=callback_data)
        keyboard.add(button)

    return keyboard


@bot.message_handler(commands=['show_dates'])
def handle_schedule(message):
    """Выбор даты"""
    # Отправляем клавиатуру с кнопками

    keyboard = generate_date_schedule()
    bot.send_message(message.chat.id, "Выберите день:", reply_markup=keyboard)


def generate_time_keyboard(chosen_date):
    keyboard = types.InlineKeyboardMarkup()

    # Получаем кнопки для указанной даты и времени
    times = ["10:00", "12:00", "15:00", "17:00"]


    try:
        with open('data.json', 'r') as file:
            user_data = json.load(file)
            for appointment in user_data["appointments"]:
                if appointment["date"] == date:
                    times.remove(appointment["time"])
    except :
        print(9)
    # Создаем кнопки и добавляем их на клавиатуру
    for time in times:
        callback_data = f"appointment:{chosen_date}:{time}"
        button = types.InlineKeyboardButton(text=time, callback_data=callback_data)
        keyboard.add(button)

    return keyboard


@bot.message_handler(commands=['set_name'])
def handle_set_name(message):
    bot.send_message(message.chat.id, "Введите имя")
    bot.register_next_step_handler_by_chat_id(message.chat.id, lambda message: save_client(message))


def save_client(message):
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"appointments": [], "review": [], "clients": {}}

    # Сохраняем имя пользователя
    data['clients'][message.chat.id] = message.text

    # Запись обновленных данных в файл
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

    bot.send_message(message.chat.id, "Ваше имя сохранено")


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data.startswith("day:"):
        chosen_date = call.data.split(":")[1]
        bot.send_message(call.message.chat.id, f"Вы выбрали дату: {chosen_date}")
        # Отправляем клавиатуру с доступным временем
        bot.send_message(call.message.chat.id, "Выберите время:", reply_markup=generate_time_keyboard(chosen_date))

    elif call.data.startswith("appointment:"):
        chosen_time = call.data.split(":")[1]
        bot.send_message(call.message.chat.id, f"Вы выбрали дату и время: {chosen_time}")
        # set_name()





def add_appointment( date, time, client):
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        data = {"appointments": [], "review": []}

    new_appointment = {'date': date, 'time': time, 'client': client}
    data['appointments'].append(new_appointment)

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(records, file, ensure_ascii=False)

def add_review(client, text):
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"appointments": [], "review": []}

    data["review"].append({
        "client": client,
        "text": text
    })

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

def handle_button_click(data):
    add_appointment(date, time, client)
    bot.send_message(message.chat.id, f'Вы записаны на {data} в {time}. Ждём вас!')

@bot.message_handler(commands=['add_review'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Напиши отзыв')
    bot.register_next_step_handler(message, save_review)


# Функция для сохранения отзыва
def save_review(message):
    client_id = message.chat.id
    review_text = message.text
    # Запись отзыва в файл
    add_review(client_id, review_text)
    bot.send_message(message.chat.id, "Спасибо за ваш отзыв!")



if __name__ == "__main__":
    bot.polling(none_stop=True)

