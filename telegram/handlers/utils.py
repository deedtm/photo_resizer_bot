import traceback
from .log import logger
from .exceptions import *
from .__utils import get_function
from .__data.constants import COMMANDS
from . import __handlers
from types import ModuleType


def get_access_module(command: str, access_lvl: int) -> ModuleType:
    command_data = COMMANDS.get(command)
    if command_data is None:
        raise CommandDoesNotExist(command)
    required_access = command_data['access_level']
    if access_lvl < required_access:
        raise InsufficientAccessLevel(access_lvl, required_access)
    return __handlers.get().get("l" + str(required_access))


def get_command(command: str, access_lvl: int):
    access_module = get_access_module(command, access_lvl)
    return access_module.__dict__[command].messages.handler


def get_state(state_data: str, access_lvl: int):
    command, data = state_data.split(":")[1:3]
    access_module = get_access_module(command, access_lvl)
    return get_function(access_module.__dict__[command].states, "state", data)


def get_exception(err: BaseException):
    class_name = err.__class__.__name__.lower()
    module = __handlers.get().get(class_name)
    if module and hasattr(module, "handler"):
        return module.handler
    logger.error(traceback.format_exc())
