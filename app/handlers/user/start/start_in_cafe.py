from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart, CommandObject

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import ADMINS, PLACE_NAME
from app.media.photos_id import MAiN_PHOTO_IN_PLACE

import app.keyboards.main_buttons as kb

# Роутер
start_in_cafe_rt = Router()

class Number_table(StatesGroup):
    number_table = State()

place_name = PLACE_NAME # Название заведения
phot_id = MAiN_PHOTO_IN_PLACE 

# функция для старта в заведении
@start_in_cafe_rt.message(CommandStart(deep_link= True))
async def start_in_caffe(message: Message, command: CommandObject, state: FSMContext):
    # main_photo = FSInputFile('app\media\main.png') # Фото когда в заведении
    
    number_table = command.args # номер столика
    text = f'<b>Доброго времени суток <i>{message.from_user.first_name}</i>!\nРады видеть вас в {place_name}\nЯ запомнил, что вы за столиком номер {number_table}\n\nОзнакомтесь с нашим меню, после чего нажми кнопку <i>Позвать официанта</i> и у вас примут заказ\nПриятного аппетита)\n\nПосле того, как вы закончите прибывание в заведении нажмите кнопку<i>Заврешить посещение</i></b>'
    
    await message.answer_photo(photo=phot_id, caption=text, reply_markup=kb.start_in_place)

    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id) # Удаление /start от пользователя
    
    await state.set_state(Number_table.number_table)
    await state.update_data(number_table = number_table)


@start_in_cafe_rt.callback_query(F.data == 'back_in_cafe')
async def back_main_menu_in_cafe(callback: CallbackQuery):
    #main_photo = FSInputFile('app\media\main.png') # Фото когда в заведении
    

    text = f'<b>Доброго времени суток <i>{callback.from_user.first_name}</i>!\nРады видеть вас в {place_name}\n\nОзнакомтесь с нашим меню, после чего нажми кнопку <i>Позвать официанта</i> и у вас примут заказ\nПриятного аппетита)</b>'
    media = InputMediaPhoto(media=phot_id, caption=text)
    
    await callback.message.edit_media(media, reply_markup=kb.start_in_place)
    
@start_in_cafe_rt.callback_query(F.data == 'call_oficient', Number_table.number_table)
async def call_oficient(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    for admin in ADMINS:
        await callback.bot.send_message(chat_id=admin, text = f'Столик номер - {data["number_table"]}\nПозвал официанта')
        
    await callback.answer(text='Официант, уже бежит к вам!', show_alert=True)

@start_in_cafe_rt.callback_query(F.data == 'account', Number_table.number_table)
async def account(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    for admin in ADMINS:
        await callback.bot.send_message(chat_id=admin, text = f'Столик номер - {data["number_table"]}\nПросит принести счёт')
        
    await callback.answer(text='Официант, скоро принесет вам счёт', show_alert=True)
    
@start_in_cafe_rt.callback_query(F.data == 'exit_in_cafe')
async def exit_in_cafe(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text='Ждем вас снова!', show_alert=True)
    
    text = f'<b>Если вы захотите заказать еду из дома или забронировать, вы можете нажать кнопку <i>Начать</i></b>'
    
    await callback.message.edit_caption(caption=text, reply_markup=kb.start_in_home_button)
    
    await state.clear()
    
