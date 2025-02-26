from time import time

from aiogram import Router

from resizer import Resizer
from config.media import OUTPUT_PATH

router = Router()
resizer = Resizer(OUTPUT_PATH)

last_time_media_added = int(time())
