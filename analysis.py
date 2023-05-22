import json
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
   data['start_time'] = data['start_date'].dt.time
   data['date'] = data['start_date'].dt.date
   data['month'] = data['start_date'].dt.month_name()
   data['year'] = data['start_date'].dt.year
   data['dayofyear'] = data['start_date'].dt.dayofyear
   data['dayofyear'] = pd.to_numeric(data['dayofyear'])
   data['moving_time'] = pd.to_timedelta(data['moving_time'], unit='s')
   return data
    
def correct_speed_distance(data):
    data['average_speed'] = (data['average_speed']*3.6)
    data['max_speed'] = (data['max_speed']*3.6)
    data['distance'] = (data['distance']/1000)
    return data
    

# MAIN CODE

# Opening json file and reading data 
file_name = 'new_data.json'
data = read_data_from_json(file_name)
data = pd.json_normalize(data)
# Manipulating data 

cols = ['resource_state', 'name', 'distance', 'moving_time', 'total_elevation_gain', 'type', 'sport_type', 'workout_type', 'id',
       'start_date', 'trainer', 'average_speed', 'max_speed', 'average_cadence', 'average_temp', 'average_watts',
       'max_watts', 'weighted_average_watts', 'device_watts', 'upload_id']
data = data[cols]

data = correct_date_time(data)
data = correct_speed_distance(data)

data.to_csv('strava_data.csv', index = False)

startdate = pd.to_datetime("2022-05-01").date()
enddate = pd.to_datetime("2023-06-01").date()

print('total:',len(data))
df = data.drop(data[(data.date > enddate) | (data.date < startdate)].index)
print(len(df))
total = round(df.moving_time.dt.seconds.sum()/3600,2)
print(total)





'''
sns.set(style="whitegrid", font_scale=1)
sns.boxplot(x="year", y="distance", hue="year", data= data)

sns.set_style('white')
sns.barplot(x='month', y='distance', data=data, hue='year', ci=None, estimator=np.sum, palette = 'hot',
           order =["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
plt.legend(loc='upper center')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0)
plt.show()

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