from agno.tools import Toolkit
from git import Repo, GitCommandError

from settings import settings


class LocalGitTools(Toolkit):
    def __init__(self, base_dir: str = ".", **kwargs):
        self.base_dir = base_dir
        self.repo = Repo(base_dir)

        tools = [
            self.create_new_branch,
            self.commit_changes,
            self.push_changes,
        ]

        with self.repo.config_writer() as git_config:
            git_config.set_value("user", "email", "code-agent@addefan.ru")
            git_config.set_value("user", "name", "AI Coding Agent")

        super().__init__(name="git", tools=tools, **kwargs)

    def create_new_branch(self, branch_name: str) -> str:
        """
        Creates a new branch from the current HEAD and switches to it.
        Use this before making any code changes when start working with an issue.
        """
        try:
            if branch_name in self.repo.heads:
                self.repo.heads[branch_name].checkout()
                return f"Switched to existing branch: {branch_name}"

            new_branch = self.repo.create_head(branch_name)
            new_branch.checkout()
            return f"Successfully created and switched to branch: {branch_name}"
        except GitCommandError as e:
            return f"Error creating branch: {str(e)}"

    def commit_changes(self, message: str) -> str:
        """
        Stages all modified files (git add .) and commits them.
        Use this after modifying files.
        """
        try:
            if not self.repo.is_dirty(untracked_files=True):
                return "No changes to commit."

            self.repo.git.add(A=True)
            self.repo.index.commit(message)
            return f"Committed changes with message: \"{message}\""
        except GitCommandError as e:
            return f"Error committing: {str(e)}"

    def push_changes(self) -> str:
        """
        Pushes the current branch to origin.
        REQUIRED before creating a Pull Request.
        """
        try:
            branch_name = self.repo.active_branch.name
            origin = self.repo.remote(name="origin")

            token = settings.github.token
            if not token:
                return "Error: GITHUB_TOKEN not found in env."

            remote_url = origin.url
            if "oauth2" not in remote_url and "https://" in remote_url:
                auth_url = remote_url.replace("https://", f"https://oauth2:{token}@")
                origin.set_url(auth_url)

            origin.push(branch_name, set_upstream=True)
            return f"Successfully pushed branch {branch_name} to origin."
        except GitCommandError as e:
            return f"Error pushing: {str(e)}"
