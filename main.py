import requests, json, getpass, dateutil.parser

intresting_events = ['PushEvent', 'IssuesEvent']

simple_commit_template = """
Name:       {author}
Url:        {url}
Date:       {date}: {time}
Message:    {message}
   """

close_issue_template = """
Close Issue
Url:        {url}
"""


def parse_push_event(event):
    date_time = dateutil.parser.parse(event['created_at'])
    print_params = {
        'author': event['actor']['login'],  # TODO: use loop to parse commit
        'url': event['payload']['commits'][0]['url'],  #TODO: use sha to construct web based commit
        'message': event['payload']['commits'][0]['message'],
        'date': date_time.date(),
        'time': date_time.time()
    }
    return print_params


def parse_issue_event(event):
    # TODO: check only closed issues
    print_params = {
        'url': event['payload']['issue']['html_url']
    }
    return print_params


github_url = "https://api.github.com/users/{user}/events"

if __name__ == '__main__':
    print(parse_issue_event({'repo': {'id': 41418916, 'name': 'dgladkov/noseyboy', 'url': 'https://api.github.com/repos/dgladkov/noseyboy'}, 'id': '3255838000', 'type': 'IssuesEvent', 'payload': {'action': 'closed', 'issue': {'comments_url': 'https://api.github.com/repos/dgladkov/noseyboy/issues/1/comments', 'comments': 0, 'updated_at': '2015-10-20T10:44:01Z', 'url': 'https://api.github.com/repos/dgladkov/noseyboy/issues/1', 'body': 'describe each action for each url', 'number': 1, 'created_at': '2015-10-16T08:45:06Z', 'title': 'add basic discription for rest api', 'id': 111788528, 'events_url': 'https://api.github.com/repos/dgladkov/noseyboy/issues/1/events', 'user': {'received_events_url': 'https://api.github.com/users/Deadlysmile/received_events', 'organizations_url': 'https://api.github.com/users/Deadlysmile/orgs', 'type': 'User', 'gravatar_id': '', 'url': 'https://api.github.com/users/Deadlysmile', 'following_url': 'https://api.github.com/users/Deadlysmile/following{/other_user}', 'avatar_url': 'https://avatars.githubusercontent.com/u/6708097?v=3', 'subscriptions_url': 'https://api.github.com/users/Deadlysmile/subscriptions', 'site_admin': False, 'login': 'Deadlysmile', 'repos_url': 'https://api.github.com/users/Deadlysmile/repos', 'id': 6708097, 'events_url': 'https://api.github.com/users/Deadlysmile/events{/privacy}', 'html_url': 'https://github.com/Deadlysmile', 'gists_url': 'https://api.github.com/users/Deadlysmile/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/Deadlysmile/starred{/owner}{/repo}', 'followers_url': 'https://api.github.com/users/Deadlysmile/followers'}, 'assignee': {'received_events_url': 'https://api.github.com/users/tsh/received_events', 'organizations_url': 'https://api.github.com/users/tsh/orgs', 'type': 'User', 'gravatar_id': '', 'url': 'https://api.github.com/users/tsh', 'following_url': 'https://api.github.com/users/tsh/following{/other_user}', 'avatar_url': 'https://avatars.githubusercontent.com/u/5930723?v=3', 'subscriptions_url': 'https://api.github.com/users/tsh/subscriptions', 'site_admin': False, 'login': 'tsh', 'repos_url': 'https://api.github.com/users/tsh/repos', 'id': 5930723, 'events_url': 'https://api.github.com/users/tsh/events{/privacy}', 'html_url': 'https://github.com/tsh', 'gists_url': 'https://api.github.com/users/tsh/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/tsh/starred{/owner}{/repo}', 'followers_url': 'https://api.github.com/users/tsh/followers'}, 'closed_at': '2015-10-20T10:44:01Z', 'html_url': 'https://github.com/dgladkov/noseyboy/issues/1', 'state': 'closed', 'labels_url': 'https://api.github.com/repos/dgladkov/noseyboy/issues/1/labels{/name}', 'milestone': None, 'locked': False, 'labels': []}}, 'created_at': '2015-10-20T10:44:01Z', 'public': False, 'actor': {'id': 5930723, 'avatar_url': 'https://avatars.githubusercontent.com/u/5930723?', 'url': 'https://api.github.com/users/tsh', 'gravatar_id': '', 'login': 'tsh'
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                }}
    ))
    # usr = input('Username: ')
    # pwd = getpass.getpass()
    # req = requests.get(github_url.format(user=usr), auth=(usr, pwd))
    # events = req.json()
    # filtered_type_events = filter(lambda d: d['type'] in intresting_events, events)
    # filtered_visibility_events = filter(lambda d: d['public'] is False, filtered_type_events)
    # for event in filtered_visibility_events:
    #     if event['type'] == 'PushEvent':
    #         print(simple_commit_template.format(**parse_push_event(event)))
    #     elif event['type'] == 'IssuesEvent':
    #         print(event)
    #         print(close_issue_template.format(**parse_issue_event({'repo': {'id': 41418916, 'name': 'dgladkov/noseyboy', 'url': 'https://api.github.com/repos/dgladkov/noseyboy'}, 'id': '3255838000', 'type': 'IssuesEvent', 'payload': {'action': 'closed', 'issue': {'comments_url': 'https://api.github.com/repos/dgladkov/noseyboy/issues/1/comments', 'comments': 0, 'updated_at': '2015-10-20T10:44:01Z', 'url': 'https://api.github.com/repos/dgladkov/noseyboy/issues/1', 'body': 'describe each action for each url', 'number': 1, 'created_at': '2015-10-16T08:45:06Z', 'title': 'add basic discription for rest api', 'id': 111788528, 'events_url': 'https://api.github.com/repos/dgladkov/noseyboy/issues/1/events', 'user': {'received_events_url': 'https://api.github.com/users/Deadlysmile/received_events', 'organizations_url': 'https://api.github.com/users/Deadlysmile/orgs', 'type': 'User', 'gravatar_id': '', 'url': 'https://api.github.com/users/Deadlysmile', 'following_url': 'https://api.github.com/users/Deadlysmile/following{/other_user}', 'avatar_url': 'https://avatars.githubusercontent.com/u/6708097?v=3', 'subscriptions_url': 'https://api.github.com/users/Deadlysmile/subscriptions', 'site_admin': False, 'login': 'Deadlysmile', 'repos_url': 'https://api.github.com/users/Deadlysmile/repos', 'id': 6708097, 'events_url': 'https://api.github.com/users/Deadlysmile/events{/privacy}', 'html_url': 'https://github.com/Deadlysmile', 'gists_url': 'https://api.github.com/users/Deadlysmile/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/Deadlysmile/starred{/owner}{/repo}', 'followers_url': 'https://api.github.com/users/Deadlysmile/followers'}, 'assignee': {'received_events_url': 'https://api.github.com/users/tsh/received_events', 'organizations_url': 'https://api.github.com/users/tsh/orgs', 'type': 'User', 'gravatar_id': '', 'url': 'https://api.github.com/users/tsh', 'following_url': 'https://api.github.com/users/tsh/following{/other_user}', 'avatar_url': 'https://avatars.githubusercontent.com/u/5930723?v=3', 'subscriptions_url': 'https://api.github.com/users/tsh/subscriptions', 'site_admin': False, 'login': 'tsh', 'repos_url': 'https://api.github.com/users/tsh/repos', 'id': 5930723, 'events_url': 'https://api.github.com/users/tsh/events{/privacy}', 'html_url': 'https://github.com/tsh', 'gists_url': 'https://api.github.com/users/tsh/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/tsh/starred{/owner}{/repo}', 'followers_url': 'https://api.github.com/users/tsh/followers'}, 'closed_at': '2015-10-20T10:44:01Z', 'html_url': 'https://github.com/dgladkov/noseyboy/issues/1', 'state': 'closed', 'labels_url': 'https://api.github.com/repos/dgladkov/noseyboy/issues/1/labels{/name}', 'milestone': None, 'locked': False, 'labels': []}}, 'created_at': '2015-10-20T10:44:01Z', 'public': False, 'actor': {'id': 5930723, 'avatar_url': 'https://avatars.githubusercontent.com/u/5930723?', 'url': 'https://api.github.com/users/tsh', 'gravatar_id': '', 'login': 'tsh'}})))
