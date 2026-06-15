"""
Prediction Service for Crop Disease Detection
Handles loading models and making predictions
"""
import numpy as np
from preprocessing import DataPreprocessor
from model import CropDiseaseModel
from config import DISEASE_CLASSES


class PredictionService:
    """Service for making crop disease predictions"""
    
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.is_loaded = False
        
    def load(self):
        """Load both model and preprocessor"""
        print("Loading crop disease detection system...")
        
        # Initialize and load model
        self.model = CropDiseaseModel()
        model_loaded = self.model.load_model()
        
        if not model_loaded:
            print("Warning: No trained model found. Please train the model first.")
            return False
        
        # Initialize and load preprocessor
        self.preprocessor = DataPreprocessor()
        preprocessor_loaded = self.preprocessor.load_preprocessor()
        
        if not preprocessor_loaded:
            print("Warning: No preprocessor found. Using default settings.")
        
        self.is_loaded = True
        print("System loaded successfully!")
        return True
    
    def predict(self, image_path):
        """
        Make prediction for a single image
        Returns detailed prediction results
        """
        if not self.is_loaded:
            raise RuntimeError("Prediction service not loaded. Call load() first.")
        
        # Preprocess image
        processed_image = self.preprocessor.preprocess_single_image(image_path)
        
        if processed_image is None:
            return {
                'success': False,
                'error': 'Failed to process image'
            }
        
        # Make prediction
        result = self.model.predict_detailed(processed_image)
        
        # Add disease info
        result['success'] = True
        result['image_path'] = str(image_path)
        
        # Parse disease information
        predicted_class = result['predicted_class']
        crop_type, disease_status = self._parse_disease_class(predicted_class)
        
        result['crop_type'] = crop_type
        result['disease_status'] = disease_status
        result['is_healthy'] = disease_status.lower() == 'healthy'
        
        return result
    
    def predict_batch(self, image_paths):
        """Make predictions for multiple images"""
        if not self.is_loaded:
            raise RuntimeError("Prediction service not loaded. Call load() first.")
        
        results = []
        
        for img_path in image_paths:
            result = self.predict(img_path)
            results.append(result)
        
        return results
    
    def _parse_disease_class(self, class_name):
        """
        Parse disease class name into crop type and disease status
        Example: 'Tomato___Early_blight' -> ('Tomato', 'Early blight')
        """
        parts = class_name.split('___')
        
        if len(parts) != 2:
            return class_name, 'Unknown'
        
        crop = parts[0].replace('_', ' ').title()
        disease = parts[1].replace('_', ' ').title()
        
        return crop, disease
    
    def get_recommendations(self, disease_class):
        """Get treatment recommendations based on detected disease"""
        recommendations = {
            'Apple_scab': 'Apply fungicides like captan or ziram. Remove fallen leaves. Prune for better air circulation.',
            'Black_rot': 'Remove mummified fruits. Apply fungicides during bloom period. Practice good sanitation.',
            'Cedar_apple_rust': 'Remove nearby cedar trees if possible. Apply fungicides in spring.',
            'Powdery_mildew': 'Apply sulfur-based fungicides. Improve air circulation. Use resistant varieties.',
            'Bacterial_spot': 'Use copper-based bactericides. Remove infected plants. Avoid overhead irrigation.',
            'Early_blight': 'Apply chlorothalonil or mancozeb. Remove lower leaves. Rotate crops annually.',
            'Late_blight': 'Apply fungicides preventively. Remove infected plants immediately. Ensure good drainage.',
            'Leaf_Mold': 'Improve ventilation. Reduce humidity. Apply fungicides if severe.',
            'Septoria_leaf_spot': 'Remove infected leaves. Apply copper-based fungicides. Water at soil level.',
            'Target_Spot': 'Apply fungicides containing azoxystrobin. Improve air circulation.',
            'healthy': 'Continue good agricultural practices. Monitor regularly for early disease detection.'
        }
        
        # Extract disease type
        disease_key = disease_class.split('___')[-1]
        
        recommendation = recommendations.get(disease_key, 
            'Consult with local agricultural extension office for specific treatment recommendations.')
        
        return {
            'disease': disease_class,
            'recommendation': recommendation,
            'urgency': 'high' if 'blight' in disease_key.lower() or 'bacterial' in disease_key.lower() else 'medium'
        }


class SimplePredictor:
    """Simplified predictor for standalone use without full service"""
    
    def __init__(self, model_path=None):
        self.model = CropDiseaseModel()
        self.preprocessor = DataPreprocessor()
        self.loaded = False
        
        if model_path:
            self.model.load_model(model_path)
            self.preprocessor.load_preprocessor()
            self.loaded = True
    
    def predict(self, image_path):
        """Make prediction for single image"""
        if not self.loaded:
            raise RuntimeError("Model not loaded")
        
        processed_image = self.preprocessor.preprocess_single_image(image_path)
        result = self.model.predict_detailed(processed_image)
        
        return result


# Singleton instance
_prediction_service = None


def get_prediction_service():
    """Get singleton prediction service instance"""
    global _prediction_service
    if _prediction_service is None:
        _prediction_service = PredictionService()
    return _prediction_service


if __name__ == "__main__":
    # Test prediction service
    service = get_prediction_service()
    
    if service.load():
        print("\nPrediction service ready!")
        print(f"Supported diseases: {len(DISEASE_CLASSES)} classes")
    else:
        print("\nFailed to load prediction service")
