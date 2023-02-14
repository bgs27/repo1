import json
import os
import requests
import time
import pandas as pd
redirect_uri = 'http://localhost/'
client_id = '22864'
client_secret = '2ae4279599c727b35fc2feea45d7c9a2be775692'
refresh_token = 'f6bb0677659c60214c3e1dce7f52f391e3e6e89e'

def get_token(client_id, client_secret, refresh_token):
    response = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                                data={'client_id': client_id,
                                    'client_secret': client_secret,
                                    'grant_type': 'refresh_token',
                                    'refresh_token': refresh_token})
    new_strava_tokens = response.json()
    # Save new tokens to file
    with open('strava_tokens.json', 'w') as outfile:
      json.dump(new_strava_tokens, outfile)
    return(new_strava_tokens)

def get_user_info(new_strava_tokens):
   access_token = new_strava_tokens['access_token']
   athlete_url = f"https://www.strava.com/api/v3/athlete?" \
          f"access_token={access_token}"
   response = requests.get(athlete_url)
   athlete = response.json()
   return athlete

def get_starred_segs(new_strava_tokens):
   access_token = new_strava_tokens['access_token']
   segments_url = f"https://www.strava.com/api/v3/segments/starred?" \
          f"access_token={access_token}"
   response = requests.get(segments_url)
   segments = response.json()
   return segments

def get_name_id(starred):
   id_dict = {}
   for item in starred:
      id = item['id']
      name = item['name']
      id_dict[id] = name
   return id_dict 


# MAIN CODE
new_strava_tokens = get_token(client_id, client_secret, refresh_token)
athlete = get_user_info(new_strava_tokens)
starred = get_starred_segs(new_strava_tokens)
names = get_name_id(starred)
print(names)
