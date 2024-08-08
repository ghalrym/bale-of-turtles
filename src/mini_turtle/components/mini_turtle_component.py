import inspect
from collections import defaultdict
from typing import Callable, Any, cast, TypedDict


class StateComponent(TypedDict):
    key: str
    fn: Callable[[Any, ...], Any]
    update_on: list[str]


class GlobalComponentState:
    _KEY_TO_FN: dict[str, Callable[[Any, ...], Any]] = dict()
    _KEY_TO_ARGS: dict[str, list[str]] = dict()
    _ARG_TO_FN: dict[str, str] = dict()
    _ARG_VALUES: dict[str, Any] = defaultdict(lambda: None)

    @classmethod
    def _set_arg_value(cls, key: str, value: Any) -> None:
        cls._ARG_VALUES[key] = value

    @classmethod
    def add_observer(cls, key: str, fn: Callable[[Any, ...], Any], update_on: list[str]) -> None:
        cls._KEY_TO_FN[key] = fn
        cls._KEY_TO_ARGS[key] = [arg.name for arg in inspect.signature(fn).parameters.values()]
        for arg in update_on:
            cls._ARG_TO_FN[arg] = key

    @classmethod
    def trigger(cls, key: str):
        cls._KEY_TO_FN[key](*[cls._ARG_VALUES[arg] for arg in cls._KEY_TO_ARGS[key]])

    @classmethod
    def update_state(cls, **kwargs):
        update_functions: set[str] = set()
        for k, v in kwargs.items():
            cls._set_arg_value(k, v)
            if k in cls._ARG_TO_FN:
                update_functions.add(cls._ARG_TO_FN[k])
        for fn in update_functions:
            cls.trigger(fn)


def use_state(state_id: str, update_on: list[str] | None = None) -> Callable:
    def inner(fn: Callable):
        fn.__state_observer = state_id
        fn.__state_update_on = update_on
        return fn

    return inner


def use_trigger(trigger_id: str) -> Callable:
    def inner(fn: Callable):
        fn.__state_trigger = trigger_id
        return fn

    return inner


class MiniTurtleComponent:

    def __init__(self):
        self.state = GlobalComponentState()
        self.has_input = False
        for class_state_component in [*self._state_methods(), *self._trigger_methods()]:
            GlobalComponentState.add_observer(**class_state_component)

    def _state_methods(self) -> list[StateComponent]:
        return [
            cast(
                StateComponent,
                {
                    "key": getattr(fn, '__state_observer'),
                    "fn": fn,
                    "update_on": getattr(fn, '__state_update_on', args)
                }
            )
            for fn_name, fn in inspect.getmembers(self, inspect.ismethod)
            if hasattr(fn, '__state_observer')
            if (args := [arg.name for arg in inspect.signature(fn).parameters.values()])
        ]

    def _trigger_methods(self) -> list[StateComponent]:
        return [
            cast(
                StateComponent,
                {
                    "key": getattr(fn, '__state_trigger'),
                    "fn": fn,
                    "update_on": []
                }
            )
            for fn_name, fn in inspect.getmembers(self, inspect.ismethod)
            if hasattr(fn, '__state_trigger')
        ]

    def state_help(self):
        return (
            f"==== {self.__class__.__name__} ====\n"
            "\n".join(
                f"{i + 1}. {component['key']} (Updates on: {update_args})"
                for i, component in enumerate(self._state_methods())
                if (update_args := ", ".join(component['update_on']))
            )
        )

    def input(self, **kwargs):
        raise NotImplementedError()
