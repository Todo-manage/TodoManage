from BotManager import Message, kb
# TODO здесь есть методы и логика обновления клавиатуры которые нужны для удаления
async def update_tasks_message(message: Message, tasks):
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
    # Отправляем сообщение со списком задач
    await message.answer(f"Вот все ваши задачи:\n{tasks_list}", reply_markup=kb.replyMarkup)