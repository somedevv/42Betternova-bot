import os, requests
from Classes.messages import *

def confirm_delete(message, bot):
    url = '{}/api/users/{}'.format(os.environ['API_BASE_URL'], str(message.chat.id))
    hed = {'Authorization': 'Bearer {}'.format(os.environ["API_TOKEN"])}
    response = requests.delete(url, headers=hed)
    if response.status_code == 200:
        bot.send_message(message.chat.id, DeleteMessages.DELETE_SUCCESS)
    else:
        bot.send_message(message.chat.id, DeleteMessages.DELETE_FAILED)