from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import PHONE_NUMBER, MAIN_ADMIN
from app.media.photos_id import MAIN_BOOKING_PHOTO

import app.keyboards.booking_buttons as kb_booking
from app.database.requests import user_yes_no, get_phone_number

import asyncio

# Роутер
book_rt = Router()

# Класс состояний для бронирования столика
class Book(StatesGroup):
    phone_number = State() # Номер телефона клиента
    count_people = State() # Кол-во посетителей будет
    time = State() # На какое время бронировать
    coment = State() # Коментарий к бронированию
    book = State() # Заключительная часть в бронировании

# Обработчик для кнопки     
@book_rt.callback_query(F.data == 'booking')
async def main_booking(callback: CallbackQuery):
    
    booking_photo = MAIN_BOOKING_PHOTO
    
    text = f'<b>Привет</b>'
    
    media = InputMediaPhoto(media=booking_photo, caption=text)
    
    await callback.message.edit_media(media = media, reply_markup=kb_booking.booking_button)

# Если бронь по телефону    
@book_rt.callback_query(F.data == 'call_phone')
async def book_call_phone(callback: CallbackQuery):

    text = f'Свяжитесь с нами и заброниируйте столик по этому номеру  {PHONE_NUMBER}'
    
    await callback.message.edit_caption(caption=text, reply_markup=kb_booking.back_to_booking)
    
# Если бронь через бота    
@book_rt.callback_query(F.data == 'booking_new')
async def booking_new(callback: CallbackQuery, state: FSMContext):
    
    if await user_yes_no(callback.from_user.id):
        
        text = 'Введите ваш номер телефона, для обратной связи или нажмите на кнопку ниже, чтобы поделиться им'
        
        first_message = await callback.message.answer(text = text, 
                                        reply_markup=kb_booking.phone_number_in_booking)
        await state.set_state(Book.phone_number)
        await state.update_data(first_message = first_message.message_id)
    else:
        phone_number = await get_phone_number(callback.from_user.id)
        
        text = 'Ваш номер у нас есть, выберите на сколько персон столик?'
        
        first_message = await callback.message.answer(text=text, reply_markup=kb_booking.count_people)
        await state.update_data(phone_number = phone_number, first_message = first_message.message_id) 
        await state.set_state(Book.count_people)

# Обработчик номера телефона
@book_rt.message(Book.phone_number)
async def phone_number(message: Message, state: FSMContext):
    
    second_message = message.message_id
    
    if message.content_type == 'contact':
        # Если есть контакт, записываем номер телефона
        phone_number = message.contact.phone_number
    else:
        # Если контакта нет, записываем текст сообщения
        phone_number = message.text
    
    text = 'Ваш номер успешно записан, выберите на сколько персон столик?'
    
    third_message = await message.answer(text = text, reply_markup=kb_booking.count_people)
    
    await state.update_data(phone_number = phone_number, second_message = second_message, 
                            third_message = third_message.message_id)
    
    await state.set_state(Book.count_people)

# Обработчик кол-ва человек       
@book_rt.message(Book.count_people)
async def count_people(message: Message, state: FSMContext):
    count_people = message.text
    fourth_message = message.message_id

    text = 'Отлично, введите на какое время вам забронировать?\nПример: 18 апреля 18:00'
    
    fifth_message = await message.answer(text = text, reply_markup=ReplyKeyboardRemove())
    
    await state.update_data(count_people = count_people, fourth_message = fourth_message,
                            fifth_message = fifth_message.message_id)
    
    await state.set_state(Book.time)

# Обработчик на какое время бронировать
@book_rt.message(Book.time)
async def time_book(message: Message, state: FSMContext):
    
    time_book = message.text
    sixth_message = message.message_id
    
    text = 'Отлично, введите коментарий к бронированию, ваши пожелания'
    seventh_message = await message.answer(text = text)
    
    await state.update_data(time_book = time_book, sixth_message = sixth_message,
                            seventh_message = seventh_message.message_id)
    
    await state.set_state(Book.coment)
    
# Обработчик коментария
@book_rt.message(Book.coment)
async def coment(message: Message, state: FSMContext):
        
    coment_message = message.text
    eighth_message = message.message_id
    
    button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = 'Подтвердить бронь', callback_data=f'booking_{message.from_user.id}')]
    ])
    
    text = 'Спасибо, ваши данные для брони успешно сохранены! Отправте их для подтверждения'
    
    ninth_message = await message.answer(text = text,reply_markup=button)
    
    await state.update_data(coment_message = coment_message, eighth_message = eighth_message, 
                        ninth_message = ninth_message.message_id)
    
    await state.set_state(Book.book)

# Обработчик для отправки брони админам   
@book_rt.callback_query(lambda c: c.data and c.data.startswith('booking_'), Book.book)
async def book_in_bot(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split('_')[1]
    data = await state.get_data()
    
    second_message = data.get('second_message')
    
    if second_message is None:
        messeges = ([data["first_message"],  data["fourth_message"], 
                    data["fifth_message"], data["sixth_message"],
                    data["seventh_message"], data["eighth_message"], data["ninth_message"]])
    else:
        messeges = ([data["first_message"], data["second_message"], data["third_message"], 
                    data["fourth_message"], data["fifth_message"], data["sixth_message"], 
                    data["seventh_message"],data["eighth_message"], data["ninth_message"]])
    
    yes_no_book = InlineKeyboardMarkup(inline_keyboard=[
        
        [InlineKeyboardButton(text = 'Забронировано', callback_data=f'booked_{user_id}'), 
        InlineKeyboardButton(text = 'Отказано', callback_data=f'denied_{user_id}')],
        
        [InlineKeyboardButton(text = 'Полная посадка', callback_data=f'full_{user_id}')]
    ])
    
    text = f'<b>Новая бронь!\nИмя - {callback.message.from_user.first_name}\nНомер телефона - {data["phone_number"]}\nКол-во человек - {data["count_people"]}\nВремя - {data["time_book"]}\nКоментарий - {data["coment_message"]}\nUserId - {user_id}</b>'
    
    await callback.bot.send_message(chat_id=MAIN_ADMIN, text=text, reply_markup=yes_no_book)
    
    text_succes = 'Бронь успешно отправлена!'
    await callback.answer(text = text_succes, show_alert=True)
    try: 
        await callback.bot.delete_messages(chat_id=user_id, message_ids=messeges)
    except:
        pass

# Обработчик успешной брони
@book_rt.callback_query(lambda c: c.data and c.data.startswith('booked_'))
async def booked(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]

    text = 'Ваша бронь одобрена, ждем вас!'
    
    message1 = await callback.bot.send_message(chat_id=user_id, text=text)
    
    await callback.bot.delete_message(chat_id=callback.from_user.id, 
                                    message_id=callback.message.message_id)
    
    await asyncio.sleep()
    await callback.bot.delete_message(chat_id=user_id, message_id=message1.message_id)

# Обработчик отклоненной брони    
@book_rt.callback_query(lambda c: c.data and c.data.startswith('denied_'))
async def booked(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]
    
    text = 'Ваша бронь отклонена, возможно в заполненной вами анкете, были какие-либо проблемы. Попробуйте связаться с нами чуть позже по телефону'
    
    await callback.bot.send_message(chat_id=user_id, text=text)
    
    await callback.bot.delete_message(chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id)

# Обработчик полной посадки
@book_rt.callback_query(lambda c: c.data and c.data.startswith('full_'))
async def booked(callback: CallbackQuery):
    user_id = callback.data.split('_')[1]
    
    text = 'К сожалению, на выбранное вами время у нас полная посадка...'
    
    await callback.bot.send_message(chat_id=user_id, text=text)
    
    await callback.bot.delete_message(chat_id=callback.from_user.id, 
                                    message_id=callback.message.message_id)
    
    