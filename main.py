import requests, json, getpass, dateutil.parser

intresting_events = ['PushEvent', 'IssuesEvent']

template = """
Name:       {author}
Url:        {url}
Date:       {date}: {time}
Message:    {message}
   """

def parse_push_event(event):
    date_time = dateutil.parser.parse(event['created_at'])
    print_params = {'author': event['actor']['login'],  #TODO: use loop to parse commit
                    'url': event['payload']['commits'][0]['url'], #TODO: use sha to construct web based commit
                    'message': event['payload']['commits'][0]['message'],
                    'date': date_time.date(),
                    'time': date_time.time()}
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
    filtered_type_events = filter(lambda d: d['type'] in intresting_events, events)
    filtered_visibility_events = filter(lambda d: d['public'] is False, filtered_type_events)
    for event in filtered_visibility_events:
        if event['type'] == 'PushEvent':
            print(event)
            print(template.format(**parse_push_event(event)))
