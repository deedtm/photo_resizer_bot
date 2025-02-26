from aiogram.types import User


def get_username(user: User):
    return '@' + user.username if user.username else f"id{user.id}"    
    