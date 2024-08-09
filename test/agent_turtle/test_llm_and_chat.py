from langchain_core.messages import HumanMessage

from bale_of_turtles.agent_turtle import AgentTurtle
from bale_of_turtles.chat_turtle import ChatTurtle
from bale_of_turtles.llm_turtle import LlamaTurtle


class Llama31Chatter(AgentTurtle):

    def __init__(self, *args, **kwargs):
        super().__init__(
            ChatTurtle(),
            LlamaTurtle("llama3.1"),
            *args,
            **kwargs,
        )

    def invoke(self, text: str | None = None, **kwargs):
        human_message = HumanMessage(content=text)
        self.state.update_state(turtle_human_message=human_message)


def test_llm_and_chat():
    llama_chatter = Llama31Chatter(lead_turtle=True)
    llama_chatter.invoke(text="this is a test")
    assert len(llama_chatter.state._state["turtle_llm_message_history"]) == 2
