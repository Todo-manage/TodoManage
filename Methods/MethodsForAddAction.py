import Keyboards as kb
async def get_info_for_add(callback_query, task):
    return {
        'user_id': str(callback_query.from_user.id),
        'name': task.name,
        'description': task.description,
        'priority': int(task.priority),
        'start_date': task.start_date.strftime("%Y-%m-%dT%H:%M:%S"),
        'finish_date': task.finish_date.strftime("%Y-%m-%dT%H:%M:%S")
    }

async def send_message_by_status_code_for_add(callback_query, response):
    if response.status == 201:
        await callback_query.message.answer("Задача добавлена!", reply_markup=kb.replyMarkup)
    else:
        error_details = await response.text()
        await callback_query.message.answer(
            f"Ошибка при добавлении задачи: {response.status}\n{error_details}",
            reply_markup=kb.replyMarkup
        )