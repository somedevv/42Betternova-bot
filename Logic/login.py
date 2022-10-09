import telebot, os, requests
from Classes.messages import LoginMessages
from Logic.checks import get_user

def login(message, bot):
    url = '{}/api/users/{}'.format(os.environ['API_BASE_URL'], str(message.chat.id))
    hed = {'Authorization': 'Bearer {}'.format(os.environ["API_TOKEN"])}
    response = requests.post(url, headers=hed)
    if response.status_code == 201:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Check 🧐', callback_data='LOGGED'))
        bot.send_message(message.chat.id, LoginMessages.LOGIN_MESSAGE.format(os.environ['LOGIN_URL'] ,os.environ['API_BASE_URL'] ,str(message.chat.id)), reply_markup=markup)

def confirm_login(message, bot):
    res, user_42_login = get_user(message.chat.id)
    if res == 200 and user_42_login is not None:
        bot.edit_message_text(LoginMessages.LOGIN_CONFIRMED.format(user_42_login), chat_id=message.chat.id, message_id=message.id)
    else:
        bot.send_message(message.chat.id, LoginMessages.LOGIN_FAILED)