from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import PHONE_NUMBER, MAIN_ADMIN
from app.media.photos_id import MAIN_ORDER_PHOTO

import app.keyboards.userkb as kb
from app.database.requests import user_yes_no, get_phone_number, get_adres_user

import asyncio

# Роутер
order_rt = Router()

# Класс состояний для заказа   
class Order(StatesGroup):
    pozition = State() # Позиции в заказе
    phone_number = State() # номер телефона клиента
    adres = State() # адрес доставки
    time = State() # в какое время осуществить доставку
    coment = State() # коментарий к заказу
    ordering = State() # отпарвка заказа администратору
    ordering_admin = State() # заказ у админа

# Обработчик для кнопки       
@order_rt.callback_query(F.data == 'oreder')
async def main_order(callback: CallbackQuery):
    order_photo = MAIN_ORDER_PHOTO
    
    text = f'<b>Привет</b>'
    media = InputMediaPhoto(media=order_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.order_button)

# Если бронь через бота 
@order_rt.callback_query(F.data == 'order_in_bot')
async def order_in_bot(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Order.pozition)
    
    text = f'<b>Введите, чтобы вы хотели заказать, позиция - кол-во штук\n\nПример\n<i>Филадельфия с огурцом - 1 шт, Картошка фри большая - 2 шт.</i></b>'
    first = await callback.message.answer(text=text)
    
    await state.update_data(first = first.message_id)

# Обработчик для позиции
@order_rt.message(Order.pozition)
async def pozition(message: Message, state: FSMContext):
    second = message.message_id
    pozition = message.text
    
    if await user_yes_no(message.from_user.id):
        text = f'<b>Введите ваш номер телефона, для обратной связи или нажмите на кнопку ниже, чтобы поделиться им</b>'
        thread = await message.answer(text = text, reply_markup=kb.phone_number_book)
        await state.set_state(Order.phone_number)
        await state.update_data(second = second,thread = thread.message_id, pozition = pozition)
    else:
        phone_number = await get_phone_number(message.from_user.id)
        text = f'<b>Ваш номер у нас есть,введите адрес доставки или укажите, что вы заберете самовывозом\nПример\n<i>Заволжье. ул.Грунина. д.12б кв.207. 6 подъезд</i></b>'
        thread = await message.answer(text = text, reply_markup=kb.order_button_adres_if_reg)
        
        await state.update_data(phone_number = phone_number, thread = thread.message_id, 
                                pozition = pozition, second = second) 
        await state.set_state(Order.adres)

# Обработчик номера телефона    
@order_rt.message(Order.phone_number)
async def phone_number(message: Message, state: FSMContext):
    
    four = message.message_id
    
    if message.content_type == 'contact':
        # Если есть контакт, записываем номер телефона
        phone_number = message.contact.phone_number
    else:
        # Если контакта нет, записываем текст сообщения
        phone_number = message.text
        
    text = f'<b>Ваш номер успешно записан, введите адрес доставки или укажите, что вы заберете самовывозом\nПример\n<i>Заволжье. ул.Грунина. д.12б кв.207. 6 подъезд</i></b>'
    
    if await user_yes_no(message.from_user.id):  
        five = await message.answer(text = text, reply_markup=kb.order_button_adres_if_not_reg)
    else:
        five = await message.answer(text = text, reply_markup=kb.order_button_adres_if_reg)
    
    await state.update_data(four = four, phone_number = phone_number, five = five.message_id)
    await state.set_state(Order.adres)

# Обработчик адреса
@order_rt.message(F.text == 'Мой адрес', Order.adres)
async def adres_my_adres(message: Message, state: FSMContext):
    
    six = message.message_id
    adres = await get_adres_user(message.from_user.id)
    
    text = f'<b>Отлично, мы записали ваш адрес. Введите на какое время сделать доставку?\n\nПример\n<i>18 апреля к 18:00</i></b>'
    
    seven = await message.answer(text = text, reply_markup=kb.order_time)
    
    await state.update_data(six = six, adres = adres, seven = seven.message_id)
    await state.set_state(Order.time)
    
# Обработчик если самовывоз
@order_rt.message(F.text == 'Самовывоз', Order.adres)
async def adres_sam(message: Message, state: FSMContext):
    
    six = message.message_id
    adres = message.text
    
    text = f'<b>Отлично, мы записали ваш адрес. Введите на какое время сделать доставку/самовывоз?\n\nПример\n<i>18 апреля к 18:00</i></b>'
    
    seven = await message.answer(text = text, reply_markup=kb.order_time)
    
    await state.update_data(six = six, adres = adres, seven = seven.message_id)
    await state.set_state(Order.time)

# Обработчик на какое время привезти заказ
@order_rt.message(Order.time)
async def time_delivery(message: Message, state: FSMContext):
    
    eight = message.message_id
    time_delivery = message.text
    
    text = f'<b>Отлично и наконец оставте коментарий к заказу\n\nПример\n<i>Кол-во приборов... Без помидор</i></b>'
    nine = await message.answer(text = text, reply_markup=ReplyKeyboardRemove())
    
    await state.update_data(eight = eight, time_delivery = time_delivery, nine = nine.message_id)
    await state.set_state(Order.coment)

# Обработчик коментария к заказу    
@order_rt.message(Order.coment)
async def coment(message: Message, state: FSMContext):
    
    ten = message.message_id
    coment_delivery = message.text
    
    data = await state.get_data()
    
    pozition = data['pozition']
    phone_number = data['phone_number']
    adres = data['adres']
    time_delivery = data['time_delivery']
    
    four = data.get('four')
    
    if four is None:
        messeges = ([data["first"], data["second"],
                    data["thread"], data["six"], 
                    data["seven"],data["eight"], 
                    data["nine"], ten])
        
    else:
        messeges = ([data["first"], data["second"], 
                    data["thread"], data["four"], 
                    data["five"], data["six"], 
                    data["seven"],data["eight"], 
                    data["nine"], ten])
        
    text = f'<b>Отлично, ваши данные по заказу сохранены! Отправить заказ администратору?\n\nПозиции - {pozition}\nКонтакт - {phone_number}\nСпособ получения - {adres}\nВремя получения заказа - {time_delivery}\nКоментарий к заказу - {coment_delivery}\n\nВсе верно?</b>'
    
    await message.answer(text = text, reply_markup=kb.order_yes_no_user)
    
    await message.bot.delete_messages(chat_id=message.from_user.id, message_ids=messeges)
    await state.update_data(coment_delivery = coment_delivery)
    await state.set_state(Order.ordering)

# Обработчик отправки заказа
@order_rt.callback_query(F.data == 'post_order', Order.ordering)
async def ordering(callback: CallbackQuery, state: FSMContext):
    
    user_id = callback.from_user.id
    
    text = 'Мы получили ваш заказ, мы оповестим вас когда он будет готов!'
    
    await callback.answer(text=text, show_alert=True)
    await callback.bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
    
    data = await state.get_data()
    
    pozition = data['pozition']
    phone_number = data['phone_number']
    adres = data['adres']
    time_delivery = data['time_delivery']
    coment_delivery = data['coment_delivery']
    
    order_yes_no_admin = InlineKeyboardMarkup(inline_keyboard=[
        
        [InlineKeyboardButton(text='Принять', callback_data=f'accept_{user_id}'), 
        InlineKeyboardButton(text='Отклонить', callback_data=f'overrule_{user_id}')],
        
        [InlineKeyboardButton(text = 'В стоп-листе', callback_data=f'stoplist_{user_id}')]
        
    ])
    
    text = f'<b>Новый заказ\n\nПозиции - {pozition}\nКонтакт - {phone_number}\nСпособ получения - {adres}\nВремя получения заказа - {time_delivery}\nКоментарий к заказу - {coment_delivery}</b>' 
    
    await callback.bot.send_message(chat_id=MAIN_ADMIN, 
                                text = text, 
                                reply_markup=order_yes_no_admin)
    
    await state.clear()

# Обработчик если клиент передумал заказывать
@order_rt.callback_query(F.data == 'no_order', Order.ordering)
async def ordering(callback: CallbackQuery, state: FSMContext):
    
    user_id = callback.from_user.id
    
    text = 'Ждём вас снова...'
    await callback.answer(text=text)
    await callback.bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
    
    await state.clear()

# Обработчик если администратор принял заказ    
@order_rt.callback_query(lambda c: c.data and c.data.startswith('accept_'))
async def accept(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]
    
    text = f'<b>Ваш заказ принят, мы скоро его сделаем!</b>'
    messageuser = await callback.bot.send_message(chat_id=user_id, text = text)
    
    await callback.bot.delete_message(chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id)
    await asyncio.sleep(600)
    
    await callback.bot.delete_message(chat_id=user_id, message_id=messageuser.message_id)

# Обработчик если администратор отклонил заказ      
@order_rt.callback_query(lambda c: c.data and c.data.startswith('overrule_'))
async def overrule(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]
    
    text = f'<b>Ваш заказ отклонен, видимо произошли какие-либо проблемы...</b>'
    messageuser = await callback.bot.send_message(chat_id=user_id, text = text)
    
    await callback.bot.delete_message(chat_id=callback.from_user.id,
                                      message_id=callback.message.message_id)
    await asyncio.sleep(600)
    
    await callback.bot.delete_message(chat_id=user_id, message_id=messageuser.message_id)

# Обработчик если заказ в стоп-листе      
@order_rt.callback_query(lambda c: c.data and c.data.startswith('stoplist_'))
async def stoplist(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]
    
    text = f'<b>К сожалению, какие-то позиции попали в стоп лист, попробуйте нам позвонить, мы решим этот вопрос</b>'
    messageuser = await callback.bot.send_message(chat_id=user_id, text = text)
    
    await callback.bot.delete_message(chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id)
    await asyncio.sleep(600)
    
    await callback.bot.delete_message(chat_id=user_id, message_id=messageuser.message_id)

# Обработчик если заказ по телефону будет
@order_rt.callback_query(F.data == 'call_phone_order')
async def call_phone_order(callback: CallbackQuery):
    
    text = f'<b>Сделайте заказ позвонив по данному номеру!\n{PHONE_NUMBER}</b>'
    
    await callback.message.edit_caption(caption=text, reply_markup=kb.back_to_ordering)
    