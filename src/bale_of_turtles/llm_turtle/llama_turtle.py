from langchain_community.chat_models import ChatOllama
from langchain_core.messages import BaseMessage

from bale_of_turtles._turtle_state import use_state
from bale_of_turtles.llm_turtle.llm_turtle import LlmTurtle


class LlamaTurtle(LlmTurtle):
    __slots__ = ("_model",)

    def __init__(self, name: str):
        super().__init__(name)
        self._model = ChatOllama(model=name)

    @use_state("llm-message", ["turtle_human_message"])
    def invoke(
        self,
        turtle_human_message: BaseMessage | None = None,
        turtle_llm_message_history: list[BaseMessage] | None = None,
        *args,
        **kwargs,
    ):
        if not turtle_human_message:
            return
        response = self._model.invoke(turtle_llm_message_history)
        self.update_state(turtle_ai_message=response)
