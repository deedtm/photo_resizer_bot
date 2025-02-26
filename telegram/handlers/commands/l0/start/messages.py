from ....__utils import get_handler_template
from aiogram.types import Message


async def handler(msg: Message):
    template = get_handler_template(__file__)
    text = template.format()
    await msg.answer(text)
