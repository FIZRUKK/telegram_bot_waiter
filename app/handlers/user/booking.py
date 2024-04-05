from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import ADMINS, PHONE_NUMBER
from app.media.photos_id import MAIN_BOOKING_PHOTO

import app.keyboards.userkb as kb
from app.database.requests import user_yes_no, get_phone_number

import asyncio
import os

# Роутер
book_rt = Router()

class Book(StatesGroup):
    phone_number = State()
    count_people = State()
    time = State()
    coment = State()
    book = State()
    
@book_rt.callback_query(F.data == 'booking')
async def main_booking(callback: CallbackQuery):
    
    booking_photo = MAIN_BOOKING_PHOTO
    
    text = f'<b>Привет</b>'
    
    media = InputMediaPhoto(media=booking_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb.book_button)
    
@book_rt.callback_query(F.data == 'call_phone')
async def book_call_phone(callback: CallbackQuery):

    text = f'Свяжитесь с нами и заброниируйте столик по этому номеру  {PHONE_NUMBER}'
    
    await callback.message.edit_caption(caption=text, reply_markup=kb.back_book)
    
@book_rt.callback_query(F.data == 'booking_new')
async def booking_new(callback: CallbackQuery, state: FSMContext):
    
    if await user_yes_no(callback.from_user.id):
        
        text = 'Введите ваш номер телефона, для обратной связи или нажмите на кнопку ниже, чтобы поделиться им'
        
        first = await callback.message.answer(text = text, reply_markup=kb.phone_number_book)
        await state.set_state(Book.phone_number)
        await state.update_data(first = first.message_id)
    else:
        phone_number = await get_phone_number(callback.from_user.id)
        
        text = 'Ваш номер у нас есть, выберите на сколько персон столик?'
        
        first = await callback.message.answer(text=text, reply_markup=kb.count_people)
        await state.update_data(phone_number = phone_number, first = first.message_id) 
        await state.set_state(Book.count_people)

@book_rt.message(Book.phone_number)
async def phone_number(message: Message, state: FSMContext):
    
    second = message.message_id
    if message.content_type == 'contact':
        # Если есть контакт, записываем номер телефона
        phone_number = message.contact.phone_number
    else:
        # Если контакта нет, записываем текст сообщения
        phone_number = message.text
    
    text = 'Ваш номер успешно записан, выберите на сколько персон столик?'
    
    third = await message.answer(text = text, reply_markup=kb.count_people)
    await state.update_data(phone_number = phone_number, second = second, third = third.message_id)
    await state.set_state(Book.count_people)
        
@book_rt.message(Book.count_people)
async def count_people(message: Message, state: FSMContext):
    count_people = message.text
    four = message.message_id

    text = 'Отлично, введите на какое время вам забронировать?\nПример: 18 апреля 18:00'
    
    five = await message.answer(text = text, reply_markup=ReplyKeyboardRemove())
    
    await state.update_data(count_people = count_people, four = four, five = five.message_id)
    await state.set_state(Book.time)

@book_rt.message(Book.time)
async def time_book(message: Message, state: FSMContext):
    
    time_book = message.text
    six = message.message_id
    
    text = 'Отлично, введите коментарий к бронированию, ваши пожелания'
    seven = await message.answer(text = text)
    await state.update_data(time_book = time_book, six = six, seven = seven.message_id)
    await state.set_state(Book.coment)
    

@book_rt.message(Book.coment)
async def coment(message: Message, state: FSMContext):
        
    coment_message = message.text
    eight = message.message_id
    
    button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = 'Подтвердить бронь', callback_data=f'booking_{message.from_user.id}')]
    ])
    
    text = 'Спасибо, ваши данные для брони успешно сохранены! Отправте их для подтверждения'
    
    nine = await message.answer(text = text,reply_markup=button)
    
    await state.update_data(coment_message = coment_message, eight = eight, nine = nine.message_id)
    await state.set_state(Book.book)

    
@book_rt.callback_query(lambda c: c.data and c.data.startswith('booking_'), Book.book)
async def book_in_bot(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split('_')[1]
    data = await state.get_data()
    
    second = data.get('second')
    
    if second is None:
        messeges = [data["first"],  data["four"], data["five"], data["six"], data["seven"], data["eight"], data["nine"]]
    else:
        messeges = [data["first"], data["second"], data["third"], data["four"], data["five"], data["six"], data["seven"],data["eight"], data["nine"]]
    
    yes_no_book = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = 'Забронировано', callback_data=f'booked_{user_id}'), InlineKeyboardButton(text = 'Отказано', callback_data=f'denied_{user_id}')],
        [InlineKeyboardButton(text = 'Полная посадка', callback_data=f'full_{user_id}')]
    ])
    text = f'<b>Новая бронь!\nИмя - {callback.message.from_user.first_name}\nНомер телефона - {data["phone_number"]}\nКол-во человек - {data["count_people"]}\nВремя - {data["time_book"]}\nКоментарий - {data["coment_message"]}\nUserId - {user_id}</b>'
    for admin in ADMINS:
        await callback.bot.send_message(chat_id=admin, text=text, reply_markup=yes_no_book)
    
    text_succes = 'Бронь успешно отправлена!'
    await callback.answer(text = text_succes, show_alert=True)
    try: 
        await callback.bot.delete_messages(chat_id=user_id, message_ids=messeges)
    except:
        pass

@book_rt.callback_query(lambda c: c.data and c.data.startswith('booked_'))
async def booked(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]

    text = 'Ваша бронь одобрена, ждем вас!'
    
    message1 = await callback.bot.send_message(chat_id=user_id, text=text)
    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    
    await asyncio.sleep()
    await callback.bot.delete_message(chat_id=user_id, message_id=message1.message_id)
    
@book_rt.callback_query(lambda c: c.data and c.data.startswith('denied_'))
async def booked(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]
    
    text = 'Ваша бронь отклонена, возможно в заполненной вами анкете, были какие-либо проблемы. Попробуйте связаться с нами чуть позже по телефону'
    
    await callback.bot.send_message(chat_id=user_id, text=text)
    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)

@book_rt.callback_query(lambda c: c.data and c.data.startswith('full_'))
async def booked(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]
    
    text = 'К сожалению, на выбранное вами время у нас полная посадка...'
    
    await callback.bot.send_message(chat_id=user_id, text=text)
    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    
    