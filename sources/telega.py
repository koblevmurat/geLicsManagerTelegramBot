import telegram
import bot

from settings import InitSettings
Settings = InitSettings()
bot.Settings = Settings
bot.init()

from telegram.ext import Updater
updater = Updater(token=Settings['telegramBotToken'], use_context=True)
dispatcher = updater.dispatcher
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Использование: <Название решения>, [сброс]")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()

def echo(update, context):
    isSlic = str(update.message.text).strip().lower().find("сброс")>=0
    sn = str(update.message.text).strip().split(' ')[0]
    result = 'not found'
    if isSlic:
        result = bot.slic(sn)
    else:
        result = bot.glic(sn)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)
 