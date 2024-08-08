from .components.mini_turtle_component import MiniTurtleComponent, GlobalComponentState


class MiniTurtle(MiniTurtleComponent):

    def __init__(self, *args: MiniTurtleComponent):
        super().__init__()
        self.has_input = True
        self.turtles: tuple[MiniTurtleComponent, ...] = args

    def state_help(self):
        for component in self.turtles:
            print(component.state_help())

    def input(self, **kwargs):
        for turtle in self.turtles:
            if turtle.has_input:
                turtle.input()
        raise NotImplementedError()
