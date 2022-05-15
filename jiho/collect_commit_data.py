import click
import pandas as pd
import github
from github import Github
import sys

URL = "https://api.github.com/users/"


class GitHubAPIShell:
    """ GitHub API 객체

    - pygithub 라이브러리 사용
    - token 이 필요!! : 만약 token 과 함께 Github 객체 호출 시 id or IP 당 1시간에 60번 밖에 호출을 못함
    """

    def __init__(self, argv):
        self.github_id = argv  # argv : GitHug ID
        self.user = None  # GitHub user 객체 담기 위함
        self.data = pd.DataFrame(columns=["repo", "commit"])

    def run(self):
        g = Github(login_or_token="<token!!>")
        self.user = g.get_user(self.github_id)

        self.get_repo_info()
        self.data.to_csv('data.csv', index=False)

        return 0

    def get_repo_info(self):
        """
        모든 commit message
        """
        repos = self.user.get_repos()

        for repo in repos[:5]:
            self.get_commits(repo)

    def get_commits(self, repo):
        """
        커밋 메시지

        :param repo: Repository Object
        """

        try:
            repo_name = repo.full_name
            for commit in repo.get_commits():
                commit_message = " ".join(commit.commit.message.split())
                self.data.loc[len(self.data)] = [repo_name, commit_message]
        except github.GithubException as e:
            print(repo.full_name, e)


@click.command()
@click.option("--id", '-i', help="Enter the GitHub ID in str format", required=True)  # github id
def main(id=None):
    if id is None:
        return 0

    return GitHubAPIShell(id).run()


if __name__ == '__main__':
    sys.exit(main())
