from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, StateFilter

class TaskAdder(StatesGroup):
    name = State()
    description = State()
    start_time = State()
    end_time = State()
    priority = State()

    day_start = State()
    month_start = State()
    year_start = State()
    day_finish = State()
    month_finish = State()
    year_finish = State()

class ShowAlltasks(StatesGroup):
    tasks = State()

class TaskDeleter(StatesGroup):
    task = State()
    tasks_message_id = ""
    selection_message_id = ""

class TaskUpdater(StatesGroup):
    day_finish = State()
    month_finish = State()
    year_finish = State()

    day_start = State()
    month_start = State()
    year_start = State()

    task_id = State()
    name = State()
    description = State()
    start_time = State()
    end_time = State()
    priority = State()
