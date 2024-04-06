from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import  CallbackQuery, InputMediaPhoto

import app.keyboards.menu_buttons as kb_menu
from app.media.photos_id import MAIN_MENU_PHOTO


# Роутер
menu_rt = Router()

# Меню в заведении    
@menu_rt.callback_query(F.data == 'menu_cafe')
async def menu_in_cafe(callback: CallbackQuery):
    
    main_menu_photo = MAIN_MENU_PHOTO # Фото главного фото меню
    text = f'<b>Вам предоставлено меню, пожалуйста ознакомьтесь с ним</b>' 
    media = InputMediaPhoto(media=main_menu_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb_menu.main_menu_cafe)

# Меню дома 
@menu_rt.callback_query(F.data == 'menu_home')
async def menu_in_home(callback: CallbackQuery):

    main_menu_photo = MAIN_MENU_PHOTO # Фото главного фото меню
    text = f'<b>Вам предоставлено меню, пожалуйста ознакомьтесь с ним\nЧто бы вы хотели заказать?</b>' 
    media = InputMediaPhoto(media=main_menu_photo, caption=text)
    await callback.message.edit_media(media = media, reply_markup=kb_menu.main_menu_home)

# Обработчик для кнопки назад
@menu_rt.callback_query(F.data == 'back_menu')
async def menu_back(callback: CallbackQuery, state: FSMContext):
    # Получаем данные состояния
    data = await state.get_data()
    
    # Проверяем, находится ли пользователь в состоянии или нет
    number = data.get("number_table")  # Используем метод get для безопасного доступа к значению
    if number is None:
        # Если пользователь не в состоянии, отправляем ему меню в домашнем кабинете
        await menu_in_home(callback)
    else:
        # Если пользователь в состоянии, отправляем ему меню в кафе
        await menu_in_cafe(callback)