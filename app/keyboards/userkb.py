from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# Главное меню, для пользователя который зарегистрирован в заведении
start_in_place = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Меню', callback_data='menu_cafe')],
    [InlineKeyboardButton(text = 'Позвать официанта', callback_data='call_oficient'), InlineKeyboardButton(text='Попросить счёт', callback_data='account')],
    [InlineKeyboardButton(text = 'Инструкция', url = 'https://telegra.ph/Instrukciya-po-ehkspluatacii-bota-04-01')],
    [InlineKeyboardButton(text = 'Заврешить посещение', callback_data='exit_in_cafe')]
])

# Главное меню, для пользователя которые дома
buttons_start_in_home = [
    [InlineKeyboardButton(text='Меню', callback_data='menu_home')],
    [InlineKeyboardButton(text = 'Забронировать столик', callback_data='booking'), InlineKeyboardButton(text='Сделать заказ', callback_data='oreder')]
]

# Главное меню, для пользователя которые дома, не зарегистрирован
start_in_home_not_reg = InlineKeyboardMarkup(inline_keyboard=buttons_start_in_home + 
                                            [[InlineKeyboardButton(text='Инструкция', url='https://telegra.ph/Instrukciya-po-ehkspluatacii-bota-04-01'), 
                                            InlineKeyboardButton(text='Пройти регистрацию', callback_data='registration')]])

# Главное меню, для пользователя которые дома, зарегистрирован
start_in_home = InlineKeyboardMarkup(inline_keyboard=buttons_start_in_home + [[InlineKeyboardButton(text = 'Инструкция', url = 'https://telegra.ph/Instrukciya-po-ehkspluatacii-bota-04-01')]])

# Кнопка если пользователь после кафе хочет заказать дома что-то
start_in_home_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начть', callback_data=f'start_in_home_button')]
])

# Главные кнопки меню, разделение на категории
# Список разделов
buttons_categories = [
    [InlineKeyboardButton(text='Наши Новинки', callback_data='new')],
    [InlineKeyboardButton(text='Бургеры', callback_data='burgers'), InlineKeyboardButton(text='Горячие блюда', callback_data='hot_dishes')],
    [InlineKeyboardButton(text='Горячие роллы', callback_data='hot_rolls'), InlineKeyboardButton(text='Открытые роллы', callback_data='open_rolls')],
    [InlineKeyboardButton(text='Закрытые роллы', callback_data='closse_rolls'), InlineKeyboardButton(text='Пасты', callback_data='pasts')],
    [InlineKeyboardButton(text='Пиццы', callback_data='pizzs'), InlineKeyboardButton(text='Салаты', callback_data='salads')],
    [InlineKeyboardButton(text='Закуски', callback_data='snacks'), InlineKeyboardButton(text='Нарезки', callback_data='slices')],
    [InlineKeyboardButton(text='Соусы', callback_data='sous')],
]

# Создание клавиатуры для кафе
main_menu_cafe = InlineKeyboardMarkup(inline_keyboard=buttons_categories + [[InlineKeyboardButton(text='Назад', callback_data='back_in_cafe')]])

# Создание клавиатуры для дома
main_menu_home = InlineKeyboardMarkup(inline_keyboard=buttons_categories + [[InlineKeyboardButton(text='Назад', callback_data='back_in_home')]])



book_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Забронировать', callback_data=f'booking_new'), InlineKeyboardButton(text = 'Позвонить по телефону', callback_data='call_phone')],
    [InlineKeyboardButton(text = 'Назад', callback_data='back_in_home')]
])

order_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Через бота', callback_data=f'order_in_bot'), InlineKeyboardButton(text = 'Позвонить по телефону', callback_data='call_phone_order')],
    [InlineKeyboardButton(text = 'Назад', callback_data='back_in_home')]
])

phone_number = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Поделиться номером', request_contact=True)],
    [KeyboardButton(text = 'Завершить')]
], resize_keyboard=True, input_field_placeholder='Поделитесь своим номером телефона...', one_time_keyboard=True)

phone_number_book = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Поделиться номером', request_contact=True)]
], resize_keyboard=True, input_field_placeholder='Поделитесь своим номером телефона...', one_time_keyboard=True)

count_people = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = '1 человек'), KeyboardButton(text = '2 человека')],
    [KeyboardButton(text = '4 человека'), KeyboardButton(text = 'более 4-х человек')]
], resize_keyboard=True, input_field_placeholder='На сколько персон столик?..', one_time_keyboard=True)


stop_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Завершить')]
], resize_keyboard=True)

back_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Назад", callback_data='back_menu')]
])

back_book = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Назад", callback_data='booking')]
])

back_order = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Назад", callback_data='oreder')]
])

booking_yes_no = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Одобрить', callback_data='yes_book'), InlineKeyboardButton(text='Отказать', callback_data='no_book')]
])

order_button_adres_if_reg = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Мой адрес'), KeyboardButton(text = 'Самовывоз')]
], resize_keyboard=True, input_field_placeholder='Введите адрес доставки...', one_time_keyboard=True)

order_button_adres_if_not_reg = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Самовывоз')]
], resize_keyboard=True, input_field_placeholder='Введите адрес доставки...', one_time_keyboard=True)

order_time = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'По мере готовности')]
], resize_keyboard=True, input_field_placeholder='Введите на какое время доставка...', one_time_keyboard=True)

order_yes_no_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data=f'post_order'), InlineKeyboardButton(text='Отменить', callback_data='no_order')]
])


