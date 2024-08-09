from ._turtle_state import _TurtleStateManager, use_trigger
from bale_of_turtles.llm_turtle import LlmTurtle
from .tool_turtle import TurtleTool


class AgentTurtle(TurtleTool):
    __slots__ = ('turtle_tools',)

    def __init__(
        self,
        *turtle_tools: TurtleTool,
        independent_state: bool = False,
        lead_turtle: bool = False,
    ):
        super().__init__()
        self.turtle_tools = list(turtle_tools)
        if independent_state or lead_turtle:
            self.register(_TurtleStateManager())

    def register(self, state: _TurtleStateManager):
        super().register(state)
        for tool in self.turtle_tools:
            tool.register(self._state)

    def invoke(self, *args, **kwargs):
        self.update_state(**kwargs)
