from pydantic import BaseModel

from ._turtle_state import _TurtleStateManager


class UnregisteredTurtleEquipment(Exception):

    def __init__(self, turtle: "TurtleTool"):
        super().__init__("Unregistered TurtleTool: {}".format(turtle.__class__.__name__))


class TurtleTool:
    """TurtleTool are tools that manage the state for the llm. you can grant the llm
    access to call the function with `grant_access` and `expect_context`"""
    __slots__ = ['_grant_access', '_expect_context', '_state']

    def __init__(
        self,
        grant_access: bool = False,
        expect_context: BaseModel | None = None,
    ):
        self._grant_access = grant_access
        self._expect_context = expect_context
        self._state = None

    @property
    def state(self) -> _TurtleStateManager:
        if self._state is None:
            raise UnregisteredTurtleEquipment(self)
        return self._state

    def register(self, state: _TurtleStateManager):
        self._state = state
        self._state.register_tool(self)

    def invoke(self):
        ...

    def __call__(self):
        return self.invoke()
