from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, 
                           ReplyKeyboardMarkup, KeyboardButton)

# Импорт кнопки выбора номера телефона
from app.keyboards.main_buttons import phone_number



# Самовывоз
self_delivery = [
    [KeyboardButton(text = 'Самовывоз')]
]

# Главная клавиатура заказа
order_button = InlineKeyboardMarkup(inline_keyboard=[
    
    [InlineKeyboardButton(text = 'Через бота', callback_data=f'order_in_bot'), 
    InlineKeyboardButton(text = 'Позвонить по телефону', callback_data='call_phone_order')],
    
    [InlineKeyboardButton(text = 'Назад', callback_data='back_in_home')]
])

# Кнопка выбора адреса во время заказа если зарегистрирован пользователь
order_button_adres_if_reg = ReplyKeyboardMarkup(keyboard= self_delivery +
                                                
        [[KeyboardButton(text = 'Мой адрес')]], 
        resize_keyboard=True, input_field_placeholder='Введите адрес доставки...', 
                        one_time_keyboard=True)

# Кнопка выбора адреса во время заказа если не зарегистрирован пользователь
order_button_adres_if_not_reg = ReplyKeyboardMarkup(keyboard=self_delivery, 
                        resize_keyboard=True, input_field_placeholder='Введите адрес доставки...', 
                        one_time_keyboard=True)

# Кнопка для выбора времени доставки
order_time = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'По мере готовности')]], 
            resize_keyboard=True, input_field_placeholder='Введите на какое время доставка...',
            one_time_keyboard=True)

# Кнопка возврата к заказу
back_to_ordering = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Назад", callback_data='oreder')]
])

# Номер телефона во время заказа 
phone_number_in_order = ReplyKeyboardMarkup(keyboard=phone_number, 
                        resize_keyboard=True, 
                        input_field_placeholder='Поделитесь своим номером телефона...', 
                        one_time_keyboard=True)

# Кнопка подтверждения заказа от пользователя
order_yes_no_user = InlineKeyboardMarkup(inline_keyboard=[
    
    [InlineKeyboardButton(text='Да', callback_data=f'post_order'), 
    InlineKeyboardButton(text='Отменить', callback_data='no_order')]
])