#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, \
     request, url_for
import pandas as pd
import wtforms
import pickle
import runpy
import time
import os
from flask import Flask, render_template, request
from flask_dropzone import Dropzone

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='.csv',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
)

dropzone = Dropzone(app)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'],"current.csv"))
    return data()

@app.route('/')#this needs to be the upload csv
@app.route('/data')#second page 
def data():
	data = pd.read_csv("uploads/current.csv")
	allCol = ""
	for col in data.columns:
		allCol += "{ \'column\' : \'" + str(col) + "\' },"
	return render_template(
		'getData.html',
		allModel = eval('[' + "{'model':'Logistic Regression Model'}, {'model':'Lineair Regression Model'}, {'model':'NA'}" + ']'),
		allColumns = eval('[' + allCol + ']') 
		)

@app.route("/test" , methods=['GET', 'POST'])
def test():
	getModel = request.form.get('model_select')
	getData = request.form.get('data_select')
	with open('trainVar.pkl', 'wb') as f:
		pickle.dump(getData, f)
	if (getModel == 'Lineair Regression Model' ) :
		runpy.run_module(mod_name='createLinear')
		time.sleep( 1 )
		return( "Building Lineair Regression Model... https://apicurrent.herokuapp.com/")
	elif (getModel == 'Logistic Regression Model' ) :
		runpy.run_module(mod_name='createLogistic')
		time.sleep( 1 )
		return( "Building Logistic Regression Model... https://apicurrent.herokuapp.com/")
	else:
		return( "Error, please try again" )

if __name__=='__main__':
	app.run(debug=True)