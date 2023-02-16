import json
from datetime import date
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
data['start_date'] = pd.to_datetime(data['start_date'])
data['start_date'] = data['start_date'].dt.date
data['average_speed'] = (data['average_speed']*3.6)
data['max_speed'] = (data['max_speed']*3.6)

rides_w_power = data.loc[data['device_watts'] == True]


rides_w_power.info()

'''
fig = plt.figure() #create overall container
ax1 = fig.add_subplot(111) #add a 1 by 1 plot to the figure
x = np.asarray(rides_w_power['start_date'])  #convert data to numpy array
y = np.asarray(rides_w_power['weighted_average_watts'])


ax1.plot_date(x, y) #plot data points in scatter plot on ax1
ax1.set_title('Average Watts over Time')

#format the figure and display
fig.autofmt_xdate(rotation=45)
fig.tight_layout()
plt.show()
'''
