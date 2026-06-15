from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Load trained model
model = None

def load_model():
    global model
    if os.path.exists('rain_model.pkl'):
        with open('rain_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return True
    return False


@app.route('/')
def index():
    """Home page with prediction form"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Predict rainfall based on input parameters"""
    try:
        # Get form data
        data = request.form
        
        month = int(data['month'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        pressure = float(data['pressure'])
        wind_speed = float(data['wind_speed'])
        
        # Prepare input for model
        input_data = pd.DataFrame([[month, temperature, humidity, pressure, wind_speed]],
                                  columns=['month', 'temperature', 'humidity', 'pressure', 'wind_speed'])
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]
        
        # Result
        result = {
            'prediction': 'Rain Expected' if prediction == 1 else 'No Rain Expected',
            'probability': f'{probability:.2%}',
            'is_rain': prediction == 1
        }
        
        return render_template('index.html', result=result, inputs=data)
    
    except Exception as e:
        error_msg = f"Error making prediction: {str(e)}"
        return render_template('index.html', error=error_msg)


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    try:
        data = request.json
        
        month = int(data.get('month', 1))
        temperature = float(data.get('temperature', 30))
        humidity = float(data.get('humidity', 70))
        pressure = float(data.get('pressure', 1000))
        wind_speed = float(data.get('wind_speed', 15))
        
        input_data = pd.DataFrame([[month, temperature, humidity, pressure, wind_speed]],
                                  columns=['month', 'temperature', 'humidity', 'pressure', 'wind_speed'])
        
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]
        
        return jsonify({
            'success': True,
            'prediction': 'Rain Expected' if prediction == 1 else 'No Rain Expected',
            'probability': f'{probability:.2%}',
            'is_rain': prediction == 1
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


if __name__ == '__main__':
    print("Loading model...")
    if load_model():
        print("Model loaded successfully!")
        print("Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Error: Model not found! Please run 'python train_model.py' first.")
