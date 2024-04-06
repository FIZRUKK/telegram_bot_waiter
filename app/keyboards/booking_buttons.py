from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, 
                           ReplyKeyboardMarkup, KeyboardButton)

# Импорт кнопки выбора номера телефона
from app.keyboards.main_buttons import phone_number



# Главная клавиатура бронирования
booking_button = InlineKeyboardMarkup(inline_keyboard=[
    
    [InlineKeyboardButton(text = 'Забронировать', callback_data='booking_new'), 
    InlineKeyboardButton(text = 'Позвонить по телефону', callback_data='call_phone')],
    
    [InlineKeyboardButton(text = 'Назад', callback_data='back_in_home')]
])

# Кнопка запроса номера во время бронирования
phone_number_in_booking = ReplyKeyboardMarkup(keyboard=phone_number, 
                        resize_keyboard=True, 
                        input_field_placeholder='Поделитесь своим номером телефона...', 
                        one_time_keyboard=True)

# Кнопка возварата к броинрованию
back_to_booking = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Назад", callback_data='booking')]
])

# Кнопка кол-ва посетителей во время бронирования
count_people = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = '1 человек'), KeyboardButton(text = '2 человека')],
    [KeyboardButton(text = '4 человека'), KeyboardButton(text = 'более 4-х человек')]],
                    resize_keyboard=True, input_field_placeholder='На сколько персон столик?..', 
                    one_time_keyboard=True)