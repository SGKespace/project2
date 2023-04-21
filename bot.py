import logging
from dotenv import load_dotenv

import aiosqlite

from datetime import date, datetime, timedelta
import calendar

import os
import common_helper_functions as chf
from typing import Dict
from telegram import __version__ as TG_VER
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


OK_PD, NOT_PD, CHOOSING, TYPING_REPLY, TYPING_CHOICE, START_ROUTES, END_ROUTES, FIO, ADRESS, CHARACTERISTICS, \
COMMENT, END_DATE, OK_DE, NOT_DE, DELIVERY = range(15)

DELIVERY_BY_COURIER = 0
FINAL_DATE = (1, 1, 1)
BEGIN_DATE = date(1, 1, 1)
TEXT_COMMENT = ' '
SPACE_FLOAT = 0
WEIGHT_FLOAT = 0
TEXT_ADRESS = ' '
TEXT_FIO = ' '
CHAT_ID = ' '
COUNT_MONTH = 1

reply_keyboard = [
    ["Help", "CreateOrder"],
    ["MyOrders", "Contacts"],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                             resize_keyboard=True, input_field_placeholder="Выберите категорию")


async def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])

    return date(year, month, day)


async def create_connection():
    db = await aiosqlite.connect(chf.user_db)
    cursor = await db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects';")
    if not await cursor.fetchone():
        await cursor.execute(chf.sql_create_ssf_table)
    return cursor, db


async def close_connection(conn):
    await conn[0].close()
    await conn[1].close()


async def add_event(n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13):  # Вставляем данные в таблицу
    event_ = (None, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13)
    async with aiosqlite.connect(chf.user_db) as db:
        await db.execute('INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', event_)
        await db.commit()


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    """ Вспомогательная функция для форматирования собранной информации о пользователе """

    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    await update.message.reply_text(chf.text_start, parse_mode="html", reply_markup=markup)
    return CHOOSING


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    """Запросите у пользователя информацию о выбранном предопределенном выборе."""
    text = update.message.text
    context.user_data["choice"] = text
    if text == 'Help':
        await update.message.reply_text(chf.text_help, parse_mode="html")
        # await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")
        return TYPING_REPLY
    if text == 'CreateOrder':
        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data=str(OK_PD)),
                InlineKeyboardButton("Нет", callback_data=str(NOT_PD)),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = "Создавая заказ вы соглашаетесь на обработку персональных данных. \n <b>" \
               "Я согласен на обработку персональных данных.</b>"
        await update.message.reply_text(text=text, parse_mode="html", reply_markup=reply_markup)

        return START_ROUTES


async def status_pd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data=str(OK_PD)),
            InlineKeyboardButton("Нет", callback_data=str(NOT_PD)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Создавая заказ вы соглашаетесь на обработку персональных данных. \n <b>" \
           "Я согласен на обработку персональных данных.</b>"
    await update.message.reply_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return START_ROUTES


async def ok_pd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    text = "Начнем заполнять анкету\n <b>" \
           "Введите полностью ваши фамилию Имя Отчество</b>"
    await query.edit_message_text(text=text, parse_mode="html")

    return FIO


async def fio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global TEXT_FIO, CHAT_ID, BEGIN_DATE
    TEXT_FIO = update.message.text
    CHAT_ID = update.message.chat.id
    BEGIN_DATE = update.message.date

    query = update.message

    text = " <b> Введите Ваш адрес и телефон для связис</b> "
    await query.reply_text(text=text, parse_mode="html")

    return ADRESS


async def adress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global TEXT_ADRESS
    TEXT_ADRESS = update.message.text

    query = update.message

    text = "  Введите примерные данные  в формате <b>объем / вес</b>.  Данные передать в метрах кубических и килограммах. " \
           "Если не можете рассчитать введите: <b> 0 / 0 </b> мы сами все измерим и скажем цену при сдаче вещей"
    await query.reply_text(text=text, parse_mode="html")
    return CHARACTERISTICS


async def characteristics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SPACE_FLOAT, WEIGHT_FLOAT
    text_characteristics = update.message.text
    try:
        SPACE_FLOAT = int(text_characteristics.partition('/')[0].replace(' ', ''))             #   объем хранимых вещей
    except:
        SPACE_FLOAT = 0
    try:
        WEIGHT_FLOAT = int(text_characteristics.partition('/')[2].replace(' ', ''))            #  вес хранимых вещей
    except:
        WEIGHT_FLOAT = 0

    query = update.message
    text = " <b>  Введите комментарий - обычно список вещей, ключевое слово - чтобы понять что сдали и т.д.</b>"
    await query.reply_text(text=text, parse_mode="html")

    return COMMENT


async def comment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global TEXT_COMMENT
    TEXT_COMMENT = update.message.text
    query = update.message
    text = " <b>  Введите количество месяцев хранения.</b>"
    await query.reply_text(text=text, parse_mode="html")
    return END_DATE


async def enddate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global FINAL_DATE, BEGIN_DATE
    COUNT_MONTH = int(update.message.text.replace(' ', ''))
    FINAL_DATE = await add_months(BEGIN_DATE, COUNT_MONTH)

    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data=str(OK_DE)),
            InlineKeyboardButton("Нет", callback_data=str(NOT_DE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = " <b> Я привезу свои вещи сам.</b>"
    await update.message.reply_text(text=text, parse_mode="html", reply_markup=reply_markup)
    query = update.callback_query
    # await query.answer()

    return DELIVERY


async def ok_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global DELIVERY_BY_COURIER, FINAL_DATE, BEGIN_DATE, TEXT_COMMENT, SPACE_FLOAT, WEIGHT_FLOAT, TEXT_ADRESS, \
        TEXT_FIO, CHAT_ID, COUNT_MONTH
    DELIVERY_BY_COURIER = 0
    price_float = SPACE_FLOAT * COUNT_MONTH
    conn = await create_connection()
    await add_event('', CHAT_ID, TEXT_FIO, TEXT_ADRESS, '', '', BEGIN_DATE, FINAL_DATE, SPACE_FLOAT, WEIGHT_FLOAT,
                    TEXT_COMMENT, price_float, DELIVERY_BY_COURIER)
    await close_connection(conn)
    return CHOOSING


async def not_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global DELIVERY_BY_COURIER, FINAL_DATE, BEGIN_DATE, TEXT_COMMENT, SPACE_FLOAT, WEIGHT_FLOAT, TEXT_ADRESS, \
        TEXT_FIO, CHAT_ID, COUNT_MONTH
    DELIVERY_BY_COURIER = 1
    price_float = SPACE_FLOAT * COUNT_MONTH
    conn = await create_connection()
    await add_event('', CHAT_ID, TEXT_FIO, TEXT_ADRESS, '', '', BEGIN_DATE, FINAL_DATE, SPACE_FLOAT, WEIGHT_FLOAT,
                    TEXT_COMMENT, price_float, DELIVERY_BY_COURIER)
    await close_connection(conn)
    return CHOOSING



async def not_pd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = "Без вашего согласия мы не можем оказать услугу\n <b>" \
           "Попробуйте переосмыслить свою ппозицию</b>"
    await update.message.reply_text(text=text, parse_mode="html")

    return CHOOSING


async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    """Запросите у пользователя описание пользовательской категории."""

    await update.message.reply_text(chf.text_Contacts)
    return TYPING_CHOICE


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    """Сохранить информацию, предоставленную пользователем, и запросить следующую категорию."""

    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )
    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    """Показать собранную информацию и завершить разговор."""

    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )
    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    load_dotenv()
    telegram_token = os.environ["TELEGRAM_TOKEN"]
    application = Application.builder().token(telegram_token).build()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    # Добавить обработчик диалога с состояниями ВЫБОР,    ВВОД ВЫБОРА  и   ВВОД ОТВЕТА

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(ok_pd, pattern="^" + str(OK_PD) + "$"),
                CallbackQueryHandler(not_pd, pattern="^" + str(NOT_PD) + "$")
            ],
            DELIVERY: [
                CallbackQueryHandler(ok_delivery, pattern="^" + str(OK_DE) + "$"),
                CallbackQueryHandler(not_delivery, pattern="^" + str(NOT_DE) + "$"),
            ],
            CHOOSING: [MessageHandler(filters.Regex("^(Help|CreateOrder|MyOrders)$"), regular_choice),
                 MessageHandler(filters.Regex("^Contacts$"), custom_choice), ],
            TYPING_CHOICE: [MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), regular_choice)],
            TYPING_REPLY: [MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), received_information,)],
            FIO: [MessageHandler(filters.TEXT, fio)],
            ADRESS: [MessageHandler(filters.TEXT, adress)],
            CHARACTERISTICS: [MessageHandler(filters.TEXT, characteristics)],
            COMMENT: [MessageHandler(filters.TEXT, comment)],
            END_DATE: [MessageHandler(filters.TEXT, enddate)]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()