# After deploying model in Sagemaker, you can run this in local Python session to make prediction

import sagemaker
import boto3
import pandas as pd
import requests
import json

sess = sagemaker.Session(boto3.session.Session(region_name='us-east-2'))
role = 'arn:aws:iam::178346040475:role/service-role/AmazonSageMaker-ExecutionRole-20200616T152066'


request = requests.get('https://0n5dn59xeb.execute-api.us-east-2.amazonaws.com/LogisticStart')
print(request.status_code)


customHeader = {'x-api-key': '6NN6vAjuJRqENqcXccJF1DdOqUBpw2f6RitcO3af'}
r = requests.post('https://jert93zwv9.execute-api.us-east-2.amazonaws.com/FirstStage/test-logistic', data=json.dumps({"data":"1.0000000e+00, 2.3180000e+01, 2.7271999e+01, 4.2600000e+02,7.2125000e+02, 4.7929883e-03, 1.0000000e+00"}), headers=customHeader)



r.text
