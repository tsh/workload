import requests, json, getpass

intresting_events = ['PushEvent', 'IssuesEvent']
template = """
Name:       {author}
Url:        {url}
Message:    {message}
   """

def parse_push_event(event):
    print_params = {'author': event['actor']['login'],
                    'url': event['payload']['commits'][0]['url'],
                    'message': event['payload']['commits'][0]['message']}
    return print_params

github_url = "https://api.github.com/users/{user}/events"

if __name__ == '__main__':
    usr = input('Username: ')
    pwd = getpass.getpass()
    req = requests.get(github_url.format(user=usr), auth=(usr, pwd))
    events = req.json()
    filtered_events = filter(lambda d: d['type'] in intresting_events, events)
    for event in filtered_events:
        if event['type'] == 'PushEvent':
            print(event)
            print(template.format(**parse_push_event(event)))
