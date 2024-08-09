from bale_of_turtles._turtle_state import _TurtleStateManager


class LlmTurtle:

    def __init__(self, name: str):
        self.name = name
        self.state = _TurtleStateManager()

    def invoke(self, *args):
        raise NotImplementedError()

    def __call__(self):
        return self.invoke()
