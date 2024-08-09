from collections import defaultdict

from bale_of_turtles import AgentTurtle, use_state
from .test_turtle_llm import TestTurtleLLM
from .test_turtle_tool import TestTurtleTool


class TestAgentTurtle(AgentTurtle):

    def __init__(self):
        super().__init__(TestTurtleLLM(), TestTurtleTool(), lead_turtle=True)

    @use_state("top-turtle", ["turtle_text"])
    def top_turtle(self, turtle_text: str | None = None, **kwargs): ...


def test_turtle_agent_init():
    test_turtle = TestAgentTurtle()
    assert len(test_turtle.turtle_tools) == 2


def test_turtle_agent_state():
    test_turtle = TestAgentTurtle()
    assert test_turtle.state._trigger_queue == []
    assert list(test_turtle.state._trigger_key_to_functions.keys()) == [
        "top-turtle",
        "llm-turtle",
        "turtle-tool",
    ]
    assert test_turtle.state._state == defaultdict(lambda: None, {})
    assert test_turtle.state._state_to_trigger_key == defaultdict(
        list, {"turtle_text": ["top-turtle", "llm-turtle"], "volume": ["turtle-tool"]}
    )


def test_world_input():
    test_turtle = TestAgentTurtle()
    test_turtle.invoke(turtle_test="hello world")
