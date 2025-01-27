import argparse
from github import Auth, Github
from helper.credentials_secret import GITHUB_TOKEN # replace credentials_secret to credentials
from helper.functions import scrape_issues

if __name__ == "__main__":

    # parse arguments 
    parser = argparse.ArgumentParser(prog='github-scrape')
    parser.add_argument('--repo', help='repository to scrape from', default='tensorflow/tensorflow')
    parser.add_argument('--pat', help='your github personal access token', default=GITHUB_TOKEN)
    args = parser.parse_args()

    repo = args.repo
    token = args.pat

    # Authorise token
    auth = Auth.Token(token)
    g = Github(auth=auth)

    repo = g.get_repo('tensorflow/tensorflow')
    print(repo.name)

    # scrape issues
    issues_df = scrape_issues(repo)
    issues_df.to_csv('test.csv', index=False)

    g.close()