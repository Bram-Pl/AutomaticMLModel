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

test_data_f =  { "id" : 0, "radius_mean" : 0, "texture_mean" : 0, "perimeter_mean" : 0, "area_mean" : 0, "smoothness_mean" : 0, "compactness_mean" : 0, "concavity_mean" : 0, "points_mean" : 0, "symmetry_mean" : 0, "dimension_mean" : 0, "radius_se" : 0, "texture_se" : 0, "perimeter_se" : 0, "area_se" : 0, "smoothness_se" : 0, "compactness_se" : 0, "concavity_se" : 0, "points_se" : 0, "symmetry_se" : 0, "dimension_se" : 0, "radius_worst" : 0, "texture_worst" : 0, "perimeter_worst" : 0, "area_worst" : 0, "smoothness_worst" : 0, "compactness_worst" : 0, "concavity_worst" : 0, "points_worst" : 0, "symmetry_worst" : 0, "dimension_worst" : 0, } 

class PredictForm(FlaskForm):
	id = IntegerField('id')
	radius_mean = IntegerField('radius_mean')
	texture_mean = IntegerField('texture_mean')
	perimeter_mean = IntegerField('perimeter_mean')
	area_mean = IntegerField('area_mean')
	smoothness_mean = IntegerField('smoothness_mean')
	compactness_mean = IntegerField('compactness_mean')
	concavity_mean = IntegerField('concavity_mean')
	points_mean = IntegerField('points_mean')
	symmetry_mean = IntegerField('symmetry_mean')
	dimension_mean = IntegerField('dimension_mean')
	radius_se = IntegerField('radius_se')
	texture_se = IntegerField('texture_se')
	perimeter_se = IntegerField('perimeter_se')
	area_se = IntegerField('area_se')
	smoothness_se = IntegerField('smoothness_se')
	compactness_se = IntegerField('compactness_se')
	concavity_se = IntegerField('concavity_se')
	points_se = IntegerField('points_se')
	symmetry_se = IntegerField('symmetry_se')
	dimension_se = IntegerField('dimension_se')
	radius_worst = IntegerField('radius_worst')
	texture_worst = IntegerField('texture_worst')
	perimeter_worst = IntegerField('perimeter_worst')
	area_worst = IntegerField('area_worst')
	smoothness_worst = IntegerField('smoothness_worst')
	compactness_worst = IntegerField('compactness_worst')
	concavity_worst = IntegerField('concavity_worst')
	points_worst = IntegerField('points_worst')
	symmetry_worst = IntegerField('symmetry_worst')
	dimension_worst = IntegerField('dimension_worst')
	submit=SubmitField('Predict')

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

model_pkl = pickle.load(open('model.pkl','rb'))

with open('LogRegTrainName.pkl', 'rb') as f:
    TrainName = pickle.load(f)

@app.route('/',methods=['GET','POST'])
@app.route('/start',methods=['GET','POST'])
def start():
	form = PredictForm()
	if form.validate_on_submit():
		flash('diagnosis')
		test_data_f['id']=form.id.data
		test_data_f['radius_mean']=form.radius_mean.data
		test_data_f['texture_mean']=form.texture_mean.data
		test_data_f['perimeter_mean']=form.perimeter_mean.data
		test_data_f['area_mean']=form.area_mean.data
		test_data_f['smoothness_mean']=form.smoothness_mean.data
		test_data_f['compactness_mean']=form.compactness_mean.data
		test_data_f['concavity_mean']=form.concavity_mean.data
		test_data_f['points_mean']=form.points_mean.data
		test_data_f['symmetry_mean']=form.symmetry_mean.data
		test_data_f['dimension_mean']=form.dimension_mean.data
		test_data_f['radius_se']=form.radius_se.data
		test_data_f['texture_se']=form.texture_se.data
		test_data_f['perimeter_se']=form.perimeter_se.data
		test_data_f['area_se']=form.area_se.data
		test_data_f['smoothness_se']=form.smoothness_se.data
		test_data_f['compactness_se']=form.compactness_se.data
		test_data_f['concavity_se']=form.concavity_se.data
		test_data_f['points_se']=form.points_se.data
		test_data_f['symmetry_se']=form.symmetry_se.data
		test_data_f['dimension_se']=form.dimension_se.data
		test_data_f['radius_worst']=form.radius_worst.data
		test_data_f['texture_worst']=form.texture_worst.data
		test_data_f['perimeter_worst']=form.perimeter_worst.data
		test_data_f['area_worst']=form.area_worst.data
		test_data_f['smoothness_worst']=form.smoothness_worst.data
		test_data_f['compactness_worst']=form.compactness_worst.data
		test_data_f['concavity_worst']=form.concavity_worst.data
		test_data_f['points_worst']=form.points_worst.data
		test_data_f['symmetry_worst']=form.symmetry_worst.data
		test_data_f['dimension_worst']=form.dimension_worst.data
		data=test_data_f
		result=model_pkl.predict(pd.DataFrame(pd.DataFrame(data, index=[0])))[0]

		if result == 1:
		    print(TrainName)
		elif result == 0:
		    print("Not" ,TrainName)

		return render_template('result.html',title='model', form=form, diagnosis=result)
	return render_template('index.html', title='model', form=form)

if __name__ == '__main__':
	app.run(debug=True)
