from BotManager import Router, TaskDeleter, CallbackQuery, FSMContext, aiohttp, API_URL


router = Router()
@router.callback_query(TaskDeleter.task)
async def get_task_id_for_deletion(callback_query: CallbackQuery, state: FSMContext):
    task_id = callback_query.data.replace("ID", "")  # Получаем ID задачи из callback_data
    try:
        task_id = int(task_id)  # Преобразуем текст в целое число
    except ValueError:
        await callback_query.answer('Пожалуйста, выберите корректный ID задачи.')
        return

    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{API_URL}/{task_id}", params={'user_id': callback_query.from_user.id}) as response:
            if response.status == 204:
                await callback_query.answer('Задача успешно удалена!')
                await state.clear()
            elif response.status == 404:
                await callback_query.answer('Задача не найдена. Проверьте ID и попробуйте снова.')
            else:
                await callback_query.answer('Ошибка при удалении задачи!')
                await state.clear()