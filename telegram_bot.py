from environs import Env
import telegram


env = Env()
env.read_env()
telegram_token = env.str('TELEGRAM_TOKEN')
chat_id = env.str('CHAT_ID')

bot = telegram.Bot(token=telegram_token)
bot.send_document(chat_id=chat_id, document=open('photos from space/nasa/Atlantis_to_Orbit.jpg', 'rb'))
