from aiogram import Bot, Dispatcher
import asyncio
from BotManager import router
from TaskOperations.TaskAdd import router as router_add
from TaskOperations.TaskDelete import router as router_delete
from TaskOperations.TaskUpdate import router as router_update
import subprocess
from datetime import datetime
async def main():
    # res = subprocess.run(['python', 'API/api.py'], capture_output=True, text=True)
    # file = open(f'API\LOGS\Out-{datetime.today().date()}.txt', 'a')
    # file.write(f'Out log from api: {res.stdout}\n')
    # if res.stderr is not None:
    #     fileErr = open(f'API\LOGS\Error-{datetime.today().date()}.txt', 'a')
    #     fileErr.write(f'Err log from api: {res.stderr}\n')

    file = open('Password.txt', 'r')
    bot = Bot(token=str(file.read()))
    file.close()

    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(router_add)
    dp.include_router(router_delete)
    dp.include_router(router_update)

    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main()) 