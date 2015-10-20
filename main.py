import requests, json, getpass

intresting_events = ['PushEvent', 'IssuesEvent']
#TODO: filter by repositores only private?
#TODO: print date/time

template = """
Name:       {author}
Url:        {url}
Message:    {message}
Date:       {date}: {time}
   """

def parse_push_event(event):
    print_params = {'author': event['actor']['login'],  #TODO: use loop to parse commit
                    'url': event['payload']['commits'][0]['url'], #TODO: use sha to construct web based commit
                    'message': event['payload']['commits'][0]['message']}
    return print_params

def parse_issue_event(event):
    # TODO: me
    pass

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
