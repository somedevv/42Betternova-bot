class WelcomeMessages:
    WELCOME_NOT_LOGGED_IN = (
        'Welcome to the 42 Betternova Telegram bot,' +
        'this bot will help you see how you are doing with your current white nova cicle,' +
        'but first, we need you to accept our terms.\n' +
        'By using this bot you agree to the following terms:\n' +
            '- 📚 We will store your 42 Login\n' +
            '- 🫵🏻 We will associate your 42 Login with your Telegram ID\n' +
            '- 👌🏻 We will not store any other information about you\n' +
            '- 🗑️ You will be able to delete all your information at any time\n' +
        'Do you agree to these terms?'
        )
    WELCOME_LOGGED_IN = 'Welcome back {}! 👋🏻'
    TERMS_STATUS_NOT_AGREED = 'Terms status: Not Accepted ❌'
    TERMS_STATUS_AGREED = 'Terms status: Accepted ✅'
    TERMS_AGRREE = 'Agree to the terms ✅'

class ErrorMessages:
    UNDEFINED_ERROR = 'Ups something went wrong, please try again later'
    USER_NOT_FOUND = 'You don\'t seem to be logged in, please use /start to login and use the bot'
    RESPONSE_ERROR = 'Error: response {}'
    CYCLE_ERROR = 'Hi {}, there was an error getting your cycle 😔, please try again later'

class LoginMessages:
    LOGIN_MESSAGE = 'Please, login using the following link:\n{}&redirect_uri={}/api/auth/intra42?id={}&response_type=code\nThen click the button below'
    LOGIN_CONFIRMED = 'Login confirmed ✅ Welcome {}! 👋🏻\nYou can now use the bot'
    LOGIN_FAILED = 'Login failed ❌\nPlease try again'

class HelpMessages:
    HELP_MESSAGE = (
        '/start - Start the bot\n' +
        '/help - Show a help message\n' +
        '/cycle - See your current cycle\n' +
        '/delete - Delete all your information\n'
        )

class DeleteMessages:
    DELETE_SUCCESS = 'All your information has been deleted ✅'
    DELETE_FAILED = 'Ups something went wrong, please try again later'
    DELETE_CONFIRMATION = 'Hi {}, are you sure you want to delete all your information? This action cannot be undone'
    CONFIRM_DELETE = 'Confirm delete 🗑️'

class CycleMessages:
    CYCLE_MESSAGE = ('Hi {}, your current cycle stats are:\n' +
        'Logged in time: {} Hours {} Minutes {} Seconds\n' +
        'Events: {}\n' +
        'Evaluations: {}\n'
        )
    FETCHING_CYCLE = '🕑 Fetching your cycle stats...'
    