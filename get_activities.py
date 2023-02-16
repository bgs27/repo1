import json
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Constants
redirect_uri = 'http://localhost/'
client_id = '22864'
client_secret = '2ae4279599c727b35fc2feea45d7c9a2be775692'
refresh_token = '7708c2376e5516b7ede03ecb2c5dc39519392159'

# Functions 
def get_token(client_id, client_secret, refresh_token):
    response = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                                data={'client_id': client_id,
                                    'client_secret': client_secret,
                                    'grant_type': 'refresh_token',
                                    'refresh_token': refresh_token})
    new_strava_tokens = response.json()
    access_token = new_strava_tokens['access_token']
    return(access_token)

def get_user_info(new_strava_tokens):
   access_token = new_strava_tokens['access_token']
   athlete_url = f"https://www.strava.com/api/v3/athlete?" \
          f"access_token={access_token}"
   response = requests.get(athlete_url)
   athlete = response.json()
   return athlete

def get_starred_segs(access_token):
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

def extract_strava_activities(access_token, file_name, num_of_pages):
   activites_url = "https://www.strava.com/api/v3/athlete/activities"
   header = {'Authorization': 'Bearer ' + access_token}
   page = 1
   param = {'per_page': 200, 'page': page}
   data = requests.get(activites_url, headers=header, params=param).json()
   save_data_to_json(data, file_name)
   page +=1
   for i in range(num_of_pages):
      param = {'per_page': 200, 'page': page}
      data = requests.get(activites_url, headers=header, params=param).json()
      activities = read_data_from_json(file_name)
      data = data + activities
      save_data_to_json(data, file_name)
      page +=1

def save_data_to_json(activities, file_name):
    with open(file_name, "w") as f:
        json.dump(activities, f, indent=4)

def read_data_from_json(file_name):
    with open(file_name, 'r') as f:
        activities = json.load(f)
    return activities

# MAIN CODE
file_name = 'test.json'
num_of_pages = 2
access_token = get_token(client_id, client_secret, refresh_token)
extract_strava_activities(access_token, file_name, num_of_pages)
 
