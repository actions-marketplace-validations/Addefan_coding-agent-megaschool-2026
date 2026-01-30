from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools.file import FileTools
from agno.tools.github import GithubTools
from agno.tools.reasoning import ReasoningTools

from code.tools import LocalGitTools
from code.utils import get_pr_branch_name
from settings import settings

ISSUE_SYSTEM_PROMPT = """
You are a Senior Developer starting a NEW task.
Your goal is to implement the requirements from Issue #{issue_id} in repository {repository}.

STRICT WORKFLOW:
1. Use `get_issue` to read Issue #{issue_id}.
2. Use `create_new_branch` to create a branch named 'feature/issue-{issue_id}'.
3. Analyze the codebase using `list_files`, `search_files`, `read_file` and `read_file_chunk`.
4. Write the code using `save_file`, `delete_file` and `replace_file_chunk`.
5. Commit changes using `commit_changes` with a descriptive message using Conventional Commits.
6. Push changes using `push_changes`.
7. Create a Pull Request using `create_pull_request` to submit your work.
"""

PR_SYSTEM_PROMPT = """
You are a Senior Developer fixing bugs in an EXISTING Pull Request #{pr_id}.
The Reviewer has requested changes.

TARGET BRANCH: '{current_branch}' in repository {repository}.

STRICT WORKFLOW:
1. Use `create_new_branch` (it checkout if branch already exist) to switch to '{current_branch}'.
   DO NOT create a new random branch name.
2. Use `get_pull_request_with_details` to read the PR comments or `get_issue` to read Issue description to 
understand what is wrong.
3. Fix the code using `save_file`, `delete_file` and `replace_file_chunk`.
4. Commit changes using `commit_changes` with a descriptive message using Conventional Commits.
5. Push changes using `push_changes`.

CRITICAL RULES:
- DO NOT create a new Pull Request. The existing one will update automatically after push.
- DO NOT merge the branch yourself.
"""


def get_system_prompt(issue_id=None, pr_id=None):
    if issue_id is not None:
        return ISSUE_SYSTEM_PROMPT.format(issue_id=issue_id, repository=settings.github.repository)
    elif pr_id is not None:
        current_branch = get_pr_branch_name(repo_name=settings.github.repository, pr_number=pr_id)
        return PR_SYSTEM_PROMPT.format(pr_id=pr_id, current_branch=current_branch,
                                       repository=settings.github.repository)
    else:
        return "You are a coding assistant. Help with code-related tasks."


def get_agent(issue_id=None, pr_id=None):
    return Agent(
        model=OpenAILike(
            id=settings.model.id,
            base_url=settings.model.base_url,
            api_key=settings.model.api_key,
        ),
        tools=[
            ReasoningTools(),
            FileTools(base_dir=settings.github.workspace, enable_delete_file=True),
            GithubTools(
                access_token=settings.github.token,
                include_tools=("get_issue", "create_pull_request", "get_pull_request_with_details"),
            ),
            LocalGitTools(base_dir=settings.github.workspace),
        ],
        instructions=get_system_prompt(issue_id=issue_id, pr_id=pr_id),
        markdown=True,
    )


if __name__ == "__main__":
    agent = get_agent(pr_id=3)
    user_prompt = input("Enter your query: ")
    agent.print_response(user_prompt, stream=True)
