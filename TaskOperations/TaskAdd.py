from Methods.MethodsForAddAction import *
from BotManager import (StateFilter, TaskAdder, Message, FSMContext, CallbackQuery, kb,
                        datetime, API_URL, Router, aiohttp, tasks, F)
from Task import Task

router = Router()
@router.message(StateFilter(TaskAdder.name))
async def get_name(message: Message, state: FSMContext):

    await tasks.update_dict(str(message.from_user.id), {'name': message.text}) #добавил для сохранение задачи

    await state.set_state(TaskAdder.description)
    await message.answer('Введите описание задачи!')
@router.message(StateFilter(TaskAdder.description))
async def get_description(message: Message, state: FSMContext):

    await tasks.update_dict(str(message.from_user.id), {'description': message.text}) #добавил для сохранение задачи

    await state.set_state(TaskAdder.year_start)
    await message.answer('Выберите год когда должна начаться задача',
                         reply_markup=kb.inlineMarkup_years)
@router.callback_query(StateFilter(TaskAdder.year_start))
async def get_year(callback_query: CallbackQuery, state: FSMContext):
    year = await kb.get_text_inline_button(callback_query)  # Дожидаемся выполнения асинхронной функции
    await state.update_data(year_start=year)  # Сохраняем год

    await callback_query.message.edit_text(
        text="Выберите месяц начала задачи",
        reply_markup=kb.inlineMarkup_months
    )
    # Переключаемся на состояние для месяца
    await state.set_state(TaskAdder.month_start)
@router.callback_query(StateFilter(TaskAdder.month_start))
async def get_month(callback_query: CallbackQuery, state: FSMContext):
    month = await kb.get_text_inline_button(callback_query)  # Дожидаемся выполнения
    # print(f"month: {month}")  # Сохраняем месяц в состояние

    await state.update_data(month_start=month)  # Сохраняем месяц

    await callback_query.message.edit_text(
        text="Выберите день начала задачи",
        reply_markup=kb.inlineMarkup_days
    )

    # Переключаемся на состояние для дня
    await state.set_state(TaskAdder.day_start)
@router.callback_query(StateFilter(TaskAdder.day_start))
async def get_day(callback_query: CallbackQuery, state: FSMContext):
    day = await kb.get_text_inline_button(callback_query)  # Дожидаемся выполнения

    await state.update_data(day_start=day)  # Сохраняем день
    # Получаем сохранённые данные
    data = await state.get_data()
    # Извлекаем значения для дня, месяца и года
    day = data.get('day_start')
    month = data.get('month_start')
    year = data.get('year_start')
    # Проверяем, что все значения есть
    if not all([day, month, year]):
        await callback_query.message.answer('Некоторые данные отсутствуют. Попробуйте снова.')
        return

    await tasks.update_dict(str(callback_query.from_user.id),
                      {'start_date': str(datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y"))}) #добавил для сохранение задачи

    # Переходим к следующему состоянию (например, для окончания задачи)
    await state.set_state(TaskAdder.year_finish)
    await callback_query.message.edit_text(
        text="Успешно добавлена дата начала задачи.\nТеперь выберите год окончания задачи.",
        reply_markup=kb.inlineMarkup_years
    )


@router.callback_query(StateFilter(TaskAdder.year_finish))
async def get_year(callback_query: CallbackQuery, state: FSMContext):
    year = await kb.get_text_inline_button(callback_query)  # Дожидаемся выполнения асинхронной функции

    await state.update_data(year_finish=year)  # Сохраняем год

    await callback_query.message.edit_text(
        text="Выберите месяц завершения задачи",
        reply_markup=kb.inlineMarkup_months
    )

    # Переключаемся на состояние для месяца
    await state.set_state(TaskAdder.month_finish)
@router.callback_query(StateFilter(TaskAdder.month_finish))
async def get_month(callback_query: CallbackQuery, state: FSMContext):
    month = await kb.get_text_inline_button(callback_query)  # Дожидаемся выполнения

    await state.update_data(month_finish=month)  # Сохраняем месяц

    await callback_query.message.edit_text(
        text="Выберите день завершения задачи",
        reply_markup=kb.inlineMarkup_days
    )

    # Переключаемся на состояние для дня
    await state.set_state(TaskAdder.day_finish)
@router.callback_query(StateFilter(TaskAdder.day_finish))
async def get_day(callback_query: CallbackQuery, state: FSMContext):
    day = await kb.get_text_inline_button(callback_query)  # Дожидаемся выполнения

    await state.update_data(day_finish=day)  # Сохраняем день

    data = await state.get_data()

    day = data.get('day_finish')
    month = data.get('month_finish')
    year = data.get('year_finish')

    if not all([day, month, year]):
        await callback_query.message.answer('Некоторые данные отсутствуют. Попробуйте снова.')
        return

    await tasks.update_dict(str(callback_query.from_user.id),
                      {'finish_date': str(datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y"))}) #добавил для сохранение задачи

    await state.set_state(TaskAdder.priority)
    await callback_query.message.edit_text(
        text="Успешно добавлена дата завершения задачи.\nТеперь выберите приоритет задачи",
        reply_markup=kb.inlineMarkup_priority
    )
@router.callback_query(TaskAdder.priority)
async def get_priority(callback_query: CallbackQuery, state: FSMContext):

    await tasks.update_dict(str(callback_query.from_user.id), {'priority': await kb.get_text_inline_button(callback_query)})
    

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=await tasks.find_element_by_user_id(str(callback_query.from_user.id))) as response:
            await send_message_by_status_code_for_add(callback_query, response)

    await callback_query.message.delete()
    print(await tasks.find_element_by_user_id(str(callback_query.from_user.id)))
