import pandas as pd

def remove_quoted_comments(text):
    """
    Remove quoted comments in replies
    """
    lines = text.splitlines()
    useful_lines = [line for line in lines if not line.strip().startswith('>')]

    return "\n".join(useful_lines).strip()

def process_comment(comment_list, issue_id, issue_creator, issue_assignees):
    """
    Processes each comment to be more readable
    """
    comments = []
    comment_thread = ''

    for comment in comment_list:
        if comment.user.login == 'google-ml-butler[bot]': # only comments feedback URLs, skip
            continue
        
        # Add possibly helpful role of authors in the thread
        author = comment.user.login
        if author == issue_creator:
            author += " (Issue Creator)"

        elif author in issue_assignees:
            author += " (Assginee)"

        date = comment.created_at.strftime("%Y-%m-%d %H:%M:%S %Z")
        # convert instances of'> {prev_comment} \n {current comment}' to '{current comment}'
        body = remove_quoted_comments(comment.body) 

        comment_thread += f'{author} on ({date}): {body}' +'\n\n'
        comments.append(
            {
                'comment_id':comment.id, 
                "issue_id":issue_id, 
                "author":comment.user.login,
                "body":comment.body.strip(),
                "created_at":comment.created_at
                })
    return comments, comment_thread

def fetch_issue(issue):
    """
    Processes data for a single issue and returns it in a dictionary
    """
    if issue.pull_request:
        return None
    
    assignee_list = [user.login for user in issue.assignees]
    comments, comment_thread = process_comment(issue.get_comments(), issue.id, issue.user.login, assignee_list)
    labels = issue.labels
    
    return  {
            "id": issue.id,
            "type": "issue",
            "title": issue.title,
            "author": issue.user.login,
            # "assignees":issue.assignees,
            "created_at": issue.created_at,
            "closed_at": issue.closed_at,
            "url": issue.html_url,
            "labels": [(label.name, label.description) for label in labels],
            "comments_list": comments,
            "comment_thread":comment_thread
        }

def scrape_issues(repo, num=100, state='closed'):
    """
    Scrapes closed Issues from the given repository and returns data in a DataFrame
    """
    
    issues = []
    for issue in repo.get_issues(state=state)[:num]:
        result = fetch_issue(issue)
        if result:
            issues.append(result)

    df = pd.DataFrame(issues)
    return df