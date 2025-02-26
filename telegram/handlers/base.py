from inspect import signature
from log import logger
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.utils import get_access_level, is_user_in, add_user
from .__data.objects import router
from .__data.constants import TEMPLATES
from .utils import get_command, get_state, get_exception
from .messages.messages import message_handler


@router.message(F.chat.type == "private")
async def main(msg: Message, state: FSMContext):
    if not is_user_in(msg.from_user.id):
        add_user(msg.from_user)
        await msg.answer(TEMPLATES['for_newbie'])
        return
    try:
        text, args = msg.text, [msg]
        access_lvl = get_access_level(msg.from_user.id)
        state_data = await state.get_state()
        if text and text.startswith("/"):
            handler = get_command(text.split()[0][1:], access_lvl)
        elif text and state_data is not None:
            handler = get_state(state_data, access_lvl)
        else:
            handler = message_handler
    except BaseException as err:
        handler = get_exception(err)

    if handler is None:
        return
    if "state" in signature(handler).parameters:
        args.append(state)
    await handler(*args)
