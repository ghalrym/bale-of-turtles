from ._turtle_state import _TurtleStateManager, use_trigger
from .turtle_llm import TurtleLLM
from .turtle_tool import TurtleTool


class AgentTurtle(TurtleTool):

    def __init__(self, llm: TurtleLLM, *turtle_tools: TurtleTool):
        super().__init__()
        self._llm = llm
        self.turtle_tools = list(turtle_tools)
        self.state = _TurtleStateManager()
        use_trigger(llm.name)(llm.invoke)

    def world_input(self, **kwargs):
        self.state.update_state(**kwargs)

    def invoke(self):
        self.state.trigger(self._llm.name)
