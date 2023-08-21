import json
import requests
from decouple import config


def get_github_commits(request_url):
    # add get url path
    url = request_url

    # init payload
    payload = {}

    # init headers
    headers = {'Authorization': config('GITHUB_AUTHORIZATION')}

    # get response
    response = requests.request("GET", url, headers=headers, data=payload)

    get_dict = json.loads(response.text)

    sha = get_dict[0]['sha']
    last_commit_time = get_dict[0]['commit']['author']['date']
    

    return {'sha': sha, 'last_commit_time': last_commit_time}
