from app.database.models import User, async_session
from sqlalchemy import select, func, update, delete


# добавление пользователя в базу по user_id
async def input_user(user_id, user_name, first_name, last_name, phone_number, adres, birthday):
    async with async_session() as session:
        new_user = User(user_id=user_id, user_name=user_name, first_name=first_name,
                        last_name=last_name, phone_number = phone_number,
                        adres = adres, birthday = birthday)

        session.add(new_user)
        await session.commit()

# Проверка есть ли юзер в базе по user_id
async def user_yes_no(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        if not user:
            return True

# Поиск номера телефона по user_id
async def get_phone_number(user_id):
    async with async_session() as session:
        
        user = (await session.execute(select(User).where(
            User.user_id == user_id
            ))).scalars().first()
        
        user = user.__dict__
        if user:
            return user['phone_number']
        else:
            None

# Поиск адреса по user_id
async def get_adres_user(user_id):
    async with async_session() as session:
        
        user = (await session.execute(select(User).where(
            User.user_id == user_id
            ))).scalars().first()
        
        user = user.__dict__
        if user:
            return user['adres']
        else:
            None
            