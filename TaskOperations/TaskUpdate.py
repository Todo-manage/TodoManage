from Methods.MethodsForUpdateAction import *
from Keyboards import get_text_inline_button
from BotManager import (Router, Message, FSMContext, aiohttp, API_URL, kb, CallbackQuery, StateFilter, datetime)
from Task import Task

# TODO посмотреть потом не поломается ли на то что импортирование идет не из BotManager а из отдельных классов
router = Router()

task = Task()
@router.callback_query(TaskUpdater.task_id)
async def get_task_id_for_update(callback_query: CallbackQuery, state: FSMContext):
    try:
        task = None
        task_id = await get_text_inline_button(callback_query)
        task_id = int(task_id) # Преобразуем текст в целое число
    except ValueError:
        await callback_query.answer('Пожалуйста, введите корректный ID задачи.')
        return
    await send_message_and_find_task(callback_query, state, task_id, API_URL)

@router.message(TaskUpdater.name)
async def get_new_name(message: Message, state: FSMContext):
    """Обработка ввода нового имени задачи"""
    try:
        if message.text.lower() != "пропустить":
            new_name = await get_name_for_update(message)
            await state.update_data(name=new_name)
        await message.answer(
            'Введите новое описание задачи (или нажмите "Пропустить", чтобы сохранить текущее):',
            reply_markup=kb.skip
        )
        await state.set_state(TaskUpdater.description)
    except ValueError as e:
        await message.answer(f"Ошибка: {str(e)}. Попробуйте ещё раз.")

@router.callback_query(TaskUpdater.name, lambda callback: callback.data == "Skip")
async def skip_name_update(callback_query: CallbackQuery, state: FSMContext):
    """Обработка нажатия кнопки "Пропустить" для имени"""
    # Получаем текущее имя из состояния
    data = await state.get_data()
    current_name = data.get("name")
    # Сохраняем текущее имя
    await state.update_data(name=current_name)
    await callback_query.answer("Изменение имени пропущено.")
    await callback_query.message.edit_text(
        'Введите новое описание задачи (или нажмите "Пропустить", чтобы сохранить текущее):',
        reply_markup=kb.skip
    )
    await state.set_state(TaskUpdater.description)

async def get_name_for_update(message) -> str:
    # Проверяем, что текст не пустой
    if not message.text.strip():
        raise ValueError("Имя задачи не может быть пустым.")

    # Ограничение на длину имени (например, не больше 50 символов)
    if len(message.text) > 50:
        raise ValueError("Имя задачи слишком длинное (максимум 50 символов).")

    # Проверяем, что имя не содержит запрещённых символов
    if any(char in message.text for char in ['<', '>', '/', '\\', '|']):
        raise ValueError("Имя задачи содержит недопустимые символы.")

    # Если всё хорошо, возвращаем обработанный текст
    return message.text.strip()

@router.message(TaskUpdater.description)
async def get_new_description(message: Message, state: FSMContext):
    """Обработка ввода нового имени задачи"""
    try:
        if message.text.lower() != "пропустить":
            new_description = await get_description_for_update(message)
            await state.update_data(description=new_description)
            await set_skip_button_for_inline_keyboard_for_update(
                'Введите новую дату начала задачи (или нажмите "Пропустить", чтобы сохранить текущее):', state,
                message=message)
    except ValueError as e:
        await message.answer(f"Ошибка: {str(e)}. Попробуйте ещё раз.")

@router.callback_query(TaskUpdater.description, lambda callback: callback.data == "Skip")
async def skip_description_update(callback_query: CallbackQuery, state: FSMContext):
    """Обработка нажатия кнопки "Пропустить" для имени"""
    # Получаем текущее имя из состояния
    data = await state.get_data()
    current_description = data.get("description")
    # Сохраняем текущее имя
    await state.update_data(description=current_description)
    await callback_query.answer("Изменение описания пропущено.")
    await set_skip_button_for_inline_keyboard_for_update(
        'Введите новую дату начала задачи (или нажмите "Пропустить", чтобы сохранить текущее):', state,
        callback_query=callback_query)

@router.callback_query(StateFilter(TaskUpdater.year_start))
async def get_year(callback_query: CallbackQuery, state: FSMContext):
    try:
        await set_year_and_send_message_for_update(callback_query, state)
    except ValueError as e:
        await callback_query.message.answer(f"Ошибка: {str(e)}. Попробуйте ещё раз.")

@router.callback_query(StateFilter(TaskUpdater.month_start))
async def get_month(callback_query: CallbackQuery, state: FSMContext):
    month = await get_text_inline_button(callback_query)  # Дожидаемся выполнения
    print(f"month: {month}")  # Сохраняем месяц в состояние

    await state.update_data(month_start=month)  # Сохраняем месяц
    await set_state_for_days_and_send_message(callback_query, "Выберите новый день начала задачи",
                                              state=state)

@router.callback_query(StateFilter(TaskUpdater.day_start))
async def get_day(callback_query: CallbackQuery, state: FSMContext):
    day = await get_text_inline_button(callback_query)  # Дожидаемся выполнения
    print(f"day: {day}")  # Сохраняем день в состояние

    await state.update_data(day_start=day)  # Сохраняем день

    # Получаем сохранённые данные
    data = await state.get_data()

    # Извлекаем значения для дня, месяца и года
    day, month, year = await data_start_get_info_for_update(data)

    # Проверяем, что все значения есть
    if not all([day, month, year]):
        await callback_query.message.answer('Некоторые данные отсутствуют. Попробуйте снова.')
        return

    # Формируем строку даты
    task.start_date = datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y")
    print(task.start_date)

    # Переходим к следующему состоянию (например, для окончания задачи)
    await set_skip_button_for_inline_keyboard_for_update(
        callback_query=callback_query,
        state=state,
        send_text_message=f"Успешно добавлена дата начала задачи.\nТеперь выберите год окончания задачи.")

@router.callback_query(StateFilter(TaskUpdater.year_finish))
async def get_year(callback_query: CallbackQuery, state: FSMContext):
    try:
        await set_year_and_send_message_for_update(callback_query, state)
    except ValueError as e:
        await callback_query.message.answer(f"Ошибка: {str(e)}. Попробуйте ещё раз.")

@router.callback_query(StateFilter(TaskUpdater.month_finish))
async def get_month(callback_query: CallbackQuery, state: FSMContext):
    month = await get_text_inline_button(callback_query)  # Дожидаемся выполнения
    print(f"month: {month}")  # Сохраняем месяц в состояние
    await state.update_data(month_finish=month)  # Сохраняем месяц
    await set_state_for_days_and_send_message(callback_query, "Выберите новый день завершения задачи",
                                              state)

@router.callback_query(StateFilter(TaskUpdater.day_finish))
async def get_day(callback_query: CallbackQuery, state: FSMContext):
    day = await get_text_inline_button(callback_query)  # Дожидаемся выполнения
    print(f"day: {day}")

    await state.update_data(day_finish=day)  # Сохраняем день

    # Получаем сохранённые данные
    data = await state.get_data()

    # Извлекаем значения для дня, месяца и года
    day, month, year = await data_finish_get_info_for_update(data)

    # Проверяем, что все значения есть
    if not all([day, month, year]):
        await callback_query.answer('Некоторые данные отсутствуют. Попробуйте снова.')
        return

    # Формируем строку даты
    task.finish_date = datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y")
    print(task.finish_date)

    # Переходим к следующему состоянию (например, для окончания задачи)
    await set_skip_button_for_inline_keyboard_for_update(
        "Успешно добавлена дата начала задачи.\nТеперь выберите приоритет задачи.",
        state, callback_query=callback_query)
@router.callback_query(TaskUpdater.priority)
async def get_new_priority(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    current_priority = data.get('priority')  # Получаем текущее значение

    new_priority = await get_text_inline_button(callback_query)
    if new_priority.lower() != 'пропустить':
        try:
            new_priority = int(new_priority)
            await check_priority_for_update(new_priority)
            await state.update_data(priority=new_priority)
        except ValueError:
            await set_skip_button_for_inline_keyboard_for_update(callback_query,
                                                                 'Пожалуйста, введите корректный приоритет от 1 до 9.')
            return
    else:
        await state.update_data(priority=current_priority)  # Сохраняем предыдущее значение

    data = await state.get_data()

    updated_data = await set_updated_data_for_update(data, task)

    async with aiohttp.ClientSession() as session:
        print(await get_info_for_update(callback_query, updated_data['start_date'], updated_data['finish_date'], updated_data))
        async with session.put(f"{API_URL}/{task_id}", json=await get_info_for_update(callback_query,
                                                                                      updated_data['start_date'],
                                                                                      updated_data['finish_date'],
                                                                                      updated_data)) as response:
            print(response.status, await response.text())
            await send_message_by_status_code_for_update(callback_query, response)
    await state.clear()  # Сброс состояния после завершения операции