import os, requests
from Classes.messages import *

def confirm_delete(message, bot, user_42_login):
    url = '{}/api/users/{}'.format(os.environ['API_BASE_URL'], str(message.chat.id))
    hed = {'Authorization': 'Bearer {}'.format(os.environ["API_TOKEN"])}
    response = requests.delete(url, headers=hed)
    if response.status_code == 200:
        bot.edit_message_text(DeleteMessages.DELETE_CONFIRMATION.format(user_42_login, StatusMessages.SUCCESS), chat_id=message.chat.id, message_id=message.id)
        bot.send_message(message.chat.id, DeleteMessages.DELETE_SUCCESS)
    else:
        bot.edit_message_text(DeleteMessages.DELETE_CONFIRMATION.format(user_42_login, StatusMessages.ERROR), chat_id=message.chat.id, message_id=message.id)
        bot.send_message(message.chat.id, DeleteMessages.DELETE_FAILED)
