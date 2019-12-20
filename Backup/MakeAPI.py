#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


data = pd.read_csv("uploads/current.csv")


# In[3]:


list(data.columns)


# # Return from HTML after selection

# In[4]:


import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LinearRegression


with open('trainVar.pkl', 'rb') as f:
    trainVar = pickle.load(f)

# In[5]:


dataX = data
datay = data[trainVar]
dataX.drop(datay,axis=1,inplace=True)

# ##### datay is the variable to be calculated

# In[6]:



# In[7]:


data.columns


# In[8]:


X_train, X_test, y_train, y_test = train_test_split(dataX, datay, test_size=0.25, random_state=101)


# # Linear Regression Model

# In[9]:


lm = LinearRegression()


# In[10]:


lm.fit(X_train,y_train)


# In[11]:


predictions = lm.predict(X_test)


# # Create API files

# In[12]:


import os
import shutil

for coly in datay.columns:
    namePredict = coly


# In[13]:


nameFolder = './API_CURRENT'

if not os.path.isdir(nameFolder) :
    os.mkdir(nameFolder)
if not os.path.isdir(nameFolder + '/templates') :    
    os.mkdir(nameFolder + '/templates')

pickle.dump(lm, open(nameFolder + "/model.pkl","wb"))


# In[14]:


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
strProc = "web: gunicorn PXLApp:app"

fileIndex = open(nameFolder + "/procfile", 'w')
fileIndex.write(strProc)
fileIndex.close();





