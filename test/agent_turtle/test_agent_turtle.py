from collections import defaultdict

import pytest

from agent_turtle import AgentTurtle, use_state
from .test_turtle_tool import TestTurtleTool
from .test_turtle_llm import TestTurtleLLM


class TestAgentTurtle(AgentTurtle):

    def __init__(self):
        super().__init__(
            TestTurtleLLM(),
            TestTurtleTool(),
            lead_turtle=True
        )

    @use_state("top-turtle", ["turtle_text"])
    def top_turtle(self, turtle_text: str | None = None, **kwargs):
        ...


def test_turtle_agent_init():
    test_turtle = TestAgentTurtle()
    assert test_turtle._llm.name == TestTurtleLLM().name
    assert len(test_turtle.turtle_tools) == 1


def test_turtle_agent_state():
    test_turtle = TestAgentTurtle()
    assert test_turtle.state._trigger_queue == []
    assert set(test_turtle.state._trigger_key_to_functions.keys()) == {"test-turtle", "top-turtle"}
    assert test_turtle.state._state == defaultdict(lambda: None, {})
    assert test_turtle.state._state_to_trigger_key == {"turtle_text": {'top-turtle'}}


def test_invoke():
    test_turtle = TestAgentTurtle()
    with pytest.raises(Exception):
        test_turtle.invoke()
        test_turtle()


def test_world_input():
    test_turtle = TestAgentTurtle()
    test_turtle.world_input(turtle_test="hello world")
