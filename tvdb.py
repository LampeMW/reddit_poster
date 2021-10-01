import tvdb_globals
from episode import Episode
import requests

def tvdb_login():
    url = "https://api.thetvdb.com/login"

    payload = """{"apikey": "%s", "userkey": "%s", "username": "%s"}""" % (tvdb_globals.tvdb_api_key, tvdb_globals.tvdb_user_key, tvdb_globals.tvdb_user_name)
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }

    r = requests.post(url, headers=headers, data = payload)
    token = r.json()["token"]

    headers = {'Authorization': "Bearer %s" % token,
        'Accept': 'application/vnd.thetvdb.v3.0.0'
    }
    url = "https://api.thetvdb.com/series/%s/episodes" % tvdb_globals.tvdb_episode_id
    r = requests.get(url, headers=headers)
    episode_data = r.json()['data']

    if 'next' in r.json()['links']:
        while r.json()['links']['next'] != None:
            next_url = "https://api.thetvdb.com/series/%s/episodes?page=%s"  % (tvdb_globals.tvdb_episode_id, r.json()['links']['next'])
            r = requests.get(next_url, headers=headers)
            episode_data.extend(r.json()['data'])

    episode_list = []

    for episode in episode_data:
        ep = Episode(episode)
        episode_list.append(ep)

    return episode_list