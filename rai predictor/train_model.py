import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os


def load_or_create_dataset():
    """Load rainfall data or create sample dataset for India/Kerala"""
    
    # Check if dataset exists
    if os.path.exists('rainfall_data.csv'):
        print("Loading existing dataset...")
        df = pd.read_csv('rainfall_data.csv')
        return df
    
    # Create synthetic dataset based on typical Kerala/India rainfall patterns
    print("Creating rainfall dataset...")
    np.random.seed(42)
    
    # Months with typical monsoon patterns in Kerala
    # Kerala has Southwest monsoon (June-Sept) and Northeast monsoon (Oct-Nov)
    n_samples = 1000
    
    data = {
        'month': np.random.randint(1, 13, n_samples),
        'temperature': np.random.uniform(25, 35, n_samples),  # Celsius
        'humidity': np.random.uniform(40, 95, n_samples),  # Percentage
        'pressure': np.random.uniform(990, 1010, n_samples),  # hPa
        'wind_speed': np.random.uniform(5, 30, n_samples),  # km/h
    }
    
    df = pd.DataFrame(data)
    
    # Create realistic rainfall labels based on patterns
    # Higher probability during monsoon months
    rainfall = []
    for idx, row in df.iterrows():
        base_prob = 0.3
        
        # Monsoon months (June-September) - Southwest monsoon
        if row['month'] in [6, 7, 8, 9]:
            base_prob = 0.7
        # October-November - Northeast monsoon
        elif row['month'] in [10, 11]:
            base_prob = 0.5
        # May - Pre-monsoon
        elif row['month'] == 5:
            base_prob = 0.4
        
        # Adjust based on humidity
        if row['humidity'] > 80:
            base_prob += 0.2
        elif row['humidity'] < 50:
            base_prob -= 0.2
        
        # Adjust based on pressure (lower pressure = more likely rain)
        if row['pressure'] < 995:
            base_prob += 0.15
        
        # Final probability check
        will_rain = 1 if np.random.random() < base_prob else 0
        rainfall.append(will_rain)
    
    df['rainfall'] = rainfall
    
    # Save dataset
    df.to_csv('rainfall_data.csv', index=False)
    print(f"Dataset created with {len(df)} samples")
    print(f"Rain distribution: {df['rainfall'].value_counts().to_dict()}")
    
    return df


def train_model(df):
    """Train a Random Forest model for rain prediction"""
    
    # Prepare features and target
    features = ['month', 'temperature', 'humidity', 'pressure', 'wind_speed']
    X = df[features]
    y = df['rainfall']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train Random Forest model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"\nModel Training Complete:")
    print(f"Training Accuracy: {train_score:.2%}")
    print(f"Test Accuracy: {test_score:.2%}")
    
    # Save model
    with open('rain_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("\nModel saved to rain_model.pkl")
    
    # Feature importance
    importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print("\nFeature Importance:")
    print(importance)
    
    return model


def main():
    print("=" * 50)
    print("India/Kerala Rain Prediction Model Training")
    print("=" * 50)
    
    # Load or create dataset
    df = load_or_create_dataset()
    
    # Train model
    model = train_model(df)
    
    print("\n" + "=" * 50)
    print("Training Complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
