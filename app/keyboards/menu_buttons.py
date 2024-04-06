from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, 
                           ReplyKeyboardMarkup, KeyboardButton)



# Список разделов
buttons_categories = [
    [InlineKeyboardButton(text='Наши Новинки', callback_data='new')],
    
    [InlineKeyboardButton(text='Бургеры', callback_data='burgers'), 
    InlineKeyboardButton(text='Горячие блюда', callback_data='hot_dishes')],
    
    [InlineKeyboardButton(text='Горячие роллы', callback_data='hot_rolls'),
    InlineKeyboardButton(text='Открытые роллы', callback_data='open_rolls')],
    
    [InlineKeyboardButton(text='Закрытые роллы', callback_data='closse_rolls'), 
    InlineKeyboardButton(text='Пасты', callback_data='pasts')],
    
    [InlineKeyboardButton(text='Пиццы', callback_data='pizzs'), 
    InlineKeyboardButton(text='Салаты', callback_data='salads')],
    
    [InlineKeyboardButton(text='Закуски', callback_data='snacks'), 
    InlineKeyboardButton(text='Нарезки', callback_data='slices')],
    
    [InlineKeyboardButton(text='Соусы', callback_data='sous')],
]

# Создание клавиатуры для кафе
main_menu_cafe = InlineKeyboardMarkup(inline_keyboard=buttons_categories + 
                    [[InlineKeyboardButton(text='Назад', callback_data='back_in_cafe')]])

# Создание клавиатуры для дома
main_menu_home = InlineKeyboardMarkup(inline_keyboard=buttons_categories + 
                    [[InlineKeyboardButton(text='Назад', callback_data='back_in_home')]])

# Кнопка возврата в меню
back_in_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Назад", callback_data='back_menu')]
])