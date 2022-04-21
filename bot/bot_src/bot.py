from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN


def start(update, context):
    btn1 = InlineKeyboardButton('1', callback_data="1st_button")
    btn2 = InlineKeyboardButton('2', callback_data="2nd_button")
    rm = InlineKeyboardMarkup([[btn1, btn2]])
    update.message.reply_text("Привет!"
                              "Этот бот предназначен для управления активными проектами.", reply_markup=rm)


def echo(update, context):
    update.message.reply_text('Сообщение: "' + update.message.text + '"')


botUpdater = Updater(TOKEN)

botDispatcher = botUpdater.dispatcher
botDispatcher.add_handler(CommandHandler("start", start))
botDispatcher.add_handler(MessageHandler(Filters.text, echo))

botUpdater.start_polling()
botUpdater.idle()
