from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.reasoning import ReasoningTools
from agno.tools.file import FileTools
from agno.tools.github import GithubTools


from settings import settings


def get_agent():
    return Agent(
        model=OpenRouter(
            id=settings.openrouter.model,
            base_url=settings.openrouter.base_url,
            api_key=settings.openrouter.api_key,
        ),
        tools=[
            ReasoningTools(),
            FileTools(),  # TODO: probably add enable_delete_file=True
            GithubTools(
                access_token=settings.github.token,
                include_tools=("get_issue", "create_pull_request"),
            ),
        ],
        markdown=True,
    )


if __name__ == "__main__":
    agent = get_agent()
    user_prompt = input("Enter your query: ")
    agent.print_response(user_prompt, stream=True)
