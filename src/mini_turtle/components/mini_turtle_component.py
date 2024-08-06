import inspect
from collections import defaultdict
from typing import Callable, Any, cast

from typedict import TypeDict


class GlobalComponentState:
    _KEY_TO_FN: dict[str, Callable[[Any, ...], Any]] = dict()
    _KEY_TO_ARGS: dict[str, list[str]] = dict()
    _ARG_TO_FN: dict[str, str] = dict()
    _ARG_VALUES: dict[str, Any] = defaultdict(lambda: None)

    @classmethod
    def _set_arg_value(cls, key: str, value: Any) -> None:
        cls._ARG_VALUES[key] = value

    @classmethod
    def _trigger_update(cls, key: str):
        cls._KEY_TO_FN[key](*[cls._ARG_VALUES[arg] for arg in cls._KEY_TO_ARGS[key]])

    @classmethod
    def add_observer(cls, key: str, fn: Callable[[Any, ...], Any], update_on: list[str]) -> None:
        cls._KEY_TO_FN[key] = fn
        cls._KEY_TO_ARGS[key] = [arg.name for arg in inspect.signature(fn).parameters.values()]
        for arg in update_on:
            cls._ARG_TO_FN[arg] = key

    @classmethod
    def update_state(cls, **kwargs):
        update_functions: set[str] = set()
        for k, v in kwargs.items():
            cls._set_arg_value(k, v)
            if k in cls._ARG_TO_FN:
                update_functions.add(cls._ARG_TO_FN[k])
        for fn in update_functions:
            cls._trigger_update(fn)


def use_state(state_id: str, update_on: list[str] | None = None) -> Callable:
    def inner(fn: Callable):
        fn.__state_observer = state_id
        fn.__state_update_on = update_on
        return fn

    return inner


class StateComponent(TypeDict):
    fn_name: str
    update_on: list[str]


class MiniTurtleComponent:

    def __init__(self):
        self.state = GlobalComponentState()
        for class_state_component in self._state_methods():
            GlobalComponentState.add_observer(
                class_state_component["fn_name"],
                getattr(self, class_state_component["fn_name"]),
                class_state_component["update_on"],
            )

    def _state_methods(self) -> list[StateComponent]:
        return [
            cast(
                StateComponent,
                {"fn_name": fn_name, "update_on": getattr(fn, '__state_update_on', args)}
            )
            for fn_name, fn in inspect.getmembers(self, inspect.ismethod)
            if hasattr(fn, '__state_observer')
            if (args := [arg.name for arg in inspect.signature(fn).parameters.values()])
        ]

    def state_help(self):
        return (
            f"==== {self.__class__.__name__} ====\n"
            "\n".join(
                f"{i + 1}. {component.fn_name} (Updates on: {update_args})"
                for i, component in enumerate(self._state_methods())
                if (update_args := ", ".join(component.update_on))
            )
        )