from langchain.tools import BaseTool


def plan(trip_plan: str):
    return ""


class plan_tool(BaseTool):
    name = "placeholder"
    description = "placeholder"

    def _run(self, query: str) -> str:
        """Use the tool."""
        return plan(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("API does not support async")