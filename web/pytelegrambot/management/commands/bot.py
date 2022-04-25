from datetime import date

from  isoweek import Week

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.utils.request import Request

from django.core.management.base import BaseCommand
from django.conf import settings

from Users.models import User
from Projects.models import Project
from Reports.models import Report

FIRST, SECOND, THIRD = range(3)
USER_NOT_FOUND, USER_NOT_CONFIRMED, USER_CONFIRMED = range(3)


# Декоратор для логирования ошибок
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
    telegram_user = update.message.from_user

    try:
        user = User.objects.get(telegram_id=telegram_user.id)  # Finding user

        if user.is_active:
            return userConfirmed(update, _)

        return userNotConfirmed(update, _)

    except User.DoesNotExist:  # user is new
        return userNotFound(update, _)


@log_errors
def userNotFound(update, _):
    telegram_user = update.message.from_user

    new_user = User.objects.create(
        is_active=False,
        telegram_id=telegram_user.id,
    )

    update.message.reply_text(
        "К сожалению, вас нет в списке участников какого-либо проекта."
        "\n Мы создали Вам неподтвержденный аккаунт."
        "\n Ваш персональный токен: " + str(new_user.personal_token)

    )
    return USER_NOT_FOUND


@log_errors
def userNotConfirmed(update, _):
    telegram_user = update.message.from_user

    user = User.objects.get(
        telegram_id=telegram_user.id
    )

    update.message.reply_text(
        "К сожалению, администратор ещё не проверил ваш аккаунт."
        "\nОжидайте проверки и назначения проектов."
        "\nВаш персональный токен: " + str(user.personal_token)
    )
    return USER_NOT_CONFIRMED


@log_errors
def userConfirmed(update, _):
    telegram_user = update.message.from_user

    user = User.objects.get(
        telegram_id=telegram_user.id
    )

    update.message.reply_text(
        "Привет, " + user.first_name + "!"
        "\nЭтот бот предназначен для управления существующими проектами. "
        "\nОтправьте /addreport для добавления отчета."
    )

    return ConversationHandler.END


@log_errors
def projectSelect(update, context):
    # TODO НУЖНО ПОЛУЧАТЬ ТОЛЬКО ПРОЕКТЫ ПОЛЬЗОВАТЕЛЯ!!!
    telegram_user = update.effective_message.from_user
    user = User.objects.get(
        telegram_id=telegram_user.id
    )

    projectsList = user.project_set.all()

    inlineButtons = [
        [InlineKeyboardButton(str(project.name), callback_data=project.pk)]
        for project in projectsList
    ]

    inlineMarkup = InlineKeyboardMarkup(inlineButtons)

    if update.effective_message.text == "/addreport":
        context.bot.send_message(update.effective_chat.id, "Выберите проект:", reply_markup=inlineMarkup)
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text("Выберите проект:", reply_markup=inlineMarkup)

    return FIRST


@log_errors
def weekSelect(update, _):
    query = update.callback_query
    query.answer()

    project_pk = int(query.data)

    project = Project.objects.get(
        id=project_pk
    )

    start_date = project.start_date
    end_date = project.end_date if project.end_date else date.today()

    start_week = Week.withdate(start_date)
    end_week = Week.withdate(end_date)

    weeks_num = end_week.week - start_week.week + 1

    weeks = [start_week + i for i in range(weeks_num)]

    # TODO Сгенерировать список недель, по которым возомжно оставить отчет

    inlineButtons = [
        [InlineKeyboardButton(week.monday().strftime("%d.%m.%Y") + " - " + week.sunday().strftime("%d%m%Y"), callback_data=str(week))]
        for week in weeks
    ]
    inlineButtons.append( #Путь назад
        [InlineKeyboardButton("Вернуться к выбору проекта", callback_data="back_to_projects")]
    )
    inlineMarkup = InlineKeyboardMarkup(inlineButtons)

    if query.data == "back_to_weeks":
        msg = update.effective_message.text
        query.edit_message_text(msg[:msg.find('\n')] +
                                '\nВыберите дату:', reply_markup=inlineMarkup)
    else:
        query.edit_message_text('Выбран проект "' + project.name + '"'
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

    def handle(self, *args, **options):
        # 1 -- правильное подключение
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )

        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )

        # 2 -- обработчики
        botUpdater = Updater(
            bot=bot,
            use_context=True,
        )
        botDispatcher = botUpdater.dispatcher

        # Commands
        """start_handler = CommandHandler("start", start)
        botDispatcher.add_handler(start_handler)"""

        userIdentification = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                USER_NOT_FOUND: [
                    MessageHandler(Filters.all, userNotFound)
                ],
                USER_NOT_CONFIRMED: [
                    MessageHandler(Filters.all, userNotConfirmed)
                ],
                USER_CONFIRMED: [
                    MessageHandler(Filters.text("ggg"), userConfirmed)
                ]
            },
            fallbacks=[CommandHandler("addreport", projectSelect)]
        )

        conversationWithUser = ConversationHandler(
            entry_points=[CommandHandler("addreport", projectSelect)],
            states={
                FIRST: [
                    CallbackQueryHandler(weekSelect),
                ],
                SECOND: [
                    CallbackQueryHandler(menu, pattern='^' + "first" + '$'),
                    CallbackQueryHandler(projectSelect, pattern='^' + "back_to_projects" + '$')
                ],
                THIRD: [
                    CallbackQueryHandler(addReport, pattern='^' + "add" + '$'),
                    CallbackQueryHandler(editReport, pattern='^' + "edit" + '$'),
                    CallbackQueryHandler(removeReport, pattern='^' + "remove" + '$'),
                    CallbackQueryHandler(weekSelect, pattern='^' + "back_to_weeks" + '$'),
                    CallbackQueryHandler(completeChanging, pattern='^' + "complete" + '$')
                ]
            },
            fallbacks=[CommandHandler("addreport", projectSelect)]
        )

        # Conversations
        botDispatcher.add_handler(userIdentification)
        botDispatcher.add_handler(conversationWithUser)

        # Running the bot
        # 3 - Бесконечная обработка сообщений

        botUpdater.start_polling()
        botUpdater.idle()
