import requests
import os
import argparse

# Set these variables with appropriate values
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # Personal Access Token
# REPO_OWNER = os.getenv('GITHUB_REPOSITORY_OWNER')  # Repository owner
# REPO_NAME = os.getenv('GITHUB_REPOSITORY').split('/')[1]  # Repository name
#GITHUB_TOKEN = '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'


def get_running_workflows(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs?status=in_progress"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["workflow_runs"]

def cancel_workflow(run_id, repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs/{run_id}/cancel"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    print(f"Cancelled workflow: {run_id}")

def main(repo_owner='compasslabs', repo_name='dojo'):
    parser = argparse.ArgumentParser(description='Cancel all running GitHub workflows.')
    parser.add_argument('repo_owner', type=str, help='The owner of the repository.')
    parser.add_argument('repo_name', type=str, help='The name of the repository.')
    args = parser.parse_args()

    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    workflows = get_running_workflows(args.repo_owner, args.repo_name)
    for workflow in workflows:
        cancel_workflow(workflow["id"],args.repo_owner, args.repo_name)

if __name__ == "__main__":
    main()
