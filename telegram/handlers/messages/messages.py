import shutil
import os
from time import time, time_ns

from aiogram.types import Message
from aiogram.types.input_file import FSInputFile

from utils import get_filename
from config.media import INPUT_PATH, OUTPUT_PATH

from .log import logger
from ..__data.constants import TEMPLATES
from ..__data.objects import last_time_media_added, resizer
from ...utils import get_username


async def message_handler(msg: Message):
    global last_time_media_added

    username = get_username(msg.from_user)
    logger.info(msg=f'Got message from {username}')

    if msg.content_type.lower() not in ('photo', 'document'):
        await msg.reply(TEMPLATES['invalid_file'])
        return

    epoch = time()
    
    for path in (INPUT_PATH, OUTPUT_PATH):
        parent_dirs = os.listdir(path)
        for dir in parent_dirs:
            if int(epoch) - int(dir) > 3600:
                shutil.rmtree(os.path.join(path, dir))

    media = msg.document if msg.document else msg.photo[-1]
    file = await msg.bot.get_file(media.file_id)

    if epoch - last_time_media_added > 1800:
        last_time_media_added = int(epoch)
        

    filename = f"{time_ns()}.{get_filename(file.file_path).split('.')[-1]}"
    input_path = os.path.join(INPUT_PATH, str(last_time_media_added))
    os.makedirs(input_path, exist_ok=True)
    input_path = os.path.join(input_path, filename)
    output_path = os.path.join(OUTPUT_PATH, str(last_time_media_added))
    os.makedirs(output_path, exist_ok=True)

    await msg.bot.download(file.file_id, input_path)
    resized_path = resizer.resize_photo_to_a4(input_path, output_path)

    await msg.answer_document(FSInputFile(resized_path))
