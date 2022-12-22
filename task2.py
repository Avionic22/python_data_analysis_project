import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv('/Users/nataliiayevtushyna/Downloads/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
#converting tenth celcium to celcium
df['Data_Value'] = df['Data_Value'].apply(lambda x: x/10)

#converting date to date timestamp
df['Date'] = pd.DatetimeIndex(df['Date']).date
lis = ['2922008','2922012'] #list of 29 Febs appearing in each leap year
dates = [datetime.datetime.strptime(i, '%d%m%Y').date() for i in lis] #converting into list of datetime.date objects
df = df[~df['Date'].isin(dates)] #remove all 29 February dates

#creating a separate column for the month
df['Month'] = pd.DatetimeIndex(df['Date']).month
#we are colleting dates between 2005 - 2014, so want to remove any data from dates after 31 Dec 2014
#creating datetime.date format of cutoff date
a= '31122014'

#converting a string into datetime.date object
cutoff_date = datetime.datetime.strptime(a,'%d%m%Y').date()

#dataframe for values before cutoff date
df2 = df[df['Date'] <= cutoff_date]

#returning dates after cutoff date
df3 = df[df['Date'] > cutoff_date]

#creating two separate data frames for min and max values after cutoff date
df3_max = df3[df3['Element'] == 'TMAX']
df3_min = df3[df3['Element'] == 'TMIN']

#creating two separate data frames for min, max values and group by month
df_min = df2[df2['Element'] =='TMIN'].groupby('Month').aggregate({'Data_Value':np.min})
df_max = df2[df2['Element'] == 'TMAX'].groupby('Month').aggregate({'Data_Value':np.max})

#create bare figure for the next drawings
plt.figure 

#filling space between max and min values
plt.gca().fill_between(df_min.index.values,
                       df_min['Data_Value'], df_max['Data_Value'],
                       facecolor='blue',
                       alpha=0.25)
#plot linear graph for min and max values before cutoff date
plt.plot(df_max,'-o', df_min, '-o', markersize = 2)
plt.legend(['Max temprature', 'Min temperature'])
df3_max = pd.merge(df3_max, df_max, on = 'Month')
df3_max = df3_max.groupby('Month').aggregate({'Data_Value_x': np.max, 'Data_Value_y': np.max})
df3_min = pd.merge(df3_min, df_min, on = 'Month')
df3_min = df3_min.groupby('Month').aggregate({'Data_Value_x': np.min, 'Data_Value_y': np.min})
#find record high and low values after 2015 comparing before 2015
df3_min = df3_min[df3_min['Data_Value_x'] < df3_min['Data_Value_y']]
df3_max = df3_max[df3_max['Data_Value_x'] > df3_max['Data_Value_y']]
plt.scatter(df3_max.index.values, df3_max['Data_Value_x'], s=3, c='red', label = 'Temperatures above max') #values over max
plt.scatter(df3_min.index.values, df3_min['Data_Value_x'], s=3, c='black', label = 'Temperatures below min') #values under min
plt.legend()

#dejunking the plot
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
plt.xticks(list(df_max.index), months)
plt.title('Min and Max temperatures in Ann Arbor Michigan United States between 2005-2015')
plt.xlabel('Years', fontsize=20)
plt.ylabel('Temperatures', fontsize=20)

plt.show()
