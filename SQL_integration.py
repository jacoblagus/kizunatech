# Must first install ODBC Driver on Amazon Sagemaker terminal: https://aws.amazon.com/premiumsupport/knowledge-center/odbc-driver-sagemaker-sql-server/

import pyodbc 

server = '3.22.160.243' 
database = 'iot_viewer_test' 
username = 'proximity_iot_user' 
password = 'iot@prox2020*' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)


import struct


# Handles -155 error with datatype
def handle_datetimeoffset(dto_value):
    # ref: https://github.com/mkleehammer/pyodbc/issues/134#issuecomment-281739794
    tup = struct.unpack("<6hI2h", dto_value)  # e.g., (2017, 3, 16, 10, 35, 18, 0, -6, 0)
    tweaked = [tup[i] // 100 if i == 6 else tup[i] for i in range(len(tup))]
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:07d} {:+03d}:{:02d}".format(*tweaked)


cursor = cnxn.cursor()


# To get table names
table_names = [x[2] for x in cursor.tables(tableType='TABLE')]
print(table_names) 


cnxn.add_output_converter(-155, handle_datetimeoffset)


import pandas as pd

sql_query = pd.read_sql_query('SELECT * FROM iot_viewer_test.dbo.devices inner join iot_viewer_test.dbo.deviceRawData on iot_viewer_test.dbo.devices.id = iot_viewer_test.dbo.deviceRawData.id',cnxn)
print(sql_query)
