from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .config import TOKEN
from django.core.management.base import BaseCommand
from Users.models import User
from Projects.models import Project
from Reports.models import Report


def start(update, _):
    user = update.message.from_user
    update.message.reply_text("Привет, " + user.first_name +
                              "\nЭтот бот предназначен для управления существующими проектами."
                              "\nОтправьте /addreport для добавления отчета.")


def projectSelect(update, callback):
    inlineButtons = [
        [InlineKeyboardButton("Создание бота", callback_data="bot")],
        [InlineKeyboardButton("Создание веб-интерфейса", callback_data="web")]
    ]
    inlineMarkup = InlineKeyboardMarkup(inlineButtons)

    callback.bot.send_message(update.effective_chat.id, "Выберите проект:", reply_markup=inlineMarkup)
    """update.message.reply_text("Выберите проект:", reply_markup=inlineMarkup)"""


def botProject(update, callback):
    query = update.callback_query
    query.answer()
    query.edit_message_text('Выбран проект "Создание бота"')

    inlineButtons = [
        [InlineKeyboardButton("11.04.2022-16.04.2022", callback_data="first")],
        [InlineKeyboardButton("Вернуться к выбору проекта", callback_data="return_to_project")]
    ]
    inlineMarkup = InlineKeyboardMarkup(inlineButtons)

    callback.bot.send_message(update.effective_chat.id, "Выберите дату:", reply_markup=inlineMarkup)

    return 2


def menu(update, callback):
    query = update.callback_query
    query.answer()
    query.edit_message_text("Дата: хх.хх.хххх")

    inlineButtons = [
        [InlineKeyboardButton("Добавить отчет", callback_data="add")],
        [InlineKeyboardButton("Изменить отчет", callback_data="edit")],
        [InlineKeyboardButton("Удалить отчет", callback_data="remove")],
        [InlineKeyboardButton("Вернуться к списку недель", callback_data="back_to_weeks")]
    ]
    inlineMarkup = InlineKeyboardMarkup(inlineButtons)

    callback.bot.send_message(update.effective_chat.id, "Выберите действие, которое необходимо совершить:",
                              reply_markup=inlineMarkup)

    return 1


def addReport(report):
    report.save() #Сохраняет отчёт в БД


def removeReport(report):
    report.delete() #Удаляет отчёт из БД


def editReport(report, message):
    report.message = message
    report.save() #Изменяет отчёт БД


def returnToWeeks(update, _):
    return ConversationHandler.END


def echo(update, _):
    update.message.reply_text('Сообщение: "' + update.message.text + '"')

class Command(BaseCommand):
    botUpdater = Updater(TOKEN)

    botDispatcher = botUpdater.dispatcher
    botDispatcher.add_handler(CommandHandler("start", start))
    botDispatcher.add_handler(CommandHandler("addreport", projectSelect))
    botDispatcher.add_handler(CallbackQueryHandler(projectSelect, pattern='^' + "return_to_project" + '$'))

    menuConversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(botProject, pattern='^' + "bot" + '$')],
        states={
            1: [
                CallbackQueryHandler(addReport, pattern='^' + "add" + '$'),
                CallbackQueryHandler(editReport, pattern='^' + "edit" + '$'),
                CallbackQueryHandler(removeReport, pattern='^' + "remove" + '$'),
                CallbackQueryHandler(returnToWeeks, pattern='^' + "return_to_weeks" + '$')
            ],
            2: [
                CallbackQueryHandler(menu, pattern='^' + "first" + '$')
            ]
        },
        fallbacks=[CallbackQueryHandler(botProject)]
    )
    botDispatcher.add_handler(menuConversation)

    botUpdater.start_polling()
    botUpdater.idle()



