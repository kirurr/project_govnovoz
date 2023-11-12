import telebot
import converter
import yandex_loader
from os import remove, path, getenv
from shutil import make_archive, rmtree
from telebot import types
from time import time
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(message.chat.id, "Здарова, присылай текст сюда")


@bot.message_handler(func=lambda message: True, content_types=["text"])
def default_command(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Да", callback_data="True")
    btn2 = types.InlineKeyboardButton(text="Нет", callback_data="False")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Обработать этот текст?", reply_markup=markup)
    global message_text
    message_text = message.text


@bot.callback_query_handler(func=lambda callback: callback)
def callback_handler(callback):
    bot.answer_callback_query(callback.id)

    bot.edit_message_reply_markup(
        callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup="",
    )

    if callback.data == "True":
        bot.edit_message_text(
            "Ок, начинаю работу...",
            callback.message.chat.id,
            message_id=callback.message.message_id,
        )
        converter.converter(message_text)
        bot.send_message(
            callback.message.chat.id, "Готово! Загружаю файл и создаю ссылку..."
        )

        archive_name = f"{time()}-images"

        make_archive(archive_name, "zip", "images")
        load = yandex_loader.Loader("images", f"{archive_name}.zip")

        load.load_to_yandex()
        link = load.get_download_link()

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Тык", url=link)
        markup.add(btn1)

        bot.send_message(
            callback.message.chat.id,
            "Вот твоя ссылка для скачивания:",
            reply_markup=markup,
        )

        if path.exists(f"{archive_name}.zip"):
            remove(f"{archive_name}.zip")
        if path.exists("images"):
            rmtree("images")

    else:
        bot.send_message(callback.message.chat.id, "Присылай другой текст")


bot.infinity_polling()
