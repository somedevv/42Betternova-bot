# 42Betternova-bot

A Telegram Bot, written in ```Python 3.11```, to check on your 42 White Nova cycle statistics, so you can be a pro Whitenover in style.

:warning: **This bot needs and API to work** and is not included, read ```Deploy it on your own``` for more details 🙂

## How to be a pro Whitenover

1. Download Telegram (easy step)
2. Start chatting with [@Betternova42_bot](https://t.me/Betternova42_bot)
3. Done

### Commands

```
/start - Start the bot, it will ask you to accept some terms and conditions and will send you a link so you can log in
/help - List the commands and what they do
/cycle - Get your current cycle stats
/delete - Delete your user and all your data from the DB, it will ask for confirmation
```

## Deploy it on your own

Because it's **free** and **fun** (kind off)

### How you can do it

Here you have infinite options, you can do it the same way as I do, or you can host everything on your own. The important part is that you create an API that follows the data structure the bot works with (Refeer to 'The data').

To deploy the bot you can:

- Build the docker image by running this on the root of the project:

  ``` docker build -t 42betternova-bot . ```

- Pull it from Docker:

  ``` docker pull somedevv/42betternova-bot:latest ```

Then deploy the bot with the following **container ENV variables**:

```
// The token set as Authentication Bearer to authenticate with your API
API_TOKEN=

// The base URL of your API
API_BASE_URL=https://something.com/api/

// The Telegram Token for the bot
TELEGRAM_TOKEN=
```

## The bot configuration

Appart from the obligatory env variables, the bot has some other configuration variables that can be set:

```
// The chat commands to add a timeout to, followed by a comma (,) without spaces.
TIMEOUT_FUNCTIONS

// The Telegram IDs of the users that can Bypass the timeouts, followed by a comma (,) without spaces.
BYPASS_TIMEOUT_USERS

// Boolean to enable or disable the bot, 1 for disable, 0 for enable
FREEZE_STATUS

// Boolean to enable or disable the bot to accept new users, 1 for disable, 0 for enable
DISABLE_NEW_USERS
```

## The data

The bot receives data from the API so it can be worked with and then sent to the user.

In every request, the bot checks for the user **login**, so it knows if the user exists or not in the DB. Also, it need the login to call him by his name in the messages, pretty self explanatory.

The 42 login is fetched as a JSON with this struture:

``` JS
{
  "login42": "" //[STRING] - User 42 login
}
```

For the cycle stats, the bot fetches it as a JSON with the following structure and data:

``` JS
{
  "cycle": {
     "campus_time": 0, // [INT] - Total time in the campus in seconds
     "evaluations": 0, //  [INT] - Number of evaluations 
     "events": 0, //  [INT] - Number of events 
     "logged_time": 0, //  [INT] - Total time logged in seconds
     "end_date": "" //  [STRING] - The end date of the cycle in the following format YYYY-MM-DD
  }
}

```

## The Telegram API Middleware

This bots implements a Simple Middleware to manage message requests. It can be found in the [bot.py](https://github.com/somedevv/42Betternova-bot/blob/main/bot.py) file.

``` Python 3.11
####### MIDDLEWARES CONFIG #######
class SimpleMiddleware(BaseMiddleware):
    def __init__(self, limit) -> None:
        self.last_time = {}
        self.limit = limit
        self.update_types = ['message']

    def pre_process(self, message, data):
        if message.text in timeout_funcs and message.from_user.id not in no_timeout_users:
            if message.from_user.id in self.last_time and message.date - self.last_time[message.from_user.id] < self.limit:
                bot.send_message(message.chat.id, ErrorMessages.TOO_MANY_REQUESTS.format(int((self.limit - (message.date - self.last_time[message.from_user.id])) / 60), int((self.limit - (message.date - self.last_time[message.from_user.id])) % 60)), parse_mode='HTML')
                return CancelUpdate()
            self.last_time[message.from_user.id] = message.date

    def post_process(self, message, data, exception):
        pass

bot.setup_middleware(SimpleMiddleware(300))
#######################################
```

Here you can change and modify how the Middleware acts in the pre and post process of a message.

### Timeouts to avoid request flooding

To avoid flooding of certain commands, I implemented a timeout if there is a request in X minutes after the last request.

``` Python 3.11
def pre_process(self, message, data):
        if message.text in timeout_funcs and message.from_user.id not in no_timeout_users:
            if message.from_user.id in self.last_time and message.date - self.last_time[message.from_user.id] < self.limit:
                bot.send_message(message.chat.id, ErrorMessages.TOO_MANY_REQUESTS.format(int((self.limit - (message.date - self.last_time[message.from_user.id])) / 60), int((self.limit - (message.date - self.last_time[message.from_user.id])) % 60)), parse_mode='HTML')
                return CancelUpdate()
            self.last_time[message.from_user.id] = message.date
```

Only the functions defined on the **TIMEOUT_FUNCTIONS** env varible will be afected by this limit. Also, all the users in **BYPASS_TIMEOUT_USERS** will bypass this timeout, so they will be ignored.

The time limit between calls can be defined in seconds as a parameter in ```bot.setup_middleware(SimpleMiddleware()))```:

``` Python 3.11
bot.setup_middleware(SimpleMiddleware(300)) # 300 Seconds = 5 minutes
```
