#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyodbc 

server = '3.22.160.243' 
database = 'iot_viewer_test' 
username = 'proximity_iot_user' 
password = 'iot@prox2020*' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)


# In[2]:


import struct

def handle_datetimeoffset(dto_value):
    # ref: https://github.com/mkleehammer/pyodbc/issues/134#issuecomment-281739794
    tup = struct.unpack("<6hI2h", dto_value)  # e.g., (2017, 3, 16, 10, 35, 18, 0, -6, 0)
    tweaked = [tup[i] // 100 if i == 6 else tup[i] for i in range(len(tup))]
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:07d} {:+03d}:{:02d}".format(*tweaked)

cursor = cnxn.cursor()


# In[3]:


# To get table names
table_names = [x[2] for x in cursor.tables(tableType='TABLE')]
print(table_names) 


# In[4]:


cnxn.add_output_converter(-155, handle_datetimeoffset)


# In[5]:


# What type of join? What do we want to do with joined table? - inner join, left outer join, full outer join?
#cursor.execute('SELECT * FROM iot_viewer_test.dbo.devices inner join iot_viewer_test.dbo.deviceRawData on iot_viewer_test.dbo.devices.id = iot_viewer_test.dbo.deviceRawData.id')

#for row in cursor:
    #print(row)


# In[ ]:





# In[6]:


import pandas as pd

sql_query = pd.read_sql_query('SELECT * FROM iot_viewer_test.dbo.devices inner join iot_viewer_test.dbo.deviceRawData on iot_viewer_test.dbo.devices.id = iot_viewer_test.dbo.deviceRawData.id',cnxn)
print(sql_query)


# In[ ]:





# In[ ]:




