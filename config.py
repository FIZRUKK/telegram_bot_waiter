import os

from dotenv import load_dotenv



load_dotenv()

# Движок для базы
ENGINE = os.getenv('ENGINE')

# Токен бота
TOKEN = os.getenv('TOKEN')

# ID главного администратора
MAIN_ADMIN = 2085376749

# ID админов
ADMINS = [2085376749, 2016568074]

# Название заведения
PLACE_NAME = 'By Terras'

# Номер телефона заведения
PHONE_NUMBER = '+7 930 695 80-44' 