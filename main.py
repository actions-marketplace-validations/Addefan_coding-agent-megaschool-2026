import argparse
import sys

from code.agent import get_agent as get_code_agent
from logger import logger
from reviewer.agent import get_agent as get_reviewer_agent


def main():
    parser = argparse.ArgumentParser(description="AI Coding/Reviewer Agent CLI")

    parser.add_argument("--mode", choices=["coder", "reviewer"], required=True, help="Mode of operation")
    parser.add_argument("--issue", type=int, help="Issue number (for Starting Coder)")
    parser.add_argument("--pr", type=int, help="Pull Request number (for Reviewer or Fixing Coder)")

    args = parser.parse_args()

    logger.info(f"Starting AI Agent in {args.mode} mode...")

    if args.mode == "coder":
        if args.issue:
            code_agent = get_code_agent(issue_id=args.issue)
            code_agent.run("Start working according to your instructions.")
        elif args.pr:
            code_agent = get_code_agent(pr_id=args.pr)
            code_agent.run("Start working according to your instructions.")
        else:
            logger.error("--issue or --pr is required for coder mode")
            sys.exit(1)

    elif args.mode == "reviewer":
        if args.pr:
            reviewer_agent = get_reviewer_agent(pr_id=args.pr)
            reviewer_agent.run("Start working according to your instructions.")
        else:
            logger.error("--pr is required for reviewer mode")
            sys.exit(1)


if __name__ == "__main__":
    main()
