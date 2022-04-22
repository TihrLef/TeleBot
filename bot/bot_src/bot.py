from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN


def start(update, _):
    user = update.message.from_user
    update.message.reply_text("Привет, " + user.first_name +
                              "\nЭтот бот предназначен для управления существующими проектами."
                              "\nОтправьте /addreport для добавления отчета.")


def projectSelect(update, _):
    inlineButtons = [
        [InlineKeyboardButton("Создание бота", callback_data="bot")],
        [InlineKeyboardButton("Создание веб-интерфейса", callback_data="web")]
    ]
    inlineMarkup = InlineKeyboardMarkup(inlineButtons)

    update.message.reply_text("Выберите проект:", reply_markup=inlineMarkup)


def botProject(update, callback):
    query = update.callback_query
    query.answer()

    query.edit_message_text('Выбран проект "Создание бота"')

    inlineButtons = [
        [InlineKeyboardButton("11.04.2022-16.04.2022", callback_data="first")]
    ]
    inlineMarkup = InlineKeyboardMarkup(inlineButtons)

    callback.bot.send_message(update.effective_chat.id, "Выберите дату:", reply_markup=inlineMarkup)


def echo(update, _):
    update.message.reply_text('Сообщение: "' + update.message.text + '"')


def main():
    botUpdater = Updater(TOKEN)

    botDispatcher = botUpdater.dispatcher
    botDispatcher.add_handler(CommandHandler("start", start))
    botDispatcher.add_handler(CommandHandler("addreport", projectSelect))
    botDispatcher.add_handler(CallbackQueryHandler(botProject, pattern='^' + "bot" + '$'))

    botUpdater.start_polling()
    botUpdater.idle()


if __name__ == "__main__":
    main()
