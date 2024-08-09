import inspect
import logging
from collections import defaultdict
from typing import Callable, Any

logger = logging.getLogger(__name__)


class DuplicateTurtleFunctionKey(Exception):

    def __init__(self, key):
        super().__init__(f"Duplicate key found in use state, {key}")


class _TurtleStateManager:
    __slots__ = (
        "_trigger_queue",
        "_trigger_key_to_functions",
        "_state",
        "_state_to_trigger_key",
    )

    def __init__(self):
        self._trigger_queue: list[str] = list()
        self._trigger_key_to_functions: dict[str, Callable[[str, ...], None]] = dict()
        self._state: dict[str, Any] = defaultdict(lambda: None)
        self._state_to_trigger_key: dict[str, list[str]] = defaultdict(list)

    def get_state(self, key: str, default_value: Any = None) -> Any:
        return self._state.get(key, default_value)

    def update_state(self, **kwargs):
        for key, value in kwargs.items():
            self._state[key] = value
            self._trigger_queue = list(
                dict.fromkeys(self._trigger_queue + self._state_to_trigger_key[key])
            )
        self.invoke()

    def trigger(self, trigger_key):
        trigger = self._trigger_key_to_functions.get(trigger_key, None)
        if trigger is None:
            logger.warning(f"{trigger_key} is not a registered trigger")
        else:
            trigger(**self._state)

    def register_tool(self, obj: object) -> None:
        for function_name, function in inspect.getmembers(obj, inspect.ismethod):
            if not (key := getattr(function, "__turtle__", None)):
                continue

            # If the key already exists raise error
            if key in self._trigger_key_to_functions:
                raise DuplicateTurtleFunctionKey(key)

            update_on: list[str] = getattr(function, "__turtle_update_on__", [])
            self._trigger_key_to_functions[key] = function
            for trigger_key in update_on:
                self._state_to_trigger_key[trigger_key].append(key)

            # todo: validate that the function has *args and **kwargs

    def invoke(self):
        while len(self._trigger_queue) > 0:
            trigger = self._trigger_queue.pop(0)
            self.trigger(trigger)

    def __call__(self):
        return self.invoke()


def use_state(
    key: str, update_on: list[str]
) -> Callable[[Callable], Callable[..., Any]]:

    # noinspection PyProtectedMember
    def inner(fn: Callable[..., Any]) -> Callable[..., Any]:
        setattr(fn, "__turtle__", key)
        setattr(fn, "__turtle_update_on__", update_on)
        return fn

    return inner


def use_trigger(key: str):
    return use_state(key, [])
