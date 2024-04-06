from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart



from app.database.requests import user_yes_no
from app.media.photos_id import MAIN_PHOTO_NOT_PLACE

import app.keyboards.main_buttons as kb


# Роутер
start_in_home_rt = Router()

photo_id = MAIN_PHOTO_NOT_PLACE

# функция для старта не в заведении
@start_in_home_rt.message(CommandStart(deep_link= False))
async def start_in_home(message: Message):
    
    
    # main_photo = FSInputFile('app\media\main.png') # Фото когда не в заведении
    
    text = f'<b>Доброго времени суток <i>{message.from_user.first_name}</i>!\nЧто вас интересует?\n\n<i>Меню</i> - наше меню, вы сможете ознакомиться с нашим меню\n<i>Забронировать столик</i> - Вы сможете забронировать столик\n<i>Сделать заказ</i> - Вы сможете, заказать доставку куда вам удобно</b>'
    if await user_yes_no(message.from_user.id):
        await message.answer_photo(photo=photo_id, caption=text, reply_markup=kb.start_in_home_not_reg) # Если не зареган пользователь, ему отправляем с кнопкой регистрации

    else:
        await message.answer_photo(photo=photo_id, caption=text, reply_markup=kb.start_in_home)
        
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id) # Удаление /start от пользователя
    
@start_in_home_rt.callback_query(F.data == 'start_in_home_button')
async def start_in_home_button(callback: CallbackQuery):
    
    # main_photo = FSInputFile('app\media\main.png') # Фото когда не в заведении
    
    text = f'<b>Доброго времени суток <i>{callback.from_user.first_name}</i>!\nЧто вас интересует?\n\n<i>Меню</i> - наше меню, вы сможете ознакомиться с нашим меню\n<i>Забронировать столик</i> - Вы сможете забронировать столик\n<i>Сделать заказ</i> - Вы сможете, заказать доставку куда вам удобно</b>'
    if await user_yes_no(callback.from_user.id):
        await callback.message.answer_photo(photo=photo_id, caption=text, reply_markup=kb.start_in_home_not_reg) # Если не зареган пользователь, ему отправляем с кнопкой регистрации
    else:
        await callback.message.answer_photo(photo=photo_id, caption=text, reply_markup=kb.start_in_home)
        
    await callback.message.delete()
    

@start_in_home_rt.callback_query(F.data == 'back_in_home')
async def back_main_menu_in_home(callback: CallbackQuery):
    
    # main_photo = FSInputFile('app\media\main.png') # Фото когда не в заведении
    
    text = f'<b>Доброго времени суток <i>{callback.from_user.first_name}</i>!\nЧто вас интересует?\n\n<i>Меню</i> - наше меню, вы сможете ознакомиться с нашим меню\n<i>Забронировать столик</i> - Вы сможете забронировать столик\n<i>Сделать заказ</i> - Вы сможете, заказать доставку куда вам удобно</b>'
    media = InputMediaPhoto(media=photo_id, caption=text)
    
    if await user_yes_no(callback.from_user.id):
        await callback.message.edit_media(media, reply_markup=kb.start_in_home_not_reg)
    else:
        await callback.message.edit_media(media, reply_markup=kb.start_in_home)

    