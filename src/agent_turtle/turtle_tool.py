from pydantic import BaseModel


class TurtleTool:
    """TurtleTool are tools that manage the state for the llm. you can grant the llm
    access to call the function with `grant_access` and `expect_context`"""

    def __init__(
        self,
        grant_access: bool = False,
        expect_context: BaseModel | None = None,
    ):
        self._grant_access = grant_access
        self._expect_context = expect_context
