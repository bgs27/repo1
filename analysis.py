import json
from datetime import date
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Functions
def save_data_to_json(activities, file_name):
    with open(file_name, "w") as f:
        json.dump(activities, f, indent=4)

def read_data_from_json(file_name):
   with open(file_name, 'r') as f:
      activities = json.load(f)
   return activities

def correct_date_time(data):
    data['start_date'] = pd.to_datetime(data['start_date'])
    data['start_date'] = data['start_date'].dt.date
    data['moving_time'] = pd.to_timedelta(data['moving_time'], unit='s')
    return data
    
def correct_speed_distance(data):
    data['average_speed'] = (data['average_speed']*3.6)
    data['max_speed'] = (data['max_speed']*3.6)
    data['distance'] = (data['distance']/1000)
    return data
    

# MAIN CODE
'''
access_token = get_token(client_id, client_secret, refresh_token)
extract_strava_activities(access_token)
'''
# Opening json file and reading data 
file_name = 'strava_data.json'
data = read_data_from_json(file_name)
data = pd.json_normalize(data)

# Manipulating data 
cols = ['resource_state', 'name', 'distance', 'moving_time', 'total_elevation_gain', 'type', 'sport_type', 'workout_type', 'id',
       'start_date', 'trainer', 'average_speed', 'max_speed', 'average_cadence', 'average_temp', 'average_watts',
       'max_watts', 'weighted_average_watts', 'device_watts', 'upload_id']
data = data[cols]

data = correct_date_time(data)
data = correct_speed_distance(data)



rides_w_power = data.loc[data['device_watts'] == True]


pp_df = rides_w_power[['distance', 'average_speed', 'weighted_average_watts', 'total_elevation_gain']]
sns.pairplot(pp_df)

print(rides_w_power.describe().round(0))

''''
fig = plt.figure() #create overall container
ax1 = fig.add_subplot(111) #add a 1 by 1 plot to the figure
x = np.asarray(rides_w_power['distance'])  #convert data to numpy array
y = np.asarray(rides_w_power['weighted_average_watts'])


ax1.plot(x, y) #plot data points in scatter plot on ax1
ax1.set_title('Average Watts over Time')

#format the figure and display
fig.tight_layout()
plt.show()
'''