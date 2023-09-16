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
    node_id = get_dict[0]['node_id']

    return {'sha': sha, 'node_id': node_id}
