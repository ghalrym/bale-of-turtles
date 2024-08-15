import pytest

from bale_of_turtles import TurtleTool, use_state, UnregisteredTurtleEquipment
from bale_of_turtles._turtle_state import _TurtleStateManager


class TestTurtleTool(TurtleTool):

    def __init__(self):
        super().__init__()
        self.last_text = None
        self.last_volume = None
        self.say_loudly = use_state("turtle-say-loudly", update_on=["volume"])(
            self._say_loudly
        )

    @use_state("turtle-say-quietly", update_on=["volume"])
    def say_quietly(self, text: str | None, volume: int):
        self.last_text = text
        self.last_volume = volume

    def _say_loudly(self, **kwargs):
        self.last_loud = kwargs

    def invoke(self):
        raise Exception("Expected exception")


def test_use_state():
    test_component = TestTurtleTool()
    test_component.register(_TurtleStateManager())

    test_component.state.update_state(text="test 1 2 3")
    assert test_component.last_text is None

    test_component.state.update_state(volume=5)
    assert test_component.last_text == "test 1 2 3"
    assert test_component.last_volume == 5
    assert test_component.last_loud == {'text': 'test 1 2 3', 'volume': 5}


def test_invoke():
    test_component = TestTurtleTool()
    with pytest.raises(Exception):
        test_component.invoke()


def test_unregistered_turtle():
    test_component = TestTurtleTool()
    with pytest.raises(UnregisteredTurtleEquipment):
        _state = test_component.state

