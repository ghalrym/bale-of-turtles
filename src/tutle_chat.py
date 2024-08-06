from dotenv import load_dotenv

from mini_turtle.mini_turtle import MiniTurtle
from mini_turtle.components import MiniTortoiseTTS

load_dotenv()


class TurtleChat(MiniTurtle):
    def __init__(self):
        super().__init__(
            MiniTortoiseTTS("mini-turtle"),
        )

    def input(self, text: str, *args, **kwargs):
        self._state.update_state(mini_tortoise_tts_say=text)


if __name__ == '__main__':
    turtle_chat = TurtleChat()
    turtle_chat.input("Hello MR. Turtle")
