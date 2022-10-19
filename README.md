# 42Betternova-bot
A Telegram Bot, written in Python, to check on your 42 White Nova cycle statistics, so you can be a pro Whitenover in style.

## How to be a pro Whitenover

1. Download Telegram (easy step)
2. Start chatting with [@Betternova42_bot](https://t.me/Betternova42_bot)
3. Done

## Deploy it on your own
Because it's **free** and **fun** (kind off)

### How I deployed it
This bots works in conjunction with my own private API. The API fetches all needed data from the 42 API and sends it in a beautifull JSON to the bot. Also, it manages a noSQL DB where I store:

- The users Telegram along with his 42 login
- The cycle data such as end and start dates
- Other credentials that are updated constantly to keep them fresh

The API is hosted on a Firebase project, using GCP Cloud Functions for the API and Firestore for the noSQL DB.

Meanwhile, the Telegram bot is imaged as a Docker Image, using Github Actions that runs on tag creation, and deployed on a Respberry Pi 4B running [Portainer](https://www.portainer.io/).

### How you can do it
Here you have infinite options, you can do it the same way as I do, or you can host everything on your own. The important part is that you create an API that follows the data structure the bot works with (Refeer to 'The data').

To deploy the bot, you only need to build the docker image by running this on the root of the project:

``` docker build -t 42betternova-bot . ```

Then deploy the bot with the following **container ENV variables**:
```
// The API token set as Bearer to authenticate with your API
API_TOKEN=

// The base URL of your API
API_BASE_URL=https://myapi.com/

// The Telegram Token for the bot
TELEGRAM_TOKEN=

// The chat commands to add a timeout to, followed by a comma (,) without spaces.
TIMEOUT_FUNCTIONS=/start,/help,...

// The Telegram IDs of the users that can Bypass the timeouts, followed by a comma (,) without spaces.
BYPASS_TIMEOUT_USERS=XXXXXXXX,XXXXXXXX,...
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
