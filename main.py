import telebot
from telebot.types import (Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery,
                            InlineKeyboardMarkup, InlineKeyboardButton as IB)


words = []
users_id = []
TONEN = "ВАШ ТОКЕН"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["exit"])
def handler(msg: Message):
    kb = InlineKeyboardMarkup()
    kb.row(IB('Подтвердить', callback_data='yes'))
    kb.row(IB("Отмена", callback_data='no'))
    bot.send_message(msg.chat.id, "Вы точно хотите выйти из игры???",reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith('exit'))
def callback(call: CallbackQuery):
    data = call.data.split()[1]
    if data == 'yes':
        # Если пользователь подтвердил выход, очищаем его ID из списка и отправляем сообщение
        if call.from_user.username in users_id:
            users_id.remove(call.from_user.username)
            bot.send_message(call.message.chat.id, f"Пользователь @{call.from_user.username} вышел из игры.")
        else:
            bot.send_message(call.message.chat.id, "Вы не находитесь в игре.")
    elif data == 'no':
        # Если пользователь отменил выход, просто отправляем сообщение
        bot.send_message(call.message.chat.id, "Вы остались в игре.")


@bot.message_handler(commands=['start'])
def handler_start(msg: Message):
    kb = InlineKeyboardMarkup()
    kb.row(IB('Присоединиться', callback_data='start play'))
    bot.send_message(msg.chat.id, 'Игра началась', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.startswith('start'))
def callback(call: CallbackQuery):
    print(users_id)
    
    if call.from_user.username not in users_id:
        users_id.append(call.from_user.username)  
    else:
        bot.answer_callback_query(call.id, 'Вы уже в игре')

    if len(users_id) == 1:
        global hotdogs
        hotdogs = bot.send_message(call.message.chat.id, f'Сейчас ходит @{call.from_user.username}')


@bot.message_handler(content_types=['text'])
def handler(msg: Message):
    print(users_id)
    small_text = msg.text.lower()  # Приводим текст к нижнему регистру
    if users_id:
        if msg.from_user.username != users_id[0]:
            bot.delete_message(msg.chat.id, msg.id)

        elif words and small_text[0] != words[-1][-1]:
            bot.send_message(msg.chat.id, f"Неправильное слово. Ваше слово должно начинаться с буквы '{words[-1][-1]}'.")

        else:
            words.append(small_text)  # Добавляем слово в список
            print(words)
            del users_id[0]
            global hotdogs
            users_id.append(msg.from_user.username)
            bot.delete_message(msg.chat.id, hotdogs.id)
            hotdogs = bot.send_message(msg.chat.id, f'//Слово добавлено// Сейчас ходит @{users_id[0]}')




bot.infinity_polling()
