import pytest

from agent_turtle import TurtleLLM


class TestTurtleLLM(TurtleLLM):

    def __init__(self):
        super().__init__("turtle", "test-turtle")

    def invoke(self):
        raise Exception("Expected Exception")


def test_turtle_llm_init():
    llm = TestTurtleLLM()
    assert llm.name == "test-turtle"
    assert llm._model == "turtle"


def test_llm_invoke():
    llm = TestTurtleLLM()
    with pytest.raises(Exception):
        llm.invoke()
        llm()

