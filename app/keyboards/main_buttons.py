from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, 
                           ReplyKeyboardMarkup, KeyboardButton)




instruction_in_place = 'https://telegra.ph/Instrukciya-po-ehkspluatacii-bota-04-01'
instruction_home = 'https://telegra.ph/Instrukciya-po-ehkspluatacii-bota-04-01'

# Главное меню, для пользователя который зарегистрирован в заведении
start_in_place = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Меню', callback_data='menu_cafe')],
    
    [InlineKeyboardButton(text = 'Позвать официанта', callback_data='call_oficient'), 
    InlineKeyboardButton(text='Попросить счёт', callback_data='account')],
    
    [InlineKeyboardButton(text = 'Инструкция', url = instruction_in_place)],
    [InlineKeyboardButton(text = 'Заврешить посещение', callback_data='exit_in_cafe')]
])

# Главное меню, для пользователя которые дома
buttons_start_in_home = [
    [InlineKeyboardButton(text='Меню', callback_data='menu_home')],
    
    [InlineKeyboardButton(text = 'Забронировать столик', callback_data='booking'), 
    InlineKeyboardButton(text='Сделать заказ', callback_data='oreder')]
]

# Главное меню, для пользователя которые дома, не зарегистрирован
start_in_home_not_reg = InlineKeyboardMarkup(inline_keyboard=buttons_start_in_home + 
            [[InlineKeyboardButton(text='Инструкция', url=instruction_home), 
            InlineKeyboardButton(text='Пройти регистрацию', callback_data='registration')]])

# Главное меню, для пользователя которые дома, зарегистрирован
start_in_home = InlineKeyboardMarkup(inline_keyboard=buttons_start_in_home + 
            [[InlineKeyboardButton(text = 'Инструкция', url = instruction_home)]])

# Кнопка если пользователь после кафе хочет заказать дома что-то
start_in_home_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начть', callback_data=f'start_in_home_button')]
])

# Завершить
finalize = [
    [KeyboardButton(text = 'Завершить')]
]

# Кнопка завершить
finalize_button = ReplyKeyboardMarkup(keyboard=finalize, resize_keyboard=True)

# Номер телефона
phone_number = [
    [KeyboardButton(text = 'Поделиться номером', request_contact=True)]
]

# Кнопка запроса номера во время регистрации
phone_number_in_registration = ReplyKeyboardMarkup(keyboard = phone_number + finalize, 
    resize_keyboard=True, input_field_placeholder='Поделитесь своим номером телефона...',
    one_time_keyboard=True)