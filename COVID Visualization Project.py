#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
#from datetime import date, timedelta
import numpy as np
import datetime
from datetime import date
import plotly.offline as ofl
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import math
from numpy import nan
#from collections import Counter


# In[2]:


#Data Engineering part: 
#Goal was to create a list with raw csv urls at each index, read every file and store it into the list at its index, 
#and finally add a Date category in each data frame/ data table at each index

#Make a seperate python script to pull everything to your local computer instead of reading the files like this, 
#takes too long
start_date = datetime.date(2020, 4, 12)
end_date = date.today()
delta = datetime.timedelta(days=1)
sorted_data_list = []
i = 0

while start_date < end_date:
    #print('Hi')
    covid_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/"
    covid_url = covid_url + start_date.strftime('%m-%d-%Y') + ".csv" 
    #print(covid_url)
    #pd.read_csv(covid_url)
    sorted_data_list.append(pd.read_csv(covid_url))
    #print('hi')
    sorted_data_list[i]['Date'] = start_date
    #print(sorted_data_list)
    #sorted_data_list[i] = pd.read_csv(covid_url)
    start_date += delta
    i += 1

#print('wrong')
#print(covid_url)
#sorted_data_list[10]


# In[ ]:





# In[3]:


#Goal was to concat all the data frames from each index into one data frame, stored in the data_table variable 
#Also to reset the indecies and update them to the propper one


data_table =  pd.concat(sorted_data_list)
data_table = data_table.reset_index()
data_table.pop('index')


# In[4]:


MA_indexes = []
MA_indexes = data_table[data_table['Province_State']== 'Massachusetts'].index.values
#print(MA_indexes)
FL_indexes =[]
FL_indexes = data_table[data_table['Province_State'] == 'Florida'].index.values

#len(MA_indexes)
len(FL_indexes)


# In[5]:


#Data Visualizaton Plan:
# I want to only use the Massachusetts rows and create a line graph on the cases confirmed, recovered, and deaths vs dates  

start_date = datetime.date(2020, 4, 12)
end_date = date.today()
delta = datetime.timedelta(days=1)
x = []
while start_date < end_date:
    x.append(start_date) 
    start_date += delta
#print(len(x))
#print(x[476])
i = 0
y_1 = []
y_2 = []
y_3 = []
y_4 =[]
y_MA =[]
y_FL =[]

#print(len(data_table))
while i < len(x):            
    y_1.append(data_table['Confirmed'][MA_indexes[i]])
    y_2.append(data_table['Deaths'][MA_indexes[i]])
    y_3.append(data_table['Confirmed'][FL_indexes[i]])
    y_4.append(data_table['Deaths'][FL_indexes[i]])
    y_MA.append(data_table['Total_Test_Results'][MA_indexes[i]])
    y_FL.append(data_table['Total_Test_Results'][FL_indexes[i]])
    i += 1

trace1 = go.Scatter(x=x, y=y_1, mode='lines', name='MA Confirmed Cases')
    
trace2 = go.Scatter(x = x, y = y_2, mode='lines', name='MA Deaths')

trace3 = go.Scatter(x=x, y=y_3, mode='lines', name='FL Confirmed Cases')

trace4 = go.Scatter(x=x, y=y_4, mode='lines', name='FL Deaths')

data = [trace1, trace2, trace3, trace4]

ofl.iplot(data, filename='line-mode')


#print(len(y_MA))
#print(len(y_FL))
#print(len(y_3))

ynew_MA = []
ynew_FL = []
i = 0
MA_pop = []
FL_pop = []

# #print(Counter(y_FL))

ynew_MA = [item_1 for item_1 in y_MA if not(math.isnan(item_1)) == True]
ynew_FL = [item_2 for item_2 in y_FL if not(math.isnan(item_2)) == True]

change = len(y_MA) - len(ynew_MA)
#print(len(y_FL))
#print(len(ynew_FL))
#num_count = 0
while i < len(ynew_MA):
    
    MA_pop.append((y_1[211 + i] / ynew_MA[i]) * 100)
    #num_count += 1
   #print(num_count)
    #print(MA_pop)
    i += 1 
    
i = 0

while i < len(ynew_FL):
    FL_pop.append((y_3[214 + i] / ynew_FL[i]) * 100)
    i += 1
    
#print(MA_pop)
#print(FL_pop)
    
avg_MA = sum(MA_pop) / len(MA_pop)
avg_FL = sum(FL_pop) / len(FL_pop)
#print("MA: ", avg_MA)
#print("FL: ", avg_FL)


data = [go.Bar(
            x = ['Massachusetts' , 'Florida'],
            y = [avg_MA, avg_FL], 
            marker=dict(
            color=['rgba(0,191,255,0.7)','rgba(255,6,0,0.7)'])
    
    )]

print('This bar graph is the average perecentage of confirmed covid cases over the total test results of each day\n')

ofl.iplot(data, filename='basic-bar')

print('As the chart shows Massachusetts is more safe in comparison to Florida')

#Add error bars (its in plotly for bar graph)


# In[6]:


#Might add a delta variant chart 

