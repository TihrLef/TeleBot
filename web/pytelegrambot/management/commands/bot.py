from datetime import date, datetime

from isoweek import Week

from telegram.ext import Updater, Handler, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.utils.request import Request

from django.core.management.base import BaseCommand
from django.conf import settings

from Users.models import User
from Projects.models import Project
from Reports.models import Report

WEEK_SELECTION, ACTION_CHOICE, PROCESSING_ACTION, ADDING_REP, EDITING_REP, DELETING_REP = range(6)
USER_NOT_CONFIRMED, USER_CONFIRMED = range(2)


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
    return USER_NOT_CONFIRMED


@log_errors
def userNotConfirmed(update, _):
    telegram_user = update.message.from_user

    user = User.objects.get(
        telegram_id=telegram_user.id
    )

    if user.is_active:
        return userConfirmed(update, _)

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
                                       "\nОтправьте /reports для добавления отчета."
    )

    return ConversationHandler.END


@log_errors
def projectSelect(update, context):
    if update.message: # Первый заход
        telegram_user = update.effective_message.from_user
        user = User.objects.get(
            telegram_id=telegram_user.id
        )
        context.chat_data["user"] = user
    else: #Возвращение назад
        user = context.chat_data["user"]

    projectsList = user.project_set.all()
    if not projectsList:
        context.bot.send_message(update.effective_chat.id, "У вас нет активных проектов.")
        return ConversationHandler.END

    inlineButtons = [
        [InlineKeyboardButton(str(project.name), callback_data=str(project.id))]
        for project in projectsList
    ]

    inlineMarkup = InlineKeyboardMarkup(inlineButtons)

    if update.effective_message.text == "/reports":
        context.bot.send_message(update.effective_chat.id, "Выберите проект:", reply_markup=inlineMarkup)
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text("Выберите проект:", reply_markup=inlineMarkup)

    return WEEK_SELECTION


def week_to_str(week):
    return week.monday().strftime("%d.%m.%Y") + " - " + week.sunday().strftime("%d.%m.%Y")


@log_errors
def weekSelect(update, context):
    query = update.callback_query
    query.answer()

    if query.data != 'back_to_weeks':
        project = context.chat_data["project"] = Project.objects.get(pk=int(query.data))
    else:
        project = context.chat_data["project"]

    start_date = project.start_date

    end_date = project.end_date if project.end_date else date.today()

    start_week = Week.withdate(start_date)
    end_week = Week.withdate(end_date)

    weeks_num = end_week.week - start_week.week + 1

    weeks = [start_week + i for i in range(weeks_num)]

    inlineButtons = [
        [InlineKeyboardButton(week_to_str(week), callback_data=str(week))]
        for week in weeks
    ]
    inlineButtons.append(  # Путь назад
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
    return ACTION_CHOICE


#
# @log_errors
# def reportSelect(update, context):
#     query = update.callback_query
#     query.answer()
#     week = context.chat_data["week"]
#     project = context.chat_data["project"]
#     user = context.chat_data["user"]
#     if query.data == 'add':
#         # добавление
#         free_days = get_days_without_reports(week, project, user)
#         inlineButtons = [
#             [InlineKeyboardButton(day.strftime("%d.%m.%Y"), callback_data=day.strftime("%d.%m.%Y"))]
#             for day in free_days
#         ]
#         inlineButtons.append([InlineKeyboardButton("Назад", callback_data='back_to_actions')])
#
#         inlineMarkup = InlineKeyboardMarkup(inlineButtons)
#
#         if len(free_days) != 0:
#             query.edit_message_text(
#                 'Выбран проект "' + project.name + '"'
#                 'Неделя "' + week_to_str(week) + '"'
#                 '\nВыберите дату:', reply_markup=inlineMarkup)
#             return ADDING_REP
#
#         query.edit_message_text(
#             'Нет возможности добавить новый отчет на этой неделе',
#             reply_markup=inlineMarkup)
#         return ACTION_CHOICE
#     else: #изменение или удаление
#         existing_reports = get_existing_reports(week, project, user)
#
#         inlineButtons = [
#             [InlineKeyboardButton(report.report_date.strftime("%d.%m.%Y"), callback_data=report.id)]
#             for report in existing_reports
#         ]
#
#         inlineButtons.append([InlineKeyboardButton("Назад", callback_data='back_to_actions')])
#
#         inlineMarkup = InlineKeyboardMarkup(inlineButtons)
#         if len(existing_reports) != 0:
#             query.edit_message_text(
#                 'Выбран проект "' + project.name + '"'
#                 'Неделя ' + week_to_str(week) +
#                 '\nВыберите дату:', reply_markup=inlineMarkup)
#             return DELETING_REP if query.data == 'remove' else EDITING_REP
#
#         # Если не нашлись отчеты
#         query.edit_message_text(
#             'Нет отчетов на этой неделе',
#             reply_markup=inlineMarkup)
#         return ACTION_CHOICE

def menu(update, context):
    query = update.callback_query
    query.answer()

    if query.data != 'back_to_menu':

        week = context.chat_data["week"] = Week.fromstring(query.data)
    else:
        week = context.chat_data["week"]
    user = context.chat_data["user"]
    project = context.chat_data["project"]

    inlineButtons = []

    try:
        report = Report.objects.get(
            user=user,
            project=project,
            report_date=week.monday()
        )
        inlineButtons.extend(
            [
                [InlineKeyboardButton("Изменить отчет", callback_data="edit")],
                [InlineKeyboardButton("Удалить отчет", callback_data="remove")],
            ]
        )
    except Report.DoesNotExist:
        inlineButtons.append(
            [InlineKeyboardButton("Добавить отчет", callback_data="add")]
        )

    inlineButtons.extend(
        [
            [InlineKeyboardButton("Вернуться к списку недель", callback_data="back_to_weeks")],
            [InlineKeyboardButton("Готово", callback_data="complete")]
        ]
    )
    inlineMarkup = InlineKeyboardMarkup(inlineButtons)

    msg = update.effective_message.text
    query.edit_message_text(msg[:msg.find('\n')] +
                            "\nНеделя: " + week_to_str(week) +
                            "\nВыберите действие, которое необходимо совершить:", reply_markup=inlineMarkup)

    return PROCESSING_ACTION


def addRequest(update, context):
    query = update.callback_query
    query.answer()
    project = context.chat_data["project"]
    user = context.chat_data["user"]
    week = context.chat_data["week"]

    query.edit_message_text('Выбран проект: "' + project.name + '"'
                            "\nНеделя: " + week_to_str(week) +
                            "\nВведите текст отчёта")

    return ADDING_REP


def addReport(update, context):

    project = context.chat_data["project"]
    user = context.chat_data["user"]
    week = context.chat_data["week"]

    message = update.message.text

    report = Report.objects.create(
        project=project,
        user=user,
        report_date=week.monday(),
        message=message
    )
    #TODO Проверка, что report успешно сохранился
    update.message.reply_text(f'Успешно добавлен отчет на проект: {project.name}\n'
                              f'Неделя: {week_to_str(week)}\n'
                              f'Текст: {report.message}\n'
                              )

    return ConversationHandler.END


def editRequest(update, context):

    query = update.callback_query
    query.answer()
    project = context.chat_data["project"]
    user = context.chat_data["user"]
    week = context.chat_data["week"]

    report = Report.objects.get(
        project=project,
        user=user,
        report_date=week.monday()
    )

    inline_button = [[InlineKeyboardButton("Отменить", callback_data="back_to_menu")]]
    inline_markup = InlineKeyboardMarkup(inline_button)
    query.edit_message_text('Выбран проект: "' + project.name + '"'
                            "\nНеделя: " + week_to_str(week) +
                            "\nТекущий текст: " + report.message +
                            "\nВведите новый текст отчёта", reply_markup=inline_markup)
    return EDITING_REP


def editReport(update, context):

    project = context.chat_data["project"]
    user = context.chat_data["user"]
    week = context.chat_data["week"]

    message = update.message.text

    report = Report.objects.get(
        project=project,
        user=user,
        report_date=week.monday()
    )
    report.message = message
    report.save()

    update.message.reply_text(f'Успешно добавлен отчет на проект: {project.name}\n'
                              f'Неделя: {week_to_str(week)}\n'
                              f'Текст: {report.message}\n'
                              )

    return ConversationHandler.END




def deleteRequest(update, context):

    query = update.callback_query
    query.answer()
    project = context.chat_data["project"]
    user = context.chat_data["user"]
    week = context.chat_data["week"]

    report = Report.objects.get(
        project=project,
        user=user,
        report_date=week.monday()
    )

    inline_button = [
        [InlineKeyboardButton("Да", callback_data="delete"), InlineKeyboardButton("Нет", callback_data="back_to_menu")]
    ]
    inline_markup = InlineKeyboardMarkup(inline_button)
    query.edit_message_text('Выбран проект: "' + project.name + '"'
                                                                "\nНеделя: " + week_to_str(week) +
                            "\nТекущий текст: " + report.message +
                            "\nВы уверены, что хотите удалить отчет?", reply_markup=inline_markup)
    return DELETING_REP


def deleteReport(update, context):
    query = update.callback_query
    query.answer()

    project = context.chat_data["project"]
    user = context.chat_data["user"]
    week = context.chat_data["week"]

    report = Report.objects.get(
        project=project,
        user=user,
        report_date=week.monday()
    )

    report.delete()
    query.edit_message_text('Проект: "' + project.name + '"'
                            "\nНеделя: " + week_to_str(week) +
                            "\nОтчет удален")

    return ConversationHandler.END


def completeChanging(update, _):
    update.effective_message.reply_text("Все изменения успешно сохранены.")
    return ConversationHandler.END


def returnToWeeks(update, _):
    return ConversationHandler.END


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

        userIdentification = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                USER_NOT_CONFIRMED: [
                    MessageHandler(Filters.all, userNotConfirmed)
                ],
                USER_CONFIRMED: [
                    MessageHandler(Filters.all, userConfirmed)
                ]
            },
            fallbacks=[CommandHandler("reports", projectSelect)]
        )

        conversationWithUser = ConversationHandler(
            entry_points=[CommandHandler("reports", projectSelect)],
            states={
                WEEK_SELECTION: [
                    CallbackQueryHandler(weekSelect)
                ],
                ACTION_CHOICE: [
                    CallbackQueryHandler(projectSelect, pattern='^' + "back_to_projects" + '$'),
                    CallbackQueryHandler(menu)
                ],
                PROCESSING_ACTION: [
                    CallbackQueryHandler(addRequest, pattern='^' + "add" + '$'),
                    CallbackQueryHandler(editRequest, pattern='^' + "edit" + '$'),
                    CallbackQueryHandler(deleteRequest, pattern='^' + "remove" + '$'),
                    CallbackQueryHandler(weekSelect, pattern='^' + "back_to_weeks" + '$'),
                    CallbackQueryHandler(completeChanging, pattern='^' + "complete" + '$')
                ],
                ADDING_REP: [
                    #CallbackQueryHandler(addRequest, pattern='^' + "add" + '$'),
                    MessageHandler(Filters.text, addReport)
                    # CallbackQueryHandler(addReport)
                ],
                EDITING_REP: [
                    #CallbackQueryHandler(editingReport),
                    MessageHandler(Filters.text, editReport),
                    CallbackQueryHandler(menu, pattern="^back_to_menu$")
                    # CallbackQueryHandler(editReport)
                ],
                DELETING_REP: [
                    CallbackQueryHandler(deleteReport, pattern="^delete$"),
                    CallbackQueryHandler(menu, pattern="^back_to_menu$")
                ]
            },
            fallbacks=[CommandHandler("reports", projectSelect)]
        )

        # Conversations
        botDispatcher.add_handler(userIdentification)
        botDispatcher.add_handler(conversationWithUser)

        # Running the bot
        # 3 - Бесконечная обработка сообщений

        botUpdater.start_polling()
        botUpdater.idle()
