from aiogram import Router, F
from aiogram.types import Message, CallbackQuery


from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


from app.database.requests import input_user
import app.keyboards.main_buttons as kb

import asyncio

# Роутер
reg_rt = Router()

# Класс состояний для регистрации
class Registration(StatesGroup):
    phone_number = State()
    adres = State()
    birthday = State()
    
# Текст если пользователь завершил регистрацию
text_close = 'Очень жаль, процедура регистрации прервана...'

# Обработчик кнопки
@reg_rt.callback_query(F.data == 'registration')
async def registration(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.phone_number)
    
    text = '<b>Пройдите процедуру регистрации, чтобы в дальнейшем, вы смогли комфортно заказывать еду!\n\nПоделитесь, своим номером телефона или напишите в формате\n+7 930 695 00-00</b>'
    
    first_message = await callback.message.answer(text = text, 
                                                reply_markup=kb.phone_number_in_registration)
    
    await state.update_data(first_message = first_message.message_id)

# Обработчик номера телефона
@reg_rt.message(Registration.phone_number)
async def phone_number(message: Message, state: FSMContext):

    if message.text != 'Завершить':
        text = f'<b>Отлично, ваш номер телефона {message.contact.phone_number}\n\nНапишите ваш адрес, куда делать доставку\n\n<i>Образец: Город. Улица, дом, квартира, этаж, подьезд</i></b>'
        
        if message.content_type == 'contact':
        # Если есть контакт, записываем номер телефона
            phone_number = message.contact.phone_number
        else:
        # Если контакта нет, записываем текст сообщения
            phone_number = message.text
            
        thred_message = await message.answer(text = text, reply_markup=kb.finalize_button)
        await state.update_data(second_message = message.message_id, 
                                phone_number = phone_number,
                                thred_message = thred_message.message_id)
        
        await state.set_state(Registration.adres)
    else:
        data = await state.get_data()
        back = await message.answer(text=text_close)
        
        messages = [data["first_message"], message.message_id]
        await message.bot.delete_messages(chat_id=message.from_user.id, message_ids=messages)
        
        await state.clear()
        
        await asyncio.sleep(5)
        
        await message.bot.delete_message(chat_id=message.from_user.id, message_id=back.message_id)
        
# Обработчик адреса
@reg_rt.message(Registration.adres)
async def adres(message: Message, state: FSMContext):
    
    if message.text != 'Завершить': 
        
        text = '<b>Отлично, укажите вашу дату рождения, это позволит нам подготовить самые лучшие подарки!\n\n<i>Образец: ГГГГ:ММ:ДД</i></b>'
        
        five_message = await message.answer(text = text, reply_markup=kb.stop_button)
        
        await state.update_data(four_message = message.message_id, 
                                five_message = five_message.message_id, 
                                adres = message.text)
        
        await state.set_state(Registration.birthday)
    else:
        data = await state.get_data()
        back = await message.answer(text = text_close)
        
        messages = ([data["first_message"], data["second_message"], 
                    data["thred_message"], message.message_id])
        
        await message.bot.delete_messages(chat_id=message.from_user.id, message_ids=messages)
        
        await state.clear()
        
        await asyncio.sleep(5)
        
        await message.bot.delete_message(chat_id=message.from_user.id, message_id=back.message_id)

# Обработчик дня рождения    
@reg_rt.message(Registration.birthday)
async def birthday(message: Message, state: FSMContext):
    
    await state.update_data(six_message = message.message_id, birthday = message.text)
    
    data = await state.get_data()
    
    phone_number = data["phone_number"]
    adres = data["adres"]
    birthday = data["birthday"]
    
    text = f'<b>Спасибо за регистрацию, вот ваши данные которые вы ввели!<i>Номер телефона - {phone_number}</i>\n<i>Адрес - {adres}</i><i>День рождения - {birthday}</i></b>'
    seven_message = await message.answer(text = text)
    
    
    messages = ([data["first_message"], data["second_message"],
                data["thred_message"], data["four_message"],
                data["five_message"], data["six_message"]])
    
    await message.bot.delete_messages(chat_id=message.from_user.id, message_ids=messages)
    
    await asyncio.sleep(5)
    
    await message.bot.delete_message(chat_id=message.from_user.id, 
                                    message_id=seven_message.message_id)
    
    await input_user(message.from_user.id, message.from_user.username, 
                    message.from_user.first_name, 
                    message.from_user.last_name, phone_number, adres, birthday)
    
    await state.clear()
    