import pytest

from bale_of_turtles import LlmTurtle, use_state


class TestTurtleLLM(LlmTurtle):

    def __init__(self):
        super().__init__("turtle")

    @use_state("llm-turtle", ["turtle_text"])
    def llm_turtle(self, turtle_text: str | None = None, **kwargs): ...

    def invoke(self):
        raise Exception("Expected Exception")


def test_turtle_llm_init():
    llm = TestTurtleLLM()
    assert llm.name == "turtle"


def test_llm_invoke():
    llm = TestTurtleLLM()
    with pytest.raises(Exception):
        llm.invoke()
