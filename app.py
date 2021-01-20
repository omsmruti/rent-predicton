import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
	Area=int(request.form['Area'])
	City=str(request.form['City'])
	Rooms=int(request.form['rooms'])
	Bathrooms=int(request.form['bathrooms'])
	Parking_Spaces=int(request.form['parking spaces'])
	Floor=int(request.form['floor'])
	Animal=request.form['Animal']
	Furniture=request.form['Furniture']

	def furniture(x):
	    if x=='furnished':
	        return 1
	    else:
	        return 0

	def animal(x):
	    if x=='acepted':
	        return 1
	    else:
	        return 0

	Animal=animal(Animal)
	Furniture=furniture(Furniture)

	if City=='Campinas':
			city_Campinas=1
			city_Porto_Alegre=0
			city_Rio_de_Janeiro=0
			city_São_Paulo=0
	elif City=='Porto Alegre':
			city_Campinas=0
			city_Porto_Alegre=1
			city_Rio_de_Janeiro=0
			city_São_Paulo=0
	elif City=='Rio de Janeiro':
			city_Campinas=0
			city_Porto_Alegre=0
			city_Rio_de_Janeiro=1
			city_São_Paulo=0
	elif City=='São Paulo'	:
			city_Campinas=0
			city_Porto_Alegre=0
			city_Rio_de_Janeiro=0
			city_São_Paulo=1
	else:
			city_Campinas=0
			city_Porto_Alegre=0
			city_Rio_de_Janeiro=0
			city_São_Paulo=0

	if (Floor==0):
			Floor_Binned=0
	elif (Floor<10):
			Floor_Binned=1
	elif (Floor<20):
			Floor_Binned=2
	else:
			Floor_Binned=3

	final_features = [Area,Rooms,Bathrooms,Parking_Spaces,Furniture,Floor_Binned,city_Campinas,city_Porto_Alegre,city_Rio_de_Janeiro,city_São_Paulo,Animal]
	prediction = model.predict(final_features)
	output = round(prediction[0], 2)
	return render_template('index.html', prediction_text='Rent Price should be {}'.format(output))

@app.route('/predict_api',methods=['POST'])
def predict_api():
	data = request.get_json(force=True)
	prediction = model.predict([np.array(list(data.values()))])
	output = prediction[0]
	return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)


