import asyncio


from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties


from config import TOKEN

# Импорты роутеров
from app.handlers.user.start.start_in_cafe import start_in_cafe_rt
from app.handlers.user.start.start_in_home import start_in_home_rt

from app.handlers.user.menu.menu import menu_rt
from app.handlers.user.menu.menu_punkt import punkt_rt 

from app.handlers.user.regestration import reg_rt

from app.handlers.user.booking import book_rt 
from app.handlers.user.order import order_rt

from app.database.models import async_main



async def main():
    await async_main()
    
    bot = Bot(token = TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    dp = Dispatcher()
    
    dp.include_routers(start_in_cafe_rt, start_in_home_rt, 
                       menu_rt, reg_rt, 
                       punkt_rt, book_rt, 
                       order_rt)
    
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')