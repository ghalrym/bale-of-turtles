import logging
from collections import defaultdict
from typing import Callable, Any

logger = logging.getLogger(__name__)


class _TurtleStateManager:
    _TRIGGER_QUEUE: list[str] = list()
    _TRIGGER_KEY_TO_FUNCTIONS: dict[str, Callable[[str, ...], None]] = dict()
    _STATE: dict[str, Any] = defaultdict(lambda: None)
    _STATE_TO_TRIGGER_KEY: dict[str, list[str]] = defaultdict(list)

    @classmethod
    def update_state(cls, **kwargs):
        for key, value in kwargs.items():
            cls._STATE[key] = value
            cls._TRIGGER_QUEUE.extend(set(cls._STATE_TO_TRIGGER_KEY[key]) - set(cls._TRIGGER_QUEUE))

    @classmethod
    def trigger(cls, trigger_key):
        trigger = cls._TRIGGER_KEY_TO_FUNCTIONS.get(trigger_key, None)
        if trigger is None:
            logger.warning(f"{trigger_key} is not a registered trigger")
        else:
            trigger(**cls._STATE)

    @classmethod
    def invoke(cls):
        while len(cls._TRIGGER_QUEUE) > 0:
            trigger = cls._TRIGGER_QUEUE.pop(0)
            cls.trigger(trigger)


def use_state(key: str, update_on: list[str]):

    # noinspection PyProtectedMember
    def inner(fn: Callable[..., Any]):
        _TurtleStateManager._TRIGGER_KEY_TO_FUNCTIONS[key] = fn
        for trigger_key in update_on:
            _TurtleStateManager._STATE_TO_TRIGGER_KEY[trigger_key].append(key)
        return fn
    return inner


def use_trigger(key: str):
    return use_state(key, [])
