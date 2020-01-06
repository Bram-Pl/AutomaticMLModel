#!/usr/bin/env python
# coding: utf-8

# In[32]:


import pandas as pd


# In[33]:


data = pd.read_csv("Data/current.csv")


# In[34]:


list(data.columns)


# # Return from HTML after selection

# In[35]:


import pickle
import pandas as pd
import wtforms
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LinearRegression


# In[36]:


trainVar = ['age']


# In[37]:


print(data)


# In[38]:


dataX = data
datay = data[trainVar]
print(datay)

dataX.drop(datay, axis=1, inplace=True)
print(dataX)


# In[7]:


for col in dataX.columns:
    print(col)


# ##### datay is the variable to be calculated

# In[8]:


print(datay)


# In[9]:


data.columns


# In[10]:


X_train, X_test, y_train, y_test = train_test_split(dataX, datay, test_size=0.25, random_state=101)


# # Linear Regression Model

# In[11]:


lm = LinearRegression()


# In[12]:


lm.fit(X_train,y_train)


# In[13]:


predictions = lm.predict(X_test)


# In[14]:


counter = len(dataX.columns)
print(counter)


# In[15]:


columnsVar = []
for x in range(len(dataX.columns)):
    columnsVar.append(dataX.columns[x])


# In[16]:


for x in range(counter):
    print(columnsVar[x])


# In[17]:


print(columnsVar[0])


# In[18]:


pickle.dump(lm, open("model.pkl","wb"))

