from ._turtle_state import _TurtleStateManager


class TurtleLLM:

    def __init__(self, model: str, name: str):
        self._model = model
        self.name = name
        self.state = _TurtleStateManager()

    def invoke(self):
        raise NotImplementedError()
