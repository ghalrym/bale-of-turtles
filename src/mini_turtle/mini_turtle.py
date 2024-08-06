from mini_turtle.components.mini_turtle_component import MiniTurtleComponent, GlobalComponentState


class MiniTurtle:

    def __init__(self, *args: MiniTurtleComponent):
        self.turtles: tuple[MiniTurtleComponent, ...] = args
        self._state: GlobalComponentState = GlobalComponentState()

    def help(self):
        for component in self.turtles:
            print(component.state_help())

    def input(self, *args, **kwargs):
        raise NotImplementedError()