from mini_turtle.components.mini_turtle_component import use_trigger, MiniTurtleComponent
from git_llama.git_llama.git_llama import GitLlama


class GitLlamaComponent(MiniTurtleComponent):

    def __init__(self):
        super().__init__()
        self.git_llama = GitLlama()

    @use_trigger("git-write-commit-message")
    def write_commit(self):
        print(self.git_llama.write_git_commit())

