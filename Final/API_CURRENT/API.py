import pandas as pd
import pickle
import os
from flask import Flask, url_for, request, json, Response, jsonify, render_template, redirect, flash
from wtforms import  SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from functools import wraps
import joblib
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY']='mysecret'

test_data_f =  { "cement" : 0, "slag" : 0, "ash" : 0, "water" : 0, "superplastic" : 0, "coarseagg" : 0, "fineagg" : 0, "strength" : 0, } 

class PredictForm(FlaskForm):
	cement = IntegerField('cement')
	slag = IntegerField('slag')
	ash = IntegerField('ash')
	water = IntegerField('water')
	superplastic = IntegerField('superplastic')
	coarseagg = IntegerField('coarseagg')
	fineagg = IntegerField('fineagg')
	strength = IntegerField('strength')
	submit=SubmitField('Predict')

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

model_pkl = pickle.load(open('model.pkl','rb'))

@app.route('/',methods=['GET','POST'])
@app.route('/start',methods=['GET','POST'])
def start():
	form = PredictForm()
	if form.validate_on_submit():
		flash('age')
		test_data_f['cement']=form.cement.data
		test_data_f['slag']=form.slag.data
		test_data_f['ash']=form.ash.data
		test_data_f['water']=form.water.data
		test_data_f['superplastic']=form.superplastic.data
		test_data_f['coarseagg']=form.coarseagg.data
		test_data_f['fineagg']=form.fineagg.data
		test_data_f['strength']=form.strength.data
		data=test_data_f
		result=model_pkl.predict(pd.DataFrame(pd.DataFrame(data, index=[0])))[0]
		return render_template('result.html',title='model', form=form, age=result)
	return render_template('index.html', title='model', form=form)

if __name__ == '__main__':
	app.run(debug=True)
