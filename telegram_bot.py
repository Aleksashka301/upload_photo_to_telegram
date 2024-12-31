from environs import Env
import telegram


env = Env()
env.read_env()
telegram_token = env.str('TELEGRAM_TOKEN')
chat_id = env.str('CHAT_ID')

bot = telegram.Bot(token=telegram_token)
bot.send_message(chat_id=chat_id, text="Test")
