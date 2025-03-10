from BotManager import (Message, kb, FSMContext, aiohttp)
from aiogram.types import InlineKeyboardButton

async def show_all_tasks(message: Message, state: FSMContext, API_URL):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params={'user_id': message.from_user.id}) as response:
            if response.status == 200:
                tasks = await response.json()  # Получаем список задач в формате JSON
                if tasks:
                    await update_tasks_message_for_delete(message, tasks, state)
                else:
                    await message.answer('Нет задач для отображения.', reply_markup=kb.replyMarkup)
            else:
                await message.answer('Ошибка при получении задач!', reply_markup=kb.replyMarkup)
    await state.clear()


async def update_tasks_message_for_delete(message: Message, tasks, state):
    tasks_list = "\n".join([
        (
            f"ID: {item['id']}\n"
            f"Название: {item['name']}\n"
            f"Описание: {item['description']}\n"
            f"Дата начала: {item['start_date']}\n"
            f"Дата окончания: {item['finish_date']}\n"
            f"Приоритет: {item['priority']}\n"
            "-------------------------------------"
        )
        for item in tasks
    ])
    # Генерация Inline-клавиатуры
    inline_keyboard = generate_tasks_keyboard(tasks, row_size=5)
    # Отправляем сообщение со списком задач
    tasks_message = await message.answer(f"Вот все ваши задачи:\n{tasks_list}", reply_markup=kb.replyMarkup)
    selection_message = await message.answer("Выберите номер задачу для удаления:",
                                            reply_markup=inline_keyboard)
    print(tasks_message, "\n", selection_message)
    # Сохраняем ID сообщения со списком задач
    await state.update_data(tasks_message_id=tasks_message.message_id,
                            selection_message_id=selection_message.message_id)
def generate_tasks_keyboard(tasks, row_size=5):
    kb.tasks.inline_keyboard.clear()
    ids = [item['id'] for item in tasks]
    # Разбиваем список кнопок на строки по `row_size` элементов
    for i in range(0, len(ids), row_size):
        row = [
            InlineKeyboardButton(text=f'{ids[j]}', callback_data=f'ID{ids[j]}')
            for j in range(i, min(i + row_size, len(ids)))
        ]
        kb.tasks.inline_keyboard.append(row)
    return kb.tasks