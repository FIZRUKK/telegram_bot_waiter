import os

from sqlalchemy import  String, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from dotenv import load_dotenv

from config import ENGINE

load_dotenv()

engine = create_async_engine(ENGINE, echo = True)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement = True)
    
    user_id: Mapped[int] = mapped_column(BigInteger)
    user_name: Mapped[str] = mapped_column(String(32), nullable = True)
    
    first_name: Mapped[str] = mapped_column(String(64), nullable = True)
    last_name: Mapped[str] = mapped_column(String(64), nullable = True)
    
    phone_number: Mapped[str] = mapped_column(String(15), nullable = True)
    adres: Mapped[str] = mapped_column(String(128), nullable = True)
    birthday: Mapped[str] = mapped_column(String(15), nullable = True)
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)