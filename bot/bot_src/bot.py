from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN

FIRST, SECOND, THIRD = range(3)


def start(update, _):
    user = update.message.from_user
    update.message.reply_text("Привет, " + user.first_name +
                              "\nЭтот бот предназначен для управления существующими проектами."
                              "\nОтправьте /addreport для добавления отчета.")


def projectSelect(update, context):
    inlineButtons = [
        [InlineKeyboardButton("Создание бота", callback_data="bot")],
        [InlineKeyboardButton("Создание веб-интерфейса", callback_data="web")]
    ]
    inlineMarkup = InlineKeyboardMarkup(inlineButtons)

    if update.effective_message.text == "/addreport":
        context.bot.send_message(update.effective_chat.id, "Выберите проект:", reply_markup=inlineMarkup)
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text("Выберите проект:", reply_markup=inlineMarkup)

    return FIRST


def botProject(update, _):
    query = update.callback_query
    query.answer()

    inlineButtons = [
        [InlineKeyboardButton("11.04.2022-16.04.2022", callback_data="first")],
        [InlineKeyboardButton("Вернуться к выбору проекта", callback_data="back_to_projects")]
    ]
    inlineMarkup = InlineKeyboardMarkup(inlineButtons)

    if query.data == "back_to_weeks":
        msg = update.effective_message.text
        query.edit_message_text(msg[:msg.find('\n')] +
                                '\nВыберите дату:', reply_markup=inlineMarkup)
    else:
        query.edit_message_text('Выбран проект "Создание бота"'
                                '\nВыберите дату:', reply_markup=inlineMarkup)

    # context.bot.send_message(update.effective_chat.id, "Выберите дату:", reply_markup=inlineMarkup)

    return SECOND


def menu(update, _):
    query = update.callback_query
    query.answer()

    inlineButtons = [
        [InlineKeyboardButton("Добавить отчет", callback_data="add")],
        [InlineKeyboardButton("Изменить отчет", callback_data="edit")],
        [InlineKeyboardButton("Удалить отчет", callback_data="remove")],
        [InlineKeyboardButton("Вернуться к списку недель", callback_data="back_to_weeks")],
        [InlineKeyboardButton("Готово", callback_data="complete")]
    ]
    inlineMarkup = InlineKeyboardMarkup(inlineButtons)

    msg = update.effective_message.text
    query.edit_message_text(msg[:msg.find('\n')] +
                            "\nДата: хх.хх.хххх"
                            "\nВыберите действие, которое необходимо совершить:", reply_markup=inlineMarkup)
    # context.bot.send_message(update.effective_chat.id, "Выберите действие, которое необходимо совершить:",
    #                           reply_markup=inlineMarkup)

    return THIRD


def addReport(update, _):
    return THIRD


def removeReport(update, _):
    return THIRD


def editReport(update, _):
    return THIRD


def completeChanging(update, _):
    update.effective_message.reply_text("Все изменения успешно сохранены.")
    return ConversationHandler.END


def main():
    botUpdater = Updater(TOKEN)
    botDispatcher = botUpdater.dispatcher

    # Commands
    botDispatcher.add_handler(CommandHandler("start", start))

    conversationWithUser = ConversationHandler(
        entry_points=[CommandHandler("addreport", projectSelect)],
        states={
            FIRST: [
                CallbackQueryHandler(botProject, pattern='^' + "bot" + '$'),
                CallbackQueryHandler(botProject, pattern='^' + "web" + '$')
            ],
            SECOND: [
                CallbackQueryHandler(menu, pattern='^' + "first" + '$'),
                CallbackQueryHandler(projectSelect, pattern='^' + "back_to_projects" + '$')
            ],
            THIRD: [
                CallbackQueryHandler(addReport, pattern='^' + "add" + '$'),
                CallbackQueryHandler(editReport, pattern='^' + "edit" + '$'),
                CallbackQueryHandler(removeReport, pattern='^' + "remove" + '$'),
                CallbackQueryHandler(botProject, pattern='^' + "back_to_weeks" + '$'),
                CallbackQueryHandler(completeChanging, pattern='^' + "complete" + '$')
            ]
        },
        fallbacks=[CommandHandler("addreport", projectSelect)]
    )

    # Conversations
    botDispatcher.add_handler(conversationWithUser)

    # Running the bot
    botUpdater.start_polling()
    botUpdater.idle()


if __name__ == "__main__":
    main()
