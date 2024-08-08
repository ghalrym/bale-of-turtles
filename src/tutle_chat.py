from dotenv import load_dotenv

from mini_turtle.mini_turtle import MiniTurtle
from mini_turtle.components import MiniTortoiseTTSComponent, GitLlamaComponent

load_dotenv()


class TurtleChat(MiniTurtle):
    def __init__(self):
        super().__init__(
            MiniTortoiseTTSComponent("mini-turtle"),
            GitLlamaComponent(),
        )

    def input(self, text: str | None = None, **kwargs):
        self.state.update_state(mini_tortoise_tts_say=text)
        self.state.trigger("git-write-commit-message")


if __name__ == '__main__':
    turtle_chat = TurtleChat()
    turtle_chat.state_help()
    turtle_chat.input("Hello MR. Turtle")
