from BotManager import aiohttp, Message, FSMContext, CallbackQuery
from aiogram.types import InlineKeyboardButton
from StateClasses import TaskUpdater
import Keyboards as kb
import asyncio

# TODO посмотреть потом не поломается ли на то что импортирование идет не из BotManager а из отдельных классов
async def get_description_for_update(message) -> str:
    # Проверяем, что текст не пустой
    if not message.text.strip():
        raise ValueError("Описание задачи не может быть пустым.")

    # Ограничение на длину имени (например, не больше 50 символов)
    if len(message.text) > 100:
        raise ValueError("Описание задачи слишком длинное (максимум 100 символов).")

    # Проверяем, что имя не содержит запрещённых символов
    if any(char in message.text for char in ['<', '>', '/', '\\', '|']):
        raise ValueError("Описание задачи содержит недопустимые символы.")

    # Если всё хорошо, возвращаем обработанный текст
    return message.text.strip()

async def update_tasks_message_for_update(message: Message, tasks, state):
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
    selection_message = await message.answer("Выберите номер задачи для обновления:",
                                            reply_markup=inline_keyboard)
    # print(tasks_message, "\n\n\n\n", selection_message)
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

async def show_all_tasks(message: Message, state: FSMContext, API_URL, user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params={'user_id': user_id}) as response:
            if response.status == 200:
                tasks = await response.json()  # Получаем список задач в формате JSON
                if tasks:
                    await update_tasks_message_for_update(message, tasks, state)
                else:
                    await message.answer('Нет задач для отображения.', reply_markup=kb.replyMarkup)
            else:
                await message.answer('Ошибка при получении задач!', reply_markup=kb.replyMarkup)
    await state.clear()


async def send_message_and_find_task(message: CallbackQuery, state, task_id, API_URL):

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/{task_id}", params={'user_id': message.from_user.id}) as response:
            if response.status == 200:
                task = await response.json()
                await state.update_data(task_id=task_id, name=task['name'], description=task['description'],
                                        start_date=task['start_date'], finish_date=task['finish_date'],
                                        priority=task['priority'])
                answer = (f"Текущие данные задачи:\n"
                f"Название: {task['name']}\n"
                f"Описание: {task['description']}\n"
                f"Дата начала: {task['start_date']}\n"
                f"Дата окончания: {task['finish_date']}\n"
                f"Приоритет: {task['priority']}\n"
                f'Введите новое название задачи (или нажмите "Пропустить", чтобы сохранить текущее):')

                await message.message.answer(answer, reply_markup=kb.skip)
                await state.set_state(TaskUpdater.name)
            elif response.status == 404:
                await message.answer('Задача не найдена. Проверьте ID и попробуйте снова.')
            else:
                await message.answer('Ошибка при получении задачи!', reply_markup=kb.replyMarkup)

async def set_year_and_send_message_for_update(callback_query, state):
    current_state = await state.get_state()
    if current_state == TaskUpdater.year_finish:
        year = await kb.get_text_inline_button(callback_query)
        if year.lower() != "пропустить":
            print(f"year: {year}")
            await state.update_data(year_finish=year)
            await callback_query.message.answer(
                'Выберите новый месяц завершения задачи:',
                reply_markup=kb.inlineMarkup_months
            )
            await state.set_state(TaskUpdater.month_finish)
        else:
            data = await state.get_data()
            current_finish_time = data.get("finish_date")
            # Сохраняем текущее имя
            await state.update_data(end_time=current_finish_time)
            await callback_query.answer("Изменение времени завершения задачи пропущено.")

            await set_skip_button_for_inline_keyboard_for_update(
                'Введите новый приоритет задачи (или нажмите "Пропустить", чтобы сохранить текущее):',
                state, callback_query=callback_query)

    elif current_state == TaskUpdater.year_start:
        year = await kb.get_text_inline_button(callback_query)
        if year.lower() != "пропустить":
            print(f"year: {year}")
            await state.update_data(year_start=year)
            await callback_query.message.answer(
                'Выберите новый месяц начала задачи:',
                reply_markup=kb.inlineMarkup_months
            )
            await state.set_state(TaskUpdater.month_start)
        else:
            data = await state.get_data()
            current_start_time = data.get("start_date")
            # Сохраняем текущее имя
            await state.update_data(start_time=current_start_time)
            await callback_query.answer("Изменение времени начала пропущено.")

            await set_skip_button_for_inline_keyboard_for_update(
                'Введите новую дату завершения задачи (или нажмите "Пропустить", чтобы сохранить текущее):',
                state, callback_query=callback_query)

async def check_priority_for_update(new_priority):
    if new_priority < 1 or new_priority > 9:
        raise ValueError

async def set_state_for_days_and_send_message(callback_query, send_text_message, state=None):
    current_state = await state.get_state()
    if current_state == TaskUpdater.month_start:
        await callback_query.message.edit_text(
            text=send_text_message,
            reply_markup=kb.inlineMarkup_days
        )
        # Переключаемся на состояние для дня
        await state.set_state(TaskUpdater.day_start)

    elif current_state == TaskUpdater.month_finish:
        await callback_query.message.edit_text(
            text=send_text_message,
            reply_markup=kb.inlineMarkup_days
        )
        # Переключаемся на состояние для дня
        await state.set_state(TaskUpdater.day_finish)

async def set_updated_data_for_update(data, task):
    if data.get('start_time') is None:
        updated_data = {
            'name': data.get('name'),
            'description': data.get('description'),
            'priority': int(data.get('priority')),
            'start_date': task.start_date.strftime("%Y-%m-%dT%H:%M:%S"),
            'finish_date': task.finish_date.strftime("%Y-%m-%dT%H:%M:%S")
        }
    else:
        updated_data = {
            'name': data.get('name'),
            'description': data.get('description'),
            'priority': int(data.get('priority')),
            'start_date': data.get('start_time'),
            'finish_date': data.get('end_time')
        }
    return updated_data

async def data_finish_get_info_for_update(data):
    day = data.get('day_finish')
    month = data.get('month_finish')
    year = data.get('year_finish')
    return day, month, year

async def data_start_get_info_for_update(data):
    day = data.get('day_start')
    month = data.get('month_start')
    year = data.get('year_start')
    return day, month, year

async def set_skip_button_for_inline_keyboard_for_update(send_text_message, state, message=None, callback_query=None):
    current_state = await state.get_state()
    if (current_state == TaskUpdater.year_finish
            or current_state == TaskUpdater.day_finish):
        kb.inlineMarkup_priority.inline_keyboard.append([InlineKeyboardButton(text=f"Пропустить", callback_data=f"Skip")])
        await asyncio.sleep(0.5)
        await callback_query.message.edit_text(
            text=send_text_message,
            reply_markup=kb.inlineMarkup_priority
        )
        kb.inlineMarkup_priority.inline_keyboard.remove([InlineKeyboardButton(text=f"Пропустить", callback_data=f"Skip")])
        await state.set_state(TaskUpdater.priority)

    elif (current_state == TaskUpdater.year_start
          or current_state == TaskUpdater.day_start):
        kb.inlineMarkup_years.inline_keyboard.append(
            [InlineKeyboardButton(text=f"Пропустить", callback_data=f"Skip")])
        await asyncio.sleep(0.5)
        await callback_query.message.edit_text(
            text=send_text_message,
            reply_markup=kb.inlineMarkup_years
        )
        kb.inlineMarkup_years.inline_keyboard.remove(
            [InlineKeyboardButton(text=f"Пропустить", callback_data=f"Skip")])
        await state.set_state(TaskUpdater.year_finish)

    elif current_state == TaskUpdater.description:
        if message is None:
            kb.inlineMarkup_years.inline_keyboard.append([InlineKeyboardButton(text=f"Пропустить", callback_data=f"Skip")])

            print('first')
            await asyncio.sleep(0.5)
            await callback_query.message.edit_text(
                text=send_text_message,
                reply_markup=kb.inlineMarkup_years
            )
            kb.inlineMarkup_years.inline_keyboard.remove([InlineKeyboardButton(text=f"Пропустить", callback_data=f"Skip")])
            await state.set_state(TaskUpdater.year_start)
        else:
            kb.inlineMarkup_years.inline_keyboard.append([InlineKeyboardButton(text=f"Пропустить", callback_data=f"Skip")])
            print("second")
            await asyncio.sleep(0.5)
            await message.answer(
                text=send_text_message,
                reply_markup=kb.inlineMarkup_years
            )
            kb.inlineMarkup_years.inline_keyboard.remove([InlineKeyboardButton(text=f"Пропустить", callback_data=f"Skip")])
            await state.set_state(TaskUpdater.year_start)

async def get_info_for_update(callback_query: CallbackQuery, start_date, finish_date, updated_data):
    return {
        'user_id': str(callback_query.from_user.id),
        'name': updated_data['name'],
        'description': updated_data['description'],
        'start_date': start_date,
        'finish_date': finish_date,
        'priority': updated_data['priority']
    }

async def send_message_by_status_code_for_update(callback_query, response):
    if response.status == 200:
        await callback_query.message.answer("Задача успешно обновлена!", reply_markup=kb.replyMarkup)
    else:
        await callback_query.answer('Ошибка при обновлении задачи!', reply_markup=kb.replyMarkup)