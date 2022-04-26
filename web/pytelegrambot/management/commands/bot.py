from datetime import date

from Projects.models import Project
from Reports.models import Report
from Users.models import User
from django.conf import settings
from django.core.management.base import BaseCommand
from isoweek import Week
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram.utils.request import Request

WEEK_SELECTION, ACTION_CHOICE, PROCESSING_ACTION, ADDING_REP, EDITING_REP, DELETING_REP, TO_MENU = range(7)
USER_NOT_CONFIRMED, USER_CONFIRMED = range(2)


def help(update, _):
    update.message.reply_text("Этот бот предназначен для создания, редактирования и удаления отчетов к проектам."
                              "\n\n/start - регистрация/вход в систему."
                              "\n/reports - выбор отчета и манипуляции.")

    return ConversationHandler.END


def start(update, _):
    telegram_user = update.message.from_user

    try:
        user = User.objects.get(telegram_id=telegram_user.id)  # Finding user

        if user.is_active:
            return user_confirmed(update, _)

        return user_not_confirmed(update, _)

    except User.DoesNotExist:  # user is new
        return user_not_found(update, _)


def user_not_found(update, _):
    telegram_user = update.message.from_user

    new_user = User.objects.create(
        is_active=False,
        telegram_id=telegram_user.id,
    )

    update.message.reply_text(
        "К сожалению, вас нет в списке участников какого-либо проекта."
        "\nМы создали Вам неподтвержденный аккаунт."
        "\nВаш персональный токен: " + str(new_user.personal_token) + "."
        "\n\nОтправьте /help для получения информации о боте."
    )
    return USER_NOT_CONFIRMED


def user_not_confirmed(update, _):
    telegram_user = update.message.from_user

    user = User.objects.get(
        telegram_id=telegram_user.id
    )

    if user.is_active:
        return user_confirmed(update, _)

    update.message.reply_text(
        "К сожалению, администратор ещё не проверил ваш аккаунт."
        "\nОжидайте проверки и назначения проектов."
        "\nВаш персональный токен: " + str(user.personal_token) + "."
        "\n\nОтправьте /help для получения информации о боте."
    )
    return USER_NOT_CONFIRMED


def user_confirmed(update, _):
    telegram_user = update.message.from_user

    user = User.objects.get(
        telegram_id=telegram_user.id
    )

    update.message.reply_text(
        "Привет, " + user.first_name + "!"
        "\nОтправьте /reports для добавления отчета."
        "\n\nОтправьте /help для получения информации о боте."
    )

    return ConversationHandler.END


def project_select(update, context):
    if update.message:  # Первый заход
        telegram_user = update.effective_message.from_user
        user = User.objects.get(
            telegram_id=telegram_user.id
        )
        context.chat_data["user"] = user
    else:  # Возвращение назад
        user = context.chat_data["user"]

    projects_list = user.project_set.all()
    if not projects_list:
        context.bot.send_message(update.effective_chat.id, "У вас нет активных проектов.")
        return ConversationHandler.END

    inline_buttons = [
        [InlineKeyboardButton(str(project.name), callback_data=str(project.id))]
        for project in projects_list
    ]

    inline_markup = InlineKeyboardMarkup(inline_buttons)

    if update.effective_message.text == "/reports":
        context.bot.send_message(update.effective_chat.id, "Выберите проект:", reply_markup=inline_markup)
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text("Выберите проект:", reply_markup=inline_markup)

    return WEEK_SELECTION


def week_to_str(week):
    return week.monday().strftime("%d.%m.%Y") + " - " + week.sunday().strftime("%d.%m.%Y")


def week_select(update, context):
    query = update.callback_query
    query.answer()

    if query.data != 'back_to_weeks':
        project = context.chat_data["project"] = Project.objects.get(pk=int(query.data))
    else:
        project = context.chat_data["project"]
    user = context.chat_data["user"]

    start_date = project.start_date

    end_date = project.end_date if project.end_date else date.today()

    start_week = Week.withdate(start_date)
    end_week = Week.withdate(end_date)

    weeks_num = end_week.week - start_week.week + 1

    weeks = [start_week + i for i in range(weeks_num)]

    inline_buttons = []
    for week in weeks:
        try:
            Report.objects.get(
                project=project,
                user=user,
                report_date=week.monday()
            )
            report_exist = True
        except Report.DoesNotExist:
            report_exist = False

        inline_buttons.append(
            [InlineKeyboardButton(week_to_str(week) + (" ✅ " if report_exist else " ❌ "), callback_data=str(week))]
        )

    inline_buttons.append(  # Путь назад
        [InlineKeyboardButton("Вернуться к выбору проекта", callback_data="back_to_projects")]
    )
    inline_markup = InlineKeyboardMarkup(inline_buttons)

    query.edit_message_text('Выбран проект "' + project.name + '"'
                                                               '\nВыберите дату:', reply_markup=inline_markup)

    return ACTION_CHOICE


def menu(update, context):
    query = update.callback_query
    query.answer()

    if query.data != 'back_to_menu':

        week = context.chat_data["week"] = Week.fromstring(query.data)
    else:
        week = context.chat_data["week"]
    user = context.chat_data["user"]
    project = context.chat_data["project"]

    inline_buttons = []

    try:
        Report.objects.get(
            user=user,
            project=project,
            report_date=week.monday()
        )
        inline_buttons.extend(
            [
                [InlineKeyboardButton("Изменить отчет", callback_data="edit")],
                [InlineKeyboardButton("Удалить отчет", callback_data="remove")],
            ]
        )
    except Report.DoesNotExist:
        inline_buttons.append(
            [InlineKeyboardButton("Добавить отчет", callback_data="add")]
        )

    inline_buttons.extend(
        [
            [InlineKeyboardButton("Вернуться к списку недель", callback_data="back_to_weeks")],
            [InlineKeyboardButton("Готово", callback_data="complete")]
        ]
    )
    inline_markup = InlineKeyboardMarkup(inline_buttons)

    msg = update.effective_message.text
    query.edit_message_text(msg[:msg.find('\n')] +
                            "\nНеделя: " + week_to_str(week) +
                            "\nВыберите действие, которое необходимо совершить:", reply_markup=inline_markup)

    return PROCESSING_ACTION


def add_request(update, context):
    query = update.callback_query
    query.answer()
    project = context.chat_data["project"]

    week = context.chat_data["week"]

    query.edit_message_text('Выбран проект: "' + project.name + '"'
                                                                "\nНеделя: " + week_to_str(week) +
                            "\nВведите текст отчёта")

    return ADDING_REP


def add_report(update, context):
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

    inline_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Ок", callback_data="back_to_menu")]])

    # TODO Проверка, что report успешно сохранился
    update.message.reply_text(f'Успешно добавлен отчет на проект: {project.name}\n'
                              f'Неделя: {week_to_str(week)}\n'
                              f'Текст: {report.message}\n', reply_markup=inline_markup)

    return ACTION_CHOICE


def edit_request(update, context):
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

    inline_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Ок", callback_data="back_to_menu")]])

    update.message.reply_text(f'Успешно изменён отчет на проект: {project.name}\n'
                              f'Неделя: {week_to_str(week)}\n'
                              f'Текст: {report.message}\n', reply_markup=inline_markup)

    return TO_MENU


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

    inline_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Ок", callback_data="back_to_menu")]])

    query.edit_message_text('Проект: "' + project.name + '"'
                            "\nНеделя: " + week_to_str(week) +
                            "\nОтчет удален", reply_markup=inline_markup)

    return TO_MENU


def completeChanging(update, _):
    query = update.callback_query
    query.answer()

    query.edit_message_text("Все изменения успешно сохранены.")
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
        bot_updater = Updater(
            bot=bot,
            use_context=True,
        )
        bot_dispatchder = bot_updater.dispatcher

        help_command = CommandHandler("help", help)

        user_identification = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                USER_NOT_CONFIRMED: [
                    MessageHandler(Filters.all, user_not_confirmed)
                ],
                USER_CONFIRMED: [
                    MessageHandler(Filters.all, user_confirmed)
                ]
            },
            fallbacks=[CommandHandler("help", help)]
        )

        conversation_with_user = ConversationHandler(
            entry_points=[CommandHandler("reports", project_select)],
            states={
                WEEK_SELECTION: [
                    CallbackQueryHandler(week_select)
                ],
                ACTION_CHOICE: [
                    CallbackQueryHandler(project_select, pattern='^' + "back_to_projects" + '$'),
                    CallbackQueryHandler(menu)
                ],
                PROCESSING_ACTION: [
                    CallbackQueryHandler(add_request, pattern='^' + "add" + '$'),
                    CallbackQueryHandler(edit_request, pattern='^' + "edit" + '$'),
                    CallbackQueryHandler(deleteRequest, pattern='^' + "remove" + '$'),
                    CallbackQueryHandler(week_select, pattern='^' + "back_to_weeks" + '$'),
                    CallbackQueryHandler(completeChanging, pattern='^' + "complete" + '$')
                ],
                ADDING_REP: [
                    MessageHandler(Filters.text, add_report)
                ],
                EDITING_REP: [
                    MessageHandler(Filters.text, editReport),
                    CallbackQueryHandler(menu, pattern="^back_to_menu$")
                ],
                DELETING_REP: [
                    CallbackQueryHandler(deleteReport, pattern="^delete$"),
                    CallbackQueryHandler(menu, pattern="^back_to_menu$")
                ],
                TO_MENU: [
                    CallbackQueryHandler(menu, pattern="^back_to_menu$")
                ]
            },
            fallbacks=[CommandHandler("help", help)]
        )

        # Conversations
        bot_dispatchder.add_handler(help_command)
        bot_dispatchder.add_handler(user_identification)
        bot_dispatchder.add_handler(conversation_with_user)

        # Running the bot
        # 3 - Бесконечная обработка сообщений

        bot_updater.start_polling()
        bot_updater.idle()
