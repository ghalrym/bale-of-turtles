from ._turtle_state import _TurtleStateManager, use_trigger
from .turtle_llm import LlmTurtle
from .turtle_tool import TurtleTool


class AgentTurtle(TurtleTool):
    __slots__ = ('_llm', 'turtle_tools')

    def __init__(
        self,
        llm: LlmTurtle,
        *turtle_tools: TurtleTool,
        independent_state: bool = False,
        lead_turtle: bool = False,
    ):
        super().__init__()
        self._llm = llm
        self.turtle_tools = list(turtle_tools)
        if independent_state or lead_turtle:
            self.register(_TurtleStateManager())

    def register(self, state: _TurtleStateManager):
        super().register(state)

        class LlmFacade:
            @use_trigger(self._llm.name)
            def trigger_llm(_):
                return self._llm.invoke()

        self._state.register_tool(self)
        self._state.register_tool(LlmFacade())
        for tool in self.turtle_tools:
            tool.register(self._state)

    def world_input(self, **kwargs):
        self.state.update_state(**kwargs)

    def invoke(self):
        self.state.trigger(self._llm.name)
