import sys

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.utils.request import Request

from django.core.management.base import BaseCommand
from django.conf import settings

from Users.models import User
from Projects.models import Project
from Reports.models import Report

FIRST, SECOND, THIRD = range(3)


#Декоратор для логирования ошибок
def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка {e}'
            print(error_message)
            raise e
    return inner


@log_errors
def start(update, _):
    #TODO найти пользователя в БД по его телеге
    #Если не нашелся - послать нахуй
    user = update.message.from_user
    update.message.reply_text("Привет, " + user.first_name + "!"
                                                             "\nЭтот бот предназначен для управления существующими проектами."
                                                             "\nОтправьте /addreport для добавления отчета.")


@log_errors
def projectSelect(update, context):
    # TODO НУЖНО ПОЛУЧАТЬ ТОЛЬКО ПРОЕКТЫ ПОЛЬЗОВАТЕЛЯ!!!
    projectsList = Project.objects.all()

    print([project.name for project in projectsList])
    inlineButtons = [
        [InlineKeyboardButton(str(project.name), callback_data=project.pk)]
        for project in projectsList
    ]
    # inlineButtons = [
    #     [InlineKeyboardButton("Создание бота", callback_data="bot")],
    #     [InlineKeyboardButton("Создание веб-интерфейса", callback_data="web")]
    # ]
    inlineMarkup = InlineKeyboardMarkup(inlineButtons)

    if update.effective_message.text == "/addreport":
        context.bot.send_message(update.effective_chat.id, "Выберите проект:", reply_markup=inlineMarkup)
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text("Выберите проект:", reply_markup=inlineMarkup)

    return FIRST


@log_errors
def botProject(update, _):
    query = update.callback_query
    query.answer()

    #TODO Сгенерировать список недель, по которым возомжно оставить отчет
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


def addReport(report):
    report.save()  # Сохраняет отчёт в БД


def removeReport(report):
    report.delete()  # Удаляет отчёт из БД


def editReport(report, message):
    report.message = message
    report.save()  # Изменяет отчёт БД


def completeChanging(update, _):
    update.effective_message.reply_text("Все изменения успешно сохранены.")
    return ConversationHandler.END


def returnToWeeks(update, _):
    return ConversationHandler.END


def echo(update, _):
    update.message.reply_text('Сообщение: "' + update.message.text + '"')




class Command(BaseCommand):
    help = 'Телеграм-бот'
    # 1 -- правильное подключение
    request = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )

    bot = Bot(
        request=request,
        token=settings.TOKEN,
    )

    #2 -- обработчики
    botUpdater = Updater(
        bot=bot,
        use_context=True,
    )
    botDispatcher = botUpdater.dispatcher

    # Commands
    start_handler = CommandHandler("start", start)
    botDispatcher.add_handler(start_handler)

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
    # 3 - Бесконечная обработка сообщений

    botUpdater.start_polling()
    botUpdater.idle()