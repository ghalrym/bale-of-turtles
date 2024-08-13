from threading import Thread

from pydantic import BaseModel

from ._turtle_state import _TurtleStateManager
from .tool_turtle import TurtleTool


class ActionTurtle(TurtleTool):
    __slots__ = ('_thread',)

    def __init__(
        self,
        grant_access: bool = False,
        expect_context: BaseModel | None = None,
    ):
        super().__init__(grant_access, expect_context)
        self._thread: Thread | None = None

    def register(self, state: _TurtleStateManager):
        self._thread = Thread(target=self.invoke)
        self._thread.start()

    def invoke(self):
        ...
