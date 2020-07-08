#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

bucket='kizsensordata'
data_key = 'datatraining.txt'
data_location = 's3://{}/{}'.format(bucket, data_key)

data1 = pd.read_csv(data_location, header=0, index_col=1, parse_dates=True, squeeze=True)


# In[2]:


data_key2 = 'datatest.txt'
data_location2 = 's3://{}/{}'.format(bucket, data_key2)

data2 = pd.read_csv(data_location2, header=0, index_col=1, parse_dates=True, squeeze=True)


# In[3]:


data_key3 = 'datatest2.txt'
data_location3 = 's3://{}/{}'.format(bucket, data_key3)

data3 = pd.read_csv(data_location3, header=0, index_col=1, parse_dates=True, squeeze=True)


# In[4]:


import matplotlib.pyplot as pyplot
n_features = data1.values.shape[1]
pyplot.figure()
for i in range(1, n_features):
	# specify the subpout
	pyplot.subplot(n_features, 1, i)
	# plot data from each set
	pyplot.plot(data1.index, data1.values[:, i])
	pyplot.plot(data2.index, data2.values[:, i])
	pyplot.plot(data3.index, data3.values[:, i])
	# add a readable name to the plot
	pyplot.title(data1.columns[i], y=0.5, loc='right')
pyplot.show()


# In[5]:


data = pd.concat([data1, data2, data3])
# save aggregated dataset
data.to_csv('combined.csv')


# In[6]:


data = pd.read_csv('combined.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
values = data.values
# split data into inputs and outputs
X, y = values[:, :-1], values[:, -1]
# split the dataset
from sklearn.model_selection import train_test_split
trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.3, shuffle=False, random_state=1)


# In[7]:


from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score

# make a naive prediction
def naive_prediction(testX, value):
	return [value for x in range(len(testX))]
 
# evaluate skill of predicting each class value
for value in [0, 1]:
	# forecast
	yhat = naive_prediction(testX, value)
	# evaluate
	score = accuracy_score(testy, yhat)
	# summarize
	print('Naive=%d score=%.3f' % (value, score))


# In[8]:


# logistic regression
from pandas import read_csv
# from sklearn.metrics import accuracy_score
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
# load the dataset
data = read_csv('combined.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
values = data.values
# split data into inputs and outputs
X, y = values[:, :-1], values[:, -1]
# split the dataset
trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.3, shuffle=False, random_state=1)
# define the model
model = LogisticRegression()
# fit the model on the training set
model.fit(trainX, trainy)
# predict the test set
yhat = model.predict(testX)
# evaluate model skill
score = accuracy_score(testy, yhat)
print(score)


# In[9]:


# More EDA - Summary Statistics
display(data.describe())


# In[10]:


import numpy as np
a = np.array(data).astype('float32')
labels = a[:,6]


# In[11]:


import sagemaker
import boto3

sess = sagemaker.Session()
prefix = "sagemaker/grades"


# In[12]:


import io
import sagemaker.amazon.common as smac
import os

buf = io.BytesIO()
smac.write_numpy_to_dense_tensor(buf, a, labels)
buf.seek(0)

key = 'linearlearner'
boto3.resource('s3').Bucket(bucket).Object(os.path.join(prefix, 'train', key)).upload_fileobj(buf)
s3_train_data = 's3://{}/{}/train/{}'.format(bucket, prefix, key)
print('uploaded training data location: {}'.format(s3_train_data))

output_location = 's3://{}/{}/output'.format(bucket, prefix)
print('training artifacts will be uploaded to: {}'.format(output_location))


# In[13]:


containers = {
             'us-east-2': '404615174143.dkr.ecr.us-east-2.amazonaws.com/linear-learner:latest'
             }
   
#containers[boto3.Session().region_name]


# In[14]:


linear = sagemaker.estimator.Estimator(containers[boto3.Session().region_name],
                                       role = sagemaker.get_execution_role(), 
                                       train_instance_count=1, 
                                       train_instance_type='ml.m4.xlarge',
                                       output_path=output_location,
                                       sagemaker_session=sess)


# In[15]:


# This is for 'dim' down below = 7
print(data.shape)


# In[16]:


get_ipython().run_cell_magic('time', '', "linear.set_hyperparameters(feature_dim=7,\n                           mini_batch_size=200,\n                           predictor_type='binary_classifier')\n\nlinear.fit({'train': s3_train_data})")


# In[17]:


linear_predictor = linear.deploy(initial_instance_count=1,
                                 instance_type='ml.m4.xlarge')


# In[18]:


from sagemaker.predictor import csv_serializer, json_deserializer

linear_predictor.content_type = 'text/csv'
linear_predictor.serializer = csv_serializer
linear_predictor.deserializer = json_deserializer


# In[19]:


result = linear_predictor.predict(a[0])
print(result)


# In[20]:


a[0]






