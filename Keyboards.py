from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import calendar


replyMarkup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Добавить задачу")],
              [KeyboardButton(text="Удалить задачу")],
              [KeyboardButton(text="Обновить задачу")],
              [KeyboardButton(text="Показать все задачи")],
              [KeyboardButton(text="Создать команду")]],
resize_keyboard=True,
one_time_keyboard=True,
input_field_placeholder="Выберите одну из опций...")



inlineMarkup_days = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"{j}", callback_data=f"Days{j}") for j in range(i, min(i + 5, 32))]
    for i in range(1, 32, 5)  # Группируем кнопки по строкам (5 кнопок на строку)
])

# def inlineMarkup_days(year: int, month: int):
#     max_days = max(calendar.monthcalendar(year, month)[-1])
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text=f"{j}", callback_data=f"Days{j}") for j in range(i, min(i + 5, max_days+1))]
#     for i in range(1, max_days+1, 5)])  # Группируем кнопки по строкам (5 кнопок на строку)

#     return keyboard



inlineMarkup_months = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"{j}", callback_data=f"Month{j}") for j in range(i, min(i + 5, 13))]
    for i in range(1, 13, 5)  # Группируем кнопки по строкам (5 кнопок на строку)
])


inlineMarkup_years = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"20{j}", callback_data=f"Years{j}") for j in range(i, min(i + 5, datetime.now().year-1985))]
    for i in range(datetime.now().year-2000, datetime.now().year-1985, 5)  # Группируем кнопки по строкам (5 кнопок на строку)
])


inlineMarkup_priority = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"{j}", callback_data=f"Priority{j}") for j in range(i, min(i + 5, 10))]
    for i in range(1, 10, 5)  # Группируем кнопки по строкам (5 кнопок на строку)
])


skip = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"Пропустить", callback_data=f"Skip")]
])


tasks = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f"ID", callback_data=f"ID1")]])


async def get_text_inline_button(callback_query):
    button_text = None
    for row in callback_query.message.reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == callback_query.data:
                button_text = button.text
                break
        if button_text:
            break
    return button_text
