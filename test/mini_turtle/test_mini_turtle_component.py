from mini_turtle.components.mini_turtle_component import use_state, MiniTurtleComponent


class TestMiniTurtleComponent(MiniTurtleComponent):

    def __init__(self):
        super().__init__()
        self.last_text = None
        self.last_volume = None

    @use_state("say", update_on=["volume"])
    def say_quietly(self, text: str | None, volume: int):
        self.last_text = text
        self.last_volume = volume


def test_use_state():
    test_component = TestMiniTurtleComponent()
    test_component.state.update_state(text="test 1 2 3")
    assert test_component.last_text is None

    test_component.state.update_state(volume=5)
    assert test_component.last_text == "test 1 2 3"
    assert test_component.last_volume == 5
