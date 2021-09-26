import telegram
import logging
from bot import GrotemServerConnector
from settings import init_settings
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Использование: <Название решения>, [сброс]")


def echo(update, context):
    # isSlic = str(update.message.text).strip().lower().find("сброс") >= 0
    sn = str(update.message.text).strip().split(' ')[0]
    if 'сброс' in str(update.message.text).lower():
        # result = bot.slic(sn)
        result = bot.reset_lic_count(solution_name=sn)
        response_text = f'{result["data"]}'
    else:
        result = bot.get_lic_info(solution_name=sn)
        # TODO: add response text
        response_text = f'{result["data"]}'

    context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)


def main():
    settings = init_settings()
    # bot.settings = settings
    # bot.init()
    bot = GrotemServerConnector(settings['bitmobile_host'], settings['root_password'])
    if not bot.check_connection():
        raise ConnectionError(f'Unable connect to Bitmobile server {settings["bitmobile_host"]}')
    updater = Updater(token=settings['telegram_bot_token'], use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()

