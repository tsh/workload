import requests, json, getpass
"""
https://api.github.com/repos/dgladkov/noseyboy/commits
"""

github_url = "https://api.github.com/repos/dgladkov/noseyboy/commits"


if __name__ == '__main__':
    usr = input('Username: ')
    pwd = getpass.getpass()
    r = requests.get(github_url, auth=(usr, pwd))
    print (r.json()[0])