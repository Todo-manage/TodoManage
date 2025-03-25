import os
from aiogram import Bot, Dispatcher
import asyncio
import aiohttp
from BotManager import router
from TaskOperations.TaskAdd import router as router_add
from TaskOperations.TaskDelete import router as router_delete
from TaskOperations.TaskUpdate import router as router_update
from datetime import datetime
def start_api():
    os.system('cd API && start /B python api.py')

async def wait_for_api():
    for _ in range(10):  # 10 попыток с интервалом 1 секунда
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:8000/tasks?user_id=1') as response:
                    if response.status in [200, 404]:
                        print("апишка запущена и доступна")
                        return
        except:
            print("Ожидание запуска апи")
        await asyncio.sleep(1)
    raise RuntimeError("апи не запустилась вовремя")

async def main():
    api_process = start_api()  # запускаем
    await wait_for_api()  #ждем

    file = open('Password.txt', 'r')
    bot = Bot(token=str(file.read().strip()))
    file.close()

    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(router_add)
    dp.include_router(router_delete)
    dp.include_router(router_update)

    try:
        await dp.start_polling(bot)
    finally:
        api_process.terminate()  # остановить апи при завершении работы бота

if __name__ == "__main__":
    asyncio.run(main())