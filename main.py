import praw
import time
import json
from datetime import date, datetime, timedelta
import requests
from episode import Episode
from tvdb import tvdb_login
import tvdb_globals
import reddit_globals
from reddit import post_to_reddit

if __name__ == "__main__":
    episode_list = tvdb_login()
    post_to_reddit(episode_list)

