"""
Example usage of Crop Disease Detection System
This script demonstrates how to use the prediction service programmatically
"""
from prediction_service import get_prediction_service
from config import DISEASE_CLASSES


def example_usage():
    """Demonstrate the crop disease detection system"""
    
    print("=" * 70)
    print("CROP DISEASE DETECTION SYSTEM - EXAMPLE USAGE")
    print("=" * 70)
    
    # Initialize prediction service
    print("\n[1/3] Initializing prediction service...")
    service = get_prediction_service()
    
    if not service.load():
        print("\n⚠ Model not found. Please train the model first:")
        print("   python train.py")
        return
    
    print("✓ Prediction service loaded successfully")
    
    # Show supported diseases
    print(f"\n[2/3] System Information:")
    print(f"   Total disease classes: {len(DISEASE_CLASSES)}")
    print(f"   Supported crops: Apple, Tomato, Potato, Corn, Grape, Pepper, etc.")
    
    # Example prediction (uncomment when you have an image)
    print(f"\n[3/3] Making Predictions:")
    print("""
To predict disease from an image, use:

    result = service.predict('path/to/leaf.jpg')
    
    # Access results
    print(f"Crop: {result['crop_type']}")
    print(f"Disease: {result['disease_status']}")
    print(f"Confidence: {result['confidence']*100:.2f}%")
    
    # Get recommendations
    rec = service.get_recommendations(result['predicted_class'])
    print(f"Treatment: {rec['recommendation']}")

Or use command line:
    python main.py predict --image path/to/leaf.jpg

Or use the web interface:
    python main.py frontend
    """)
    
    # Example with mock data
    print("\n" + "=" * 70)
    print("EXAMPLE OUTPUT (Mock)")
    print("=" * 70)
    
    mock_result = {
        'crop_type': 'Tomato',
        'disease_status': 'Early Blight',
        'predicted_class': 'Tomato___Early_blight',
        'confidence': 0.9845,
        'is_healthy': False,
        'top_3_predictions': [
            {'class': 'Tomato___Early_blight', 'confidence': 0.9845},
            {'class': 'Tomato___Late_blight', 'confidence': 0.0120},
            {'class': 'Tomato___healthy', 'confidence': 0.0035}
        ]
    }
    
    print(f"\nCrop Type: {mock_result['crop_type']}")
    print(f"Disease Status: {mock_result['disease_status']}")
    print(f"Predicted Class: {mock_result['predicted_class']}")
    print(f"Confidence: {mock_result['confidence']*100:.2f}%")
    print(f"Healthy: {'Yes ✓' if mock_result['is_healthy'] else 'No ✗'}")
    
    print("\nTop 3 Predictions:")
    for i, pred in enumerate(mock_result['top_3_predictions'], 1):
        confidence_pct = pred['confidence'] * 100
        print(f"  {i}. {pred['class']}: {confidence_pct:.2f}%")
    
    # Get treatment recommendation
    rec = service.get_recommendations(mock_result['predicted_class'])
    print(f"\nTreatment Recommendation:")
    print(f"  {rec['recommendation']}")
    print(f"  Urgency: {rec['urgency'].upper()}")
    
    print("\n" + "=" * 70)
    print("Ready to detect crop diseases!")
    print("=" * 70)


if __name__ == "__main__":
    example_usage()
