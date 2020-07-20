#!/usr/bin/env python
# coding: utf-8

# In[58]:


# Read in data

import pandas as pd
df = pd.read_csv('Data/HOJA_DE_TRAB_INS_TRABAJO.csv', header=1, skipfooter=7, engine = 'python')
#df.head(10)


# In[59]:


# Reorder columns from alphabetical to chronological

cols = df.columns.tolist()
cols = cols[0:2] + cols[5:6] + cols[6:7] + cols[9:10] + cols[2:3] + cols[10:11] + cols[8:9] + cols[7:8] + cols[3:4] + cols[13:14] + cols[12:13] + cols[11:12] + cols[4:5] + cols[14:]
df = df[cols] 
df.head(10)


# In[60]:


import numpy as np
a = np.array(df.fillna(0))


# In[61]:


# print first row of data
column = 2
for month in range(12):
    print(a[0][column])
    column+=1


# In[62]:


# Moving average to predict supply based trivially on previous 3 months.
# Take array as input and produces array as output

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


# In[63]:


# predictions for first row of data
# first prediction in this array is the prediction for the fourth month above — and so on
# Not super accurate — but a start

b = a[0][2:14]
moving_average(b,3)


# Could do a prediction for each month, beginning with the fourth month. You would want to do this for each medicine, though, which would result in a 2D array, so pretty big (comparable to size of original data set essetially). This would allow us to actually see accuracy of our model because we could test it against our data. Othrwise, could also just create one 'prediction' column, and have one prediction for each row. This would just be based upon the past n months and would predict the supply for the month coming after the last one. Also, note that these months in the columns are not in order, so they should probably be reordered.

# One notable problem with this model is that supply kind of lags behind, whether that means overabundance or scarcity. Another issue is that it does not give different weights to different months, which could be a problem if certain medications are in higher demand on a more seasonal basis.

# In[ ]:




