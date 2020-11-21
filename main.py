import logging
from webpreview import web_preview
import wikipedia
import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
# from settings import TOKEN


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def find_artist(update: Update, context: CallbackContext) -> None:
    data = update.message.text
    logger.info(f"data from user {data}")

    try:
        web_prev = web_preview(data)
        full = web_prev[1]
        artist = full[full.find("a song by") + len("a song by "):full.find(" on Spotify")]
        wiki_info = wikipedia.summary(artist)
        update.message.reply_text(wiki_info)
    
    except:
        update.message.reply_text("Your link is incorect! Please provide a track link (you can get it from share button in spotify)")
    


def main():
    NAME = os.environ.get("HEROKU_APP_NAME")
    TOKEN = os.environ["TOKEN"]

    # Port is given by Heroku
    PORT = int(os.environ.get("PORT", "8443"))

    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, find_artist))

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT ,
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))

    updater.idle()


if __name__ == '__main__':
    main()
