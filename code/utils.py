from github import Github, Auth

from settings import settings


def get_pr_branch_name(repo_name: str, pr_number: int) -> str:
    github = Github(auth=Auth.Token(settings.github.token))
    repo = github.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    return pr.head.ref


if __name__ == "__main__":
    repo_name = "Addefan/megaschool-test-v1"
    pr_number = 2
    branch_name = get_pr_branch_name(repo_name, pr_number)
    print(f"PR #{pr_number} branch name: {branch_name}")
