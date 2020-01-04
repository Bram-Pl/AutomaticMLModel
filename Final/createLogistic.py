#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import numpy as np


# In[19]:


data = pd.read_csv("uploads/current.csv")
##data = pd.read_csv("uploads/current.csv")


# In[20]:


list(data.columns)


# # Return from HTML after selection

# In[21]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle


# imported variables from html

# In[22]:


##selection = ['points_mean','dimension_mean','smoothness_se','symmetry_se','radius_worst','perimeter_worst']
with open('trainVar.pkl', 'rb') as f:
    trainVar = pickle.load(f)


# set imported data to dataX var

# In[23]:


dataX = data##[selection]
datay = trainVar

# get deferent names fer true or false (moet nog gedaan worden!!!)

# In[ ]:





# In[24]:


#print(data[trainVar])


# ## replace trainvar to 0 and 1 

# In[25]:


replace = pd.get_dummies(data[trainVar],drop_first=True)
data.drop(trainVar,axis=1,inplace=True)
data = pd.concat([data,replace],axis=1)
datay = data.iloc[:,-1]


# In[26]:


#print(datay)


# ### set name of 1/0 column in var

# In[27]:


TrainName = data.columns[-1]


# ### drop 1/0 column from dataset

# In[28]:


data.drop(data.columns[[-1,]], axis=1, inplace=True)


# ### write TrainName to .pkl file

# In[29]:


with open('LogRegTrainName.pkl', 'wb') as f:
    pickle.dump(API_CURRENT/TrainName, f)


# ###     

# In[30]:


X_train, X_test, y_train, y_test = train_test_split(dataX, datay, test_size=0.25, random_state=42)


# # logistic regresion

# In[31]:


logmodel = LogisticRegression()
logmodel.fit(X_train,y_train)


# In[32]:


predictions = logmodel.predict(X_test)


# ## classiffication report
# 

# In[33]:


#print(classification_report(y_test,predictions))


# In[ ]:





# In[34]:


##pickle.dump(logmodel, open("model.pkl","wb"))





import os
import shutil


namePredict = trainVar

nameFolder = './API_CURRENT'

if not os.path.isdir(nameFolder) :
    os.mkdir(nameFolder)
if not os.path.isdir(nameFolder + '/templates') :    
    os.mkdir(nameFolder + '/templates')

pickle.dump(logmodel, open(nameFolder + "/model.pkl","wb"))











#Creating index.html
strINDEX = "<!-- By Jarni Vanmal, Bram Plessers and Sven Musters -->" + "\n"
strINDEX = strINDEX +"<!DOCTYPE html>" + "\n"
strINDEX = strINDEX + "<html>" + "\n"
strINDEX = strINDEX + "<head>" + "\n"
strINDEX = strINDEX + "\t" + "<title>" + "Predict " + namePredict + "</title>" + "\n"
strINDEX = strINDEX + "</head>" + "\n"

strINDEX = strINDEX + "<body>" + "\n"
strINDEX = strINDEX + "\t" + "<h1>" + "Predict " + namePredict + "</h1>" + "\n"

strINDEX = strINDEX + "\t" + "{% block content %}{% endblock %}" + "\n"
strINDEX = strINDEX + "\t" + "<form action=\"/start\" method=\"post\" novalidate>" + "\n"
strINDEX = strINDEX + "\t" + "{{ form.hidden_tag() }}" + "\n"

for colx in dataX.columns:
    strINDEX = strINDEX + "\t\t" + "<p>" + "\n"
    strINDEX = strINDEX + "\t\t" + "{{ form." + colx + ".label }}<br>" + "\n"
    strINDEX = strINDEX + "\t\t" + "{{ form." + colx + "(size=32) }}" + "\n"
    strINDEX = strINDEX + "\t\t" + "</p>" + "\n\n"

strINDEX = strINDEX + "\t\t" + "<p>{{form.submit()}}</p>" + "\n"
strINDEX = strINDEX + "\t" + "</form>" + "\n"

strINDEX = strINDEX + "</body>" + "\n"
strINDEX = strINDEX + "</html>" + "\n"
 
fileIndex = open(nameFolder + "/templates/index.html", 'w')
fileIndex.write(strINDEX)
fileIndex.close();


# In[15]:


#Creating Result.html
strRESULT = "<!-- By Jarni Vanmal, Bram Plessers and Sven Musters -->" + "\n"
strRESULT = strRESULT + "{% extends \"index.html\" %}" + "\n"
strRESULT = strRESULT + "{% block content %}" + "\n"
strRESULT = strRESULT + "\t" + "<h2>Predicted " + namePredict + " is: {{" + namePredict + "}} </h2>" + "\n"
strRESULT = strRESULT + "{% endblock %}" + "\n"

fileIndex = open(nameFolder + "/templates/result.html", 'w')
fileIndex.write(strRESULT)
fileIndex.close();


# In[27]:


#Creating PXLApp.py
strPXLApp = "import pandas as pd" + "\n"
strPXLApp = strPXLApp + "import pickle" + "\n"
strPXLApp = strPXLApp + "import os" + "\n"
strPXLApp = strPXLApp + "from flask import Flask, url_for, request, json, Response, jsonify, render_template, redirect, flash" + "\n"
strPXLApp = strPXLApp + "from wtforms import  SubmitField, IntegerField" + "\n"
strPXLApp = strPXLApp + "from wtforms.validators import DataRequired" + "\n"
strPXLApp = strPXLApp + "from flask_wtf import FlaskForm" + "\n"
strPXLApp = strPXLApp + "from functools import wraps" + "\n"
strPXLApp = strPXLApp + "import joblib" + "\n"
strPXLApp = strPXLApp + "import numpy as np" + "\n"
strPXLApp = strPXLApp +  "\n"

strPXLApp = strPXLApp + "app = Flask(__name__)" + "\n"
strPXLApp = strPXLApp + "app.config['SECRET_KEY']='mysecret'" + "\n"
strPXLApp = strPXLApp + "\n"

strPXLApp = strPXLApp + "test_data_f =  { " 
for colx in dataX.columns:
    strPXLApp = strPXLApp + "\"" + colx + "\" : 0, "
strPXLApp = strPXLApp + "} \n"
strPXLApp = strPXLApp + "\n"

strPXLApp = strPXLApp + "class PredictForm(FlaskForm):" + "\n"
for colx in dataX.columns:
    strPXLApp = strPXLApp + "\t" + colx + " = IntegerField('" + colx + "')" + "\n"
strPXLApp = strPXLApp + "\t" + "submit=SubmitField('Predict')" + "\n"
strPXLApp = strPXLApp + "\n"

strPXLApp = strPXLApp + "class Config(object):" + "\n"
strPXLApp = strPXLApp + "\t" + "SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'" + "\n"
strPXLApp = strPXLApp + "\n"

strPXLApp = strPXLApp + "model_pkl = pickle.load(open('model.pkl','rb'))" + "\n"
strPXLApp = strPXLApp + "\n"

strPXLApp = strPXLApp + "@app.route('/',methods=['GET','POST'])" + "\n"
strPXLApp = strPXLApp + "@app.route('/start',methods=['GET','POST'])" + "\n"
strPXLApp = strPXLApp + "def start():" + "\n"
strPXLApp = strPXLApp + "\t" + "form = PredictForm()" + "\n"
strPXLApp = strPXLApp + "\t" + "if form.validate_on_submit():" + "\n"

strPXLApp = strPXLApp + "\t\t" + "flash('" + namePredict + "')" + "\n"

for colx in dataX.columns:
    strPXLApp = strPXLApp + "\t\t" + "test_data_f['" + colx + "']=form."+ colx + ".data" +"\n"
strPXLApp = strPXLApp + "\t\t" + "data=test_data_f" + "\n"
strPXLApp = strPXLApp + "\t\t" + "result=model_pkl.predict(pd.DataFrame(pd.DataFrame(data, index=[0])))[0]" + "\n"    
strPXLApp = strPXLApp + "\t\t" + "return render_template('result.html',title='model', form=form, " + namePredict + "=result)" + "\n"
strPXLApp = strPXLApp + "\t" + "return render_template('index.html', title='model', form=form)" + "\n"
strPXLApp = strPXLApp + "\n"

strPXLApp = strPXLApp + "if __name__ == '__main__':" + "\n"
strPXLApp = strPXLApp + "\t" + "app.run(debug=True)" + "\n"

fileIndex = open(nameFolder + "/API.py", 'w')
fileIndex.write(strPXLApp)
fileIndex.close();


# In[28]:


#Creating requirements.txt
strReq = "flask" + "\n"
strReq = strReq + "flask_wtf" + "\n"
strReq = strReq + "pandas" + "\n"
strReq = strReq + "sklearn" + "\n"
strReq = strReq + "wtforms" + "\n"
strReq = strReq + "numpy" + "\n"
strReq = strReq + "joblib" + "\n"
strReq = strReq + "gunicorn" + "\n"

fileIndex = open(nameFolder + "/requirements.txt", 'w')
fileIndex.write(strReq)
fileIndex.close();


# In[29]:


#Creating procfile
strProc = "web: gunicorn API:app"

fileIndex = open(nameFolder + "/Procfile", 'w')
fileIndex.write(strProc)
fileIndex.close();