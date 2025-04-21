from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(_name_)

model = pickle.load(open('tree_gridcv.pkl', 'rb'))
# Define the AQI categories and their effects
def get_aqi_category(aqi_value):
    if aqi_value <= 50:
        return "Good", "Air quality is considered satisfactory, and air pollution poses little or no risk."
    elif 51 <= aqi_value <= 100:
        return "Satisfactory", "Air quality is acceptable; however, for some pollutants, there may be a moderate health concern for a small number of people."
    elif 101 <= aqi_value <= 200:
        return "Moderate", "Members of sensitive groups may experience health effects. The general public is unlikely to be affected."
    elif 201 <= aqi_value <= 300:
        return "Poor", "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
    elif 301 <= aqi_value <= 400:
        return "Very Poor", "Health alert: everyone may experience more serious health effects."
    else:
        return "Severe", "Health warnings of emergency conditions. The entire population is more likely to be affected."

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    AQI_predict = None
    if request.method == 'POST':
        features = [
            float(request.form['T']),
            float(request.form['TM']),
            float(request.form['Tm']),
            float(request.form['SLP']),
            float(request.form['H']),
            float(request.form['VV']),
            float(request.form['V']),
            float(request.form['VM'])
        ]
        
        AQI_predict = model.predict([features])[0]
        category, health_effect = get_aqi_category(AQI_predict)

    return render_template('result.html', prediction=AQI_predict, category=category, health_effect=health_effect)

if _name_ == '_main_':
    app.run(debug=True)
