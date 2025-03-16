from aiogram import Router, F
from aiogram.client.session import aiohttp
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from StateClasses import *
from aiogram.types import Message, CallbackQuery
import Keyboards as kb
from Task import *
from Methods.MethodsForShowAllTasksAction import update_tasks_message as update_tasks_message_for_show
from Methods.MethodsForDeleteAction import show_all_tasks as show_all_tasks_for_delete
from Methods.MethodsForUpdateAction import show_all_tasks as show_all_tasks_for_update
from SaveTask import SaveTask

router = Router()
API_URL = 'http://localhost:8000/tasks'
tasks = SaveTask()
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!",
                         reply_markup=kb.replyMarkup)

@router.message(F.text == 'Добавить задачу')# TODO надо подумать как попадать в метод после этого заменив set_state().
async def task_add(message: Message, state: FSMContext):

    await state.set_state(TaskAdder.name)
    await message.answer('Введите название задачи!')
    await tasks.update_dict(str(message.from_user.id), {'user_id': str(message.from_user.id)})


@router.message(F.text == 'Показать все задачи')
async def show_all_tasks(message: Message, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params={'user_id': message.from_user.id}) as response:
            if response.status == 200:
                tasks = await response.json()  # Получаем список задач в формате JSON
                if tasks:
                    await update_tasks_message_for_show(message, tasks)
                else:
                    await message.answer('Нет задач для отображения.', reply_markup=kb.replyMarkup)
            else:
                await message.answer('Ошибка при получении задач!', reply_markup=kb.replyMarkup)
    await state.clear()

@router.message(F.text == 'Удалить задачу')
async def delete_task(message: Message, state: FSMContext):
    await show_all_tasks_for_delete(message, state, API_URL)
    await state.set_state(TaskDeleter.task)

@router.message(F.text == 'Обновить задачу')
async def update_task(message: Message, state: FSMContext):
    await show_all_tasks_for_update(message, state, API_URL, message.from_user.id)
    await state.set_state(TaskUpdater.task_id)