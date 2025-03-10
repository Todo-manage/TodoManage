from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

replyMarkup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Добавить задачу")],
              [KeyboardButton(text="Удалить задачу")],
              [KeyboardButton(text="Обновить задачу")],
              [KeyboardButton(text="Показать все задачи")]],
resize_keyboard=True,
one_time_keyboard=True,
input_field_placeholder="Выберите одну из опций...")


inlineMarkup_days = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"{j}", callback_data=f"Days{j}") for j in range(i, min(i + 5, 32))]
    for i in range(1, 32, 5)  # Группируем кнопки по строкам (5 кнопок на строку)
])
inlineMarkup_months = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"{j}", callback_data=f"Month{j}") for j in range(i, min(i + 5, 13))]
    for i in range(1, 32, 5)  # Группируем кнопки по строкам (5 кнопок на строку)
])
inlineMarkup_years = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"20{j}", callback_data=f"Years{j}") for j in range(i, min(i + 5, 51))]
    for i in range(24, 51, 5)  # Группируем кнопки по строкам (5 кнопок на строку)
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