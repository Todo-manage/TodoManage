from aiogram import Bot, Dispatcher
import asyncio
from BotManager import router
from TaskOperations.TaskAdd import router as router_add
from TaskOperations.TaskDelete import router as router_delete
from TaskOperations.TaskUpdate import router as router_update

async def main():
    bot = Bot(token='7559173892:AAGF9i5R8FiGhdM6M4UpjycTWDa8ku2Fyc8')
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(router_add)
    dp.include_router(router_delete)
    dp.include_router(router_update)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 
