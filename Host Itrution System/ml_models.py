"""
Machine Learning Models Module - Implements various ML models for intrusion detection
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from sklearn.ensemble import IsolationForest, RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import OneClassSVM
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntrusionDetectionModel:
    """Base class for intrusion detection models"""
    
    def __init__(self, model_type: str = 'isolation_forest'):
        self.model_type = model_type
        self.model = None
        self.is_fitted = False
        self.feature_names = []
        self.threshold = 0.5
        
    def train(self, X: np.ndarray, y: np.ndarray = None):
        """Train the model"""
        raise NotImplementedError
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        raise NotImplementedError
    
    def save(self, filepath: str):
        """Save model to disk"""
        joblib.dump(self.model, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load(self, filepath: str):
        """Load model from disk"""
        self.model = joblib.load(filepath)
        self.is_fitted = True
        logger.info(f"Model loaded from {filepath}")


class AnomalyDetectionModel(IntrusionDetectionModel):
    """Unsupervised anomaly detection model"""
    
    def __init__(self, contamination: float = 0.1, n_estimators: int = 100, 
                 random_state: int = 42):
        super().__init__('anomaly_detection')
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.random_state = random_state
        
    def train(self, X: np.ndarray, y: np.ndarray = None):
        """Train isolation forest for anomaly detection"""
        try:
            self.model = IsolationForest(
                n_estimators=self.n_estimators,
                contamination=self.contamination,
                random_state=self.random_state,
                bootstrap=True
            )
            
            self.model.fit(X)
            self.is_fitted = True
            self.feature_names = list(range(X.shape[1]))
            
            logger.info("Isolation Forest model trained successfully")
            return self
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return None
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict anomalies (-1 for anomaly, 1 for normal)"""
        if not self.is_fitted:
            raise ValueError("Model not fitted yet")
        
        predictions = self.model.predict(X)
        # Convert to binary: 1 for anomaly, 0 for normal
        predictions = (predictions == -1).astype(int)
        
        return predictions
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Get anomaly scores"""
        if not self.is_fitted:
            raise ValueError("Model not fitted yet")
        
        # Get anomaly scores (more negative = more anomalous)
        scores = self.model.decision_function(X)
        
        # Convert to probability-like scores (0-1)
        # Normalize scores to 0-1 range where higher = more anomalous
        min_score = scores.min()
        max_score = scores.max()
        
        if max_score - min_score > 0:
            probabilities = 1 - (scores - min_score) / (max_score - min_score)
        else:
            probabilities = np.zeros_like(scores)
        
        return probabilities
    
    def get_anomalies(self, X: np.ndarray, threshold: float = None) -> Tuple[np.ndarray, np.ndarray]:
        """Get anomalies above threshold"""
        if threshold is None:
            threshold = self.threshold
        
        probabilities = self.predict_proba(X)
        predictions = (probabilities >= threshold).astype(int)
        
        return predictions, probabilities


class SupervisedClassificationModel(IntrusionDetectionModel):
    """Supervised classification model for known attack patterns"""
    
    def __init__(self, model_type: str = 'random_forest', n_estimators: int = 100,
                 random_state: int = 42):
        super().__init__(model_type)
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.class_weights = None
        
    def train(self, X: np.ndarray, y: np.ndarray):
        """Train supervised classification model"""
        try:
            if self.model_type == 'random_forest':
                self.model = RandomForestClassifier(
                    n_estimators=self.n_estimators,
                    random_state=self.random_state,
                    class_weight='balanced',
                    n_jobs=-1
                )
            elif self.model_type == 'gradient_boosting':
                self.model = GradientBoostingClassifier(
                    n_estimators=self.n_estimators,
                    random_state=self.random_state
                )
            elif self.model_type == 'logistic_regression':
                self.model = LogisticRegression(
                    random_state=self.random_state,
                    class_weight='balanced',
                    max_iter=1000
                )
            else:
                raise ValueError(f"Unknown model type: {self.model_type}")
            
            self.model.fit(X, y)
            self.is_fitted = True
            self.feature_names = list(range(X.shape[1]))
            
            # Calculate class weights for imbalanced datasets
            self.class_weights = self.calculate_class_weights(y)
            
            logger.info(f"{self.model_type} model trained successfully")
            return self
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return None
    
    def calculate_class_weights(self, y: np.ndarray) -> Dict[int, float]:
        """Calculate class weights for imbalanced data"""
        unique, counts = np.unique(y, return_counts=True)
        total = len(y)
        weights = {}
        
        for class_id, count in zip(unique, counts):
            weights[class_id] = total / (len(unique) * count)
        
        return weights
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels"""
        if not self.is_fitted:
            raise ValueError("Model not fitted yet")
        
        return self.model.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Get prediction probabilities"""
        if not self.is_fitted:
            raise ValueError("Model not fitted yet")
        
        return self.model.predict_proba(X)
    
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Evaluate model performance"""
        if not self.is_fitted:
            raise ValueError("Model not fitted yet")
        
        predictions = self.predict(X)
        
        metrics = {
            'accuracy': accuracy_score(y, predictions),
            'classification_report': classification_report(y, predictions, zero_division=0)
        }
        
        logger.info(f"Accuracy: {metrics['accuracy']:.4f}")
        logger.info(f"Classification Report:\n{metrics['classification_report']}")
        
        return metrics
    
    def get_feature_importance(self) -> np.ndarray:
        """Get feature importance scores"""
        if not self.is_fitted:
            raise ValueError("Model not fitted yet")
        
        if hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        else:
            logger.warning("Model does not support feature importance")
            return None


class HybridIntrusionDetection:
    """Hybrid model combining multiple approaches"""
    
    def __init__(self):
        self.anomaly_detector = AnomalyDetectionModel()
        self.classifier = SupervisedClassificationModel(model_type='random_forest')
        self.voting_weights = {'anomaly': 0.6, 'classifier': 0.4}
        self.is_fitted = False
        
    def train_anomaly_detector(self, X: np.ndarray):
        """Train the anomaly detection component"""
        self.anomaly_detector.train(X)
        logger.info("Anomaly detector trained")
    
    def train_classifier(self, X: np.ndarray, y: np.ndarray):
        """Train the classification component"""
        self.classifier.train(X, y)
        logger.info("Classifier trained")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Combine predictions from both models"""
        if not self.is_fitted:
            raise ValueError("Models not fitted yet")
        
        # Get anomaly scores
        anomaly_scores = self.anomaly_detector.predict_proba(X)
        
        # Get classifier predictions (if trained with labels)
        try:
            classifier_probs = self.classifier.predict_proba(X)[:, 1]
        except:
            classifier_probs = np.zeros(len(X))
        
        # Weighted combination
        combined_scores = (
            self.voting_weights['anomaly'] * anomaly_scores +
            self.voting_weights['classifier'] * classifier_probs
        )
        
        # Threshold at 0.5
        predictions = (combined_scores >= 0.5).astype(int)
        
        return predictions, combined_scores
    
    def save(self, base_path: str):
        """Save both models"""
        os.makedirs(os.path.dirname(base_path), exist_ok=True)
        self.anomaly_detector.save(f"{base_path}_anomaly.pkl")
        self.classifier.save(f"{base_path}_classifier.pkl")
        logger.info("Both models saved")
    
    def load(self, base_path: str):
        """Load both models"""
        self.anomaly_detector.load(f"{base_path}_anomaly.pkl")
        self.classifier.load(f"{base_path}_classifier.pkl")
        self.is_fitted = True
        logger.info("Both models loaded")


class ModelTrainer:
    """Utility class for training and managing models"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.models = {}
        
    def train_models(self, X_train: np.ndarray, y_train: np.ndarray = None,
                    X_val: np.ndarray = None, y_val: np.ndarray = None) -> Dict:
        """Train multiple models and compare performance"""
        
        results = {}
        
        # Train anomaly detection model
        logger.info("Training Isolation Forest...")
        iforest = AnomalyDetectionModel(
            contamination=self.config.get('contamination', 0.1),
            n_estimators=self.config.get('n_estimators', 100)
        )
        iforest.train(X_train)
        results['isolation_forest'] = iforest
        
        # Train supervised model if labels provided
        if y_train is not None:
            logger.info("Training Random Forest Classifier...")
            rf = SupervisedClassificationModel(model_type='random_forest')
            rf.train(X_train, y_train)
            
            if X_val is not None and y_val is not None:
                val_metrics = rf.evaluate(X_val, y_val)
                results['random_forest_metrics'] = val_metrics
            
            results['random_forest'] = rf
            
            logger.info("Training Gradient Boosting...")
            gb = SupervisedClassificationModel(model_type='gradient_boosting')
            gb.train(X_train, y_train)
            results['gradient_boosting'] = gb
        
        self.models = results
        return results
    
    def select_best_model(self, X_val: np.ndarray, y_val: np.ndarray) -> IntrusionDetectionModel:
        """Select best performing model based on validation data"""
        best_model = None
        best_score = 0
        
        for name, model in self.models.items():
            if isinstance(model, SupervisedClassificationModel):
                try:
                    metrics = model.evaluate(X_val, y_val)
                    score = metrics['accuracy']
                    
                    if score > best_score:
                        best_score = score
                        best_model = model
                        logger.info(f"New best model: {name} with accuracy {score:.4f}")
                except Exception as e:
                    logger.warning(f"Could not evaluate {name}: {e}")
        
        return best_model
    
    def save_all_models(self, directory: str):
        """Save all trained models"""
        os.makedirs(directory, exist_ok=True)
        
        for name, model in self.models.items():
            filepath = os.path.join(directory, f"{name}.pkl")
            try:
                if isinstance(model, AnomalyDetectionModel):
                    model.save(filepath)
                elif isinstance(model, SupervisedClassificationModel):
                    model.save(filepath)
            except Exception as e:
                logger.error(f"Error saving {name}: {e}")
    
    def load_model(self, filepath: str, model_type: str = 'anomaly') -> IntrusionDetectionModel:
        """Load a specific model"""
        if model_type == 'anomaly':
            model = AnomalyDetectionModel()
        else:
            model = SupervisedClassificationModel()
        
        model.load(filepath)
        return model


if __name__ == "__main__":
    # Test model training
    from data_collector import DataCollector
    from feature_engineering import DataPreprocessor
    
    # Collect sample data
    collector = DataCollector()
    raw_data = [collector.collect_all_data() for _ in range(100)]
    
    # Prepare features
    preprocessor = DataPreprocessor()
    X, y, feature_names = preprocessor.preprocess_for_training(raw_data)
    
    print(f"Training data shape: {X.shape}")
    
    # Train models
    trainer = ModelTrainer({'contamination': 0.1, 'n_estimators': 100})
    models = trainer.train_models(X)
    
    print(f"\nTrained {len(models)} models")
    
    # Test predictions
    if 'isolation_forest' in models:
        test_sample = X[0:1]
        prediction = models['isolation_forest'].predict(test_sample)
        print(f"\nTest prediction: {prediction[0]}")
