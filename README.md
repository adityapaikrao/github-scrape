# github-scrape
Python Script tp scrape Issues &amp; PRs from a github repo using github API via `PyGithub` library. Requires Python 3.x

## Features
1.Fetches closed issues from the TensorFlow repository.

2.Collects comments and comment threads.
Retrieves issue metadata such as title, author, creation date, and closure date.

3.Extracts labels and events associated with each issue.

## Setup

**Install Dependencies**
```
pip install -r requirements.txt
```
**Generate Github Personal Access Token**

copy your github PAT into ```credential_secret.py``` or pass as an argument while running script (see below)

**Running the Script**
```
python scraper.py --repo=<your repository> --pat=<your github PAT>
```