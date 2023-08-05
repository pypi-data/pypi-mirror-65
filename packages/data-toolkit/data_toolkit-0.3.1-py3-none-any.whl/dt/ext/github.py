# pip install github3.py
import github3
import pandas as pd
import sys

def init():
    sys.path.append('/Users/jakub/remote_code')
    from github_auth import gh_username, gh_password
    return gh_username, gh_password

def find_forks(repo_url: str):
    gh_username, gh_password = init()

    user, repo = repo_url.split('/')[-2:]

    g = github3.login(gh_username, gh_password)
    r = g.repository(user, repo)
    total_list = list(r.forks(sort='commits', number=r.fork_count))
    data = [ (i,i.updated_at, 
            i.pushed_at, i.updated_at == i.created_at) for i in total_list ]
    df = pd.DataFrame(data,columns=['name','updated_at','pushed_at','ever_changed'])
    df = df.sort_values('ever_changed')
    print(df.ever_changed.value_counts())
    return df
