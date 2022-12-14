import telebot, os, requests, logging, sys, datetime
from telebot.handler_backends import BaseMiddleware, CancelUpdate
from Classes.messages import *
from Logic.delete import *
from Logic.login import *
from Logic.checks import *

####### ONLY FOR TESTING AND DEVELOPMENT #######
# from dotenv import load_dotenv
# load_dotenv()
################################################

####### SETUP TELEGRAM BOT #######
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token, use_class_middlewares=True)
##################################

####### ACTIVATE AND CONFIGURE LOGGING #######
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
###############################################

####### OTHER OPTIONAL SETTINGS CONFIGURATION #######
if 'BOT_FREEZE_STATUS' in os.environ:
    BOT_FREEZE_STATUS = int(os.environ['BOT_FREEZE_STATUS'])  # 0 = bot is active, 1 = bot is frozen
else:
    BOT_FREEZE_STATUS = 0

if 'TIMEOUT_FUNCTIONS' in os.environ:
    timeout_funcs = os.environ['TIMEOUT_FUNCTIONS'].split(',') # list of functions that should not be affected by the timeout separated by comma
else:
    timeout_funcs = []

if 'BYPASS_TIMEOUT_USERS' in os.environ:
    no_timeout_users = [ eval(i) for i in os.environ['BYPASS_TIMEOUT_USERS'].split(',') ] # list of users that should not be affected by the timeout separated by comma
else:
    no_timeout_users = []
    
if 'DISABLE_NEW_USERS' in os.environ:
    DISABLE_NEW_USERS = int(os.environ['DISABLE_NEW_USERS']) # 0 = new users can register, 1 = new users cannot register
else:
    DISABLE_NEW_USERS = 0
############################################

####### MIDDLEWARES CONFIG #######
class SimpleMiddleware(BaseMiddleware):
    def __init__(self, limit) -> None:
        self.last_time = {}
        self.limit = limit
        self.update_types = ['message']

    def pre_process(self, message, data):
        if DISABLE_NEW_USERS == 1 and message.text == '/start':
            res, user_42_login = get_user(message.chat.id)
            if res == 404 or (res==200 and user_42_login is None):
                bot.send_message(message.chat.id, ErrorMessages.DISABLE_NEW_USERS, parse_mode='HTML')
                return CancelUpdate()
                
        if BOT_FREEZE_STATUS == 1:
            res, user_42_login = get_user(message.chat.id)
            if res == 404 or (res==200 and user_42_login is None):
                user_42_login = 'anon'
            bot.send_message(message.chat.id, ErrorMessages.BOT_FREEZE_STATUS.format(user_42_login), parse_mode='HTML')
            return CancelUpdate()

        if message.text in timeout_funcs and message.from_user.id not in no_timeout_users:
            if message.from_user.id in self.last_time and message.date - self.last_time[message.from_user.id] < self.limit:
                bot.send_message(message.chat.id, ErrorMessages.TOO_MANY_REQUESTS.format(int((self.limit - (message.date - self.last_time[message.from_user.id])) / 60), int((self.limit - (message.date - self.last_time[message.from_user.id])) % 60)), parse_mode='HTML')
                return CancelUpdate()
            self.last_time[message.from_user.id] = message.date

    def post_process(self, message, data, exception):
        pass

bot.setup_middleware(SimpleMiddleware(300))
#######################################

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'ACCEPT_TERMS':
        try:
            bot.edit_message_text(WelcomeMessages.TERMS_STATUS_AGREED, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='HTML')
            login(call.message, bot)
        except Exception as e:
            fail(call.message, e)
    if call.data == 'LOGGED':
        try:
            confirm_login(call.message, bot)
        except Exception as e:
            fail(call.message, e)
    if call.data == 'RETRY_LOGING':
        try:
            login(call.message, bot)
        except Exception as e:
            fail(call.message, e)
    if call.data == 'CONFIRM_DELETE':
        try:
            res, user_42_login = get_user(call.message.chat.id)
            if res == 200 and user_42_login is not None:
                bot.edit_message_text(DeleteMessages.DELETE_CONFIRMATION.format(user_42_login, StatusMessages.CONFIRMED), chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='HTML')
                confirm_delete(call.message, bot, user_42_login)
            elif res == 404 or (res==200 and user_42_login is None):
                bot.edit_message_text(DeleteMessages.DELETE_CONFIRMATION.format(user_42_login, StatusMessages.ERROR), chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='HTML')
        except Exception as e:
            fail(call.message, e)
    if call.data == 'CANCEL_DELETE':
        try:
            res, user_42_login = get_user(call.message.chat.id)
            if res == 200 and user_42_login is not None:
                bot.edit_message_text(DeleteMessages.DELETE_CONFIRMATION.format(user_42_login, StatusMessages.CANCELED), chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='HTML')
            elif res == 404 or (res==200 and user_42_login is None):
                bot.edit_message_text(DeleteMessages.DELETE_CONFIRMATION.format(user_42_login, StatusMessages.ERROR), chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='HTML')
        except Exception as e:
            fail(call.message, e)

@bot.message_handler(commands=['start'])
def start(message):
    logging.info('User {} started the bot'.format(message.from_user.id))
    res, user_42_login = get_user(message.chat.id)
    if res == 200 and user_42_login is not None:
        bot.send_message(message.chat.id, WelcomeMessages.WELCOME_LOGGED_IN.format(user_42_login), parse_mode='HTML')
    elif res == 404 or (res==200 and user_42_login is None):
        bot.send_message(message.chat.id, WelcomeMessages.WELCOME_NOT_LOGGED_IN)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text=WelcomeMessages.TERMS_AGRREE, callback_data='ACCEPT_TERMS'))
        bot.send_message(message.chat.id, WelcomeMessages.TERMS_STATUS_NOT_AGREED, reply_markup=markup)
    else:
        fail(message, ErrorMessages.RESPONSE_ERROR.format(res))

@bot.message_handler(commands=['help'])
def help(message):
    logging.info('User {} requested help'.format(message.from_user.id))
    bot.send_message(message.chat.id, HelpMessages.HELP_MESSAGE)

@bot.message_handler(commands=['delete'])
def delete(message):
    logging.info('User {} requested delete'.format(message.from_user.id))
    res, user_42_login = get_user(message.chat.id)
    if res == 200 and user_42_login is not None:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text=DeleteMessages.CONFIRM_DELETE, callback_data='CONFIRM_DELETE'))
        markup.add(telebot.types.InlineKeyboardButton(text=DeleteMessages.CANCEL_DELETE, callback_data='CANCEL_DELETE'))
        bot.send_message(message.chat.id, DeleteMessages.DELETE_CONFIRMATION.format(user_42_login, StatusMessages.WAITING_FOR_CONFIRMATION), reply_markup=markup, parse_mode='HTML')
    elif res == 404 or (res==200 and user_42_login is None):
        bot.send_message(message.chat.id, ErrorMessages.USER_NOT_FOUND)
    else:
        fail(message, ErrorMessages.RESPONSE_ERROR.format(res))

@bot.message_handler(commands=['cycle'])
def cycle(message):
    logging.info('User {} requested cycle'.format(message.from_user.id))
    msg = bot.send_message(message.chat.id, CycleMessages.FETCHING_CYCLE)
    res, user_42_login = get_user(message.chat.id)
    if res == 200 and user_42_login is not None:
        url = '{}/api/users/{}/cycle'.format(os.environ['API_BASE_URL'], str(message.chat.id))
        hed = {'Authorization': 'Bearer {}'.format(os.environ["API_TOKEN"])}
        response = requests.get(url, headers=hed)
        if response.status_code == 200:
            # LOGGED TIME
            mm, ss = divmod(round(response.json()['cycle']['logged_time']), 60)
            hh, mm = divmod(mm, 60)
            # EVENTS
            events = response.json()['cycle']['events']
            # EVALUATIONS
            evaluations = response.json()['cycle']['evaluations']
            end_date = datetime.datetime.strptime("{}T{}".format(response.json()['cycle']['end_date'],"10:0:0.000Z"), '%Y-%m-%dT%H:%M:%S.%fZ')
            now = datetime.datetime.now()
            delta = end_date - now
            cycle_days, cycle_hours, cycle_minutes = delta.days, delta.seconds // 3600, delta.seconds // 60 % 60
            bot.edit_message_text(CycleMessages.CYCLE_MESSAGE.format(
                user_42_login,
                "???" if hh >= 12 else "???", # LOGGED TIME COMPLETION STATUS
                hh, 
                mm, 
                ss,
                "???" if events >= 2 else "???", # EVENTS COMPLETION STATUS 
                events, 
                "???" if evaluations >= 2 else "???", # EVALUATIONS COMPLETION STATUS 
                evaluations, 
                cycle_days, 
                cycle_hours, 
                cycle_minutes
                ), message_id=msg.message_id, chat_id=msg.chat.id, parse_mode='HTML')
        else:
            bot.edit_message_text(ErrorMessages.CYCLE_ERROR.format(user_42_login), message_id=msg.message_id, chat_id=msg.chat.id, parse_mode='HTML')
    elif res == 404 or (res==200 and user_42_login is None):
        bot.send_message(message.chat.id, ErrorMessages.USER_NOT_FOUND)
    else:
        fail(message, ErrorMessages.RESPONSE_ERROR.format(res))

def fail(message, e):
    logging.error(e)
    bot.send_message(message.chat.id, ErrorMessages.UNDEFINED_ERROR)

bot.polling()
