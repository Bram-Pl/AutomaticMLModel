from flask import Flask, url_for, request, json, Response, jsonify, render_template, redirect, flash
from wtforms import  SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from functools import wraps
import joblib
import numpy as np 
import pickle
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY']='mysecret'

test_data_f =  { "cement" : 10, "slag" : 25000, "ash" : 110, "water" : 1600, "superplastic" : 1200, "coarseagg" : 570, "fineagg" : 80, "age" : 16}  

class PredictForm(FlaskForm):
	cement = IntegerField('cement')
	slag = IntegerField('slag')
	ash = IntegerField('ash')
	water = IntegerField('water')
	superplastic = IntegerField('superplastic')
	coarseagg = IntegerField('coarseagg')
	fineagg = IntegerField('fineagg')
	age = IntegerField('age')
	submit = SubmitField('Calculate the strength of the cement')

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

model_pkl = pickle.load(open('lmmodel.pkl','rb'))

@app.route('/hi', methods = ['GET'])
def api_hi():
	data = {
		'hello': 'hiworld',
		'number': 456
	}
	js = json.dumps(data)

	resp = Response(js, status=200, mimetype='application/json')
	resp.headers['Link']= 'http://www.cteq.eu'
	return resp

@app.route('/start',methods=['GET','POST'])
def start():
	form = PredictForm()
	if form.validate_on_submit():
		flash('Cement Strength Calculation Requested')
		test_data_f['cement']=form.cement.data
		test_data_f['slag']=form.slag.data
		test_data_f['ash']=form.ash.data
		test_data_f['water']=form.water.data
		test_data_f['superplastic']=form.superplastic.data
		test_data_f['coarseagg']=form.coarseagg.data
		test_data_f['fineagg']=form.fineagg.data
		test_data_f['age']=form.age.data
		data = test_data_f
		result=model_pkl.predict(pd.DataFrame(pd.DataFrame(data, index=[0])))[0]      
		return render_template('result.html',title='Cement strength prediction', form=form, strength=result)       
	return render_template('index.html', title='Cement strength prediction', form=form)


# This can be used with curl to test the api/webserver
@app.route('/predict', methods=['POST'])
def price_predict():
	if request.method == 'POST':
	# Get the data from the POST method
		data = request.get_json(force=True)     
	# Predict using Model loaded from pkl file 
	return jsonify(model_pkl.predict(pd.DataFrame(pd.DataFrame(data, index=[0])))[0])

@app.route('/apitest_json')
def apitest_json():
	test_data =  { "cement" : 10, "slag" : 25000, "ash" : 110, "water" : 1600, "superplastic" : 1200, "coarseagg" : 69, "fineagg" : 420, "age" : 18}    
	return jsonify(model_pkl.predict(pd.DataFrame(pd.DataFrame(test_data, index=[0])))[0])

@app.route('/apitest')
def apitest():   
	return jsonify(model_pkl.predict(pd.DataFrame([[10,25000,110,1600,1200]]))[0])

if __name__ == '__main__':
	app.run(debug=True)
