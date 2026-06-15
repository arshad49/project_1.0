# Kerala Rain Predictor 🌧️

A simple AI-powered rain prediction system for India (mainly Kerala) using Python and Flask.

## Features

- Machine Learning model (Random Forest) for rain prediction
- Simple web interface built with Flask
- Considers monsoon patterns specific to Kerala
- Takes 5 input parameters: Month, Temperature, Humidity, Pressure, Wind Speed

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Train the model:
```bash
python train_model.py
```

3. Run the Flask app:
```bash
python app.py
```

4. Open your browser and go to: `http://localhost:5000`

## How It Works

The system uses a Random Forest classifier trained on rainfall patterns typical to Kerala, India:
- **Southwest Monsoon** (June-September): Higher rain probability
- **Northeast Monsoon** (October-November): Moderate rain probability
- **Summer/Dry Season** (December-May): Lower rain probability

The model considers:
- Month (to account for monsoon seasons)
- Temperature
- Humidity
- Atmospheric Pressure
- Wind Speed

## Dataset

The system creates a synthetic dataset based on realistic Kerala rainfall patterns if no dataset is found. The dataset includes 1000 samples with realistic weather parameter distributions.

## API Endpoint

You can also use the REST API:

```bash
POST http://localhost:5000/api/predict
Content-Type: application/json

{
    "month": 7,
    "temperature": 28.5,
    "humidity": 85,
    "pressure": 995,
    "wind_speed": 20
}
```

## Project Structure

```
rai predictor/
├── app.py                 # Flask web application
├── train_model.py         # Model training script
├── requirements.txt       # Python dependencies
├── rainfall_data.csv      # Training dataset (auto-generated)
├── rain_model.pkl         # Trained model (auto-generated)
└── templates/
    └── index.html         # Web interface
```

## Notes

- The model achieves ~85-90% accuracy on test data
- You can replace the synthetic dataset with real historical data if available
- The web interface is mobile-responsive
