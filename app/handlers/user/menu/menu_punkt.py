from aiogram import Router, F
from aiogram.types import  CallbackQuery, InputMediaPhoto

import app.keyboards.menu_buttons as kb
from app.media.photos_id import (NEW_MENU_PHOTO, BURGERS_MENU_PHOTO, HOT_DISHES_MENU_PHOTO,
                                HOT_ROLLS_MENU_PHOTO, OPEN_ROLLS_MENU_PHOTO, 
                                CLOSSE_ROLLS_MENU_PHOTO,
                                PASTS_MENU_PHOTO, PIZZS_MENU_PHOTO, SALADS_MENU_PHOTO,
                                SNACKS_MENU_PHOTO, SLICES_MENU_PHOTO, SOUS_MENU_PHOTO)

# Роутер
punkt_rt = Router()

# Наши новинки
@punkt_rt.callback_query(F.data == 'new')
async def new(callback: CallbackQuery):
    new_menu_photo = NEW_MENU_PHOTO
    text = f'<b>Наши новинки</b>'
    
    media = InputMediaPhoto(media=new_menu_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.back_in_menu)

# Бургеры
@punkt_rt.callback_query(F.data == 'burgers')
async def burgers(callback: CallbackQuery):
    burgers_menu_photo = BURGERS_MENU_PHOTO
    text = f'<b>Бургеры</b>'
    
    media = InputMediaPhoto(media=burgers_menu_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.back_in_menu)

# Горячие блюда
@punkt_rt.callback_query(F.data == 'hot_dishes')
async def hot_dishes(callback: CallbackQuery):
    hot_dishes_menu_photo = HOT_DISHES_MENU_PHOTO
    text = f'<b>Горячие блюда</b>'
    
    media = InputMediaPhoto(media=hot_dishes_menu_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.back_menu)

# Горячие роллы
@punkt_rt.callback_query(F.data == 'hot_rolls')
async def hot_rolls(callback: CallbackQuery):
    hot_rolls_menu_photo = HOT_ROLLS_MENU_PHOTO
    text = f'<b>Горячие роллы</b>'
    
    media = InputMediaPhoto(media=hot_rolls_menu_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.back_menu)
    
# Открытые роллы
@punkt_rt.callback_query(F.data == 'open_rolls')
async def open_rolls(callback: CallbackQuery):
    open_rolls_menu_photo = OPEN_ROLLS_MENU_PHOTO
    text = f'<b>Открытые роллы</b>'
    
    media = InputMediaPhoto(media=open_rolls_menu_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.back_menu)

# Закрытые роллы   
@punkt_rt.callback_query(F.data == 'closse_rolls')
async def closse_rolls(callback: CallbackQuery):
    closse_rolls_menu_photo = CLOSSE_ROLLS_MENU_PHOTO
    text = f'<b>Закрытые роллы</b>'
    
    media = InputMediaPhoto(media=closse_rolls_menu_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.back_menu)
    
# Пасты
@punkt_rt.callback_query(F.data == 'pasts')
async def pasts(callback: CallbackQuery):
    pasts_menu_photo = PASTS_MENU_PHOTO
    text = f'<b>Пасты</b>'
    
    media = InputMediaPhoto(media=pasts_menu_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.back_menu)

# Пиццы
@punkt_rt.callback_query(F.data == 'pizzs')
async def pizzs(callback: CallbackQuery):
    pizzs_menu_photo = PIZZS_MENU_PHOTO
    text = f'<b>Пиццы</b>'
    
    media = InputMediaPhoto(media=pizzs_menu_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.back_menu)

# Салаты    
@punkt_rt.callback_query(F.data == 'salads')
async def salads(callback: CallbackQuery):
    salads_menu_photo = SALADS_MENU_PHOTO
    text = f'<b>Салаты</b>'
    
    media = InputMediaPhoto(media=salads_menu_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.back_menu)

# Снэки    
@punkt_rt.callback_query(F.data == 'snacks')
async def snacks(callback: CallbackQuery):
    snacks_menu_photo = SNACKS_MENU_PHOTO
    text = f'<b>Снэки</b>'
    
    media = InputMediaPhoto(media=snacks_menu_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.back_menu)

# Нарезки    
@punkt_rt.callback_query(F.data == 'slices')
async def slices(callback: CallbackQuery):
    slices_menu_photo = SLICES_MENU_PHOTO
    text = f'<b>Нарезки</b>'
    
    media = InputMediaPhoto(media=slices_menu_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.back_menu)

# Соусы    
@punkt_rt.callback_query(F.data == 'sous')
async def sous(callback: CallbackQuery):
    sous_menu_photo = SOUS_MENU_PHOTO
    text = f'<b>Соусы</b>'
    
    media = InputMediaPhoto(media=sous_menu_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.back_menu)