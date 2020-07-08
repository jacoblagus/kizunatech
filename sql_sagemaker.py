# Must first install ODBC Driver on Amazon Sagemaker terminal: https://aws.amazon.com/premiumsupport/knowledge-center/odbc-driver-sagemaker-sql-server/

import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = '35.178.133.141' 
database = 'proximity_iot' 
username = 'user_iot' 
password = 'user_iot' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

test = cursor.execute('SELECT * FROM proximity_iot.dbo.deviceRawData')
data = cursor.fetchall()
for line in data:
    print(line)
