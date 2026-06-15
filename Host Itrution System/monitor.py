"""
Real-time Monitoring Engine - Continuously monitors system and detects intrusions
"""
import time
import threading
import json
import os
import numpy as np
from datetime import datetime
from typing import Dict, List, Callable, Optional
import logging

from data_collector import DataCollector
from feature_engineering import DataPreprocessor
from ml_models import AnomalyDetectionModel, HybridIntrusionDetection, ModelTrainer
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RealTimeMonitor:
    """Real-time system monitoring with intrusion detection"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.data_collector = DataCollector()
        self.preprocessor = DataPreprocessor()
        self.model = None
        self.is_running = False
        self.monitor_thread = None
        self.callbacks = []
        self.alert_history = []
        self.baseline_data = []
        
    def load_model(self, model_path: str):
        """Load trained model"""
        try:
            if os.path.exists(model_path):
                self.model = AnomalyDetectionModel()
                self.model.load(model_path)
                logger.info(f"Model loaded from {model_path}")
            else:
                logger.warning(f"Model not found at {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
    
    def train_baseline_model(self, training_data: List[Dict] = None):
        """Train initial baseline model"""
        try:
            if training_data is None:
                # Collect baseline data (reduced for faster startup)
                logger.info("Collecting baseline data...")
                training_data = []
                for i in range(20):  # Collect 20 samples (faster startup)
                    data = self.data_collector.collect_all_data()
                    training_data.append(data)
                    time.sleep(0.5)  # Reduced sleep
                    if i % 5 == 0:
                        logger.info(f"Collected {i+1}/20 baseline samples")
            
            self.baseline_data = training_data
            
            # Prepare features
            X, _, _ = self.preprocessor.preprocess_for_training(training_data)
            
            if len(X) > 0:
                # Train model
                self.model = AnomalyDetectionModel(
                    contamination=self.config.CONTAMINATION,
                    n_estimators=self.config.N_ESTIMATORS
                )
                self.model.train(X)
                logger.info("Baseline model trained successfully")
                
                # Save model
                model_path = os.path.join(self.config.MODEL_DIR, 'baseline_model.pkl')
                self.model.save(model_path)
                
        except Exception as e:
            logger.error(f"Error training baseline model: {e}")
    
    def add_callback(self, callback: Callable):
        """Add callback function for alerts"""
        self.callbacks.append(callback)
    
    def check_anomaly(self, data: Dict) -> Dict:
        """Check if current data indicates an anomaly"""
        try:
            if self.model is None:
                return {'is_anomaly': False, 'score': 0.0, 'message': 'No model loaded'}
            
            # Preprocess data
            X, _ = self.preprocessor.preprocess_for_inference(data)
            
            if len(X) == 0:
                return {'is_anomaly': False, 'score': 0.0, 'message': 'Feature extraction failed'}
            
            # Get prediction
            prediction = self.model.predict(X)[0]
            score = self.model.predict_proba(X)[0]
            
            is_anomaly = prediction == 1
            
            result = {
                'is_anomaly': is_anomaly,
                'score': float(score),
                'timestamp': datetime.now().isoformat(),
                'message': 'Anomaly detected' if is_anomaly else 'Normal activity'
            }
            
            if is_anomaly and score >= self.config.ALERT_THRESHOLD:
                self.handle_alert(result, data)
            
            return result
            
        except Exception as e:
            logger.error(f"Error checking anomaly: {e}")
            return {'is_anomaly': False, 'score': 0.0, 'message': f'Error: {str(e)}'}
    
    def handle_alert(self, result: Dict, raw_data: Dict):
        """Handle detected anomaly"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'severity': 'HIGH' if result['score'] >= 0.9 else 'MEDIUM',
            'score': result['score'],
            'message': result['message'],
            'system_metrics': raw_data.get('system_metrics', {}),
            'network_metrics': raw_data.get('network_metrics', {})
        }
        
        self.alert_history.append(alert)
        
        # Keep only last 1000 alerts
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]
        
        # Log alert
        logger.warning(f"ALERT: {alert['severity']} - {alert['message']} (Score: {alert['score']:.4f})")
        
        # Save alert to file
        self.save_alert(alert)
        
        # Call registered callbacks
        for callback in self.callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Error in callback: {e}")
    
    def save_alert(self, alert: Dict):
        """Save alert to file"""
        try:
            date_str = datetime.now().strftime('%Y-%m-%d')
            alert_file = os.path.join(self.config.ALERTS_DIR, f"alerts_{date_str}.json")
            
            alerts = []
            if os.path.exists(alert_file):
                with open(alert_file, 'r') as f:
                    alerts = json.load(f)
            
            alerts.append(alert)
            
            with open(alert_file, 'w') as f:
                json.dump(alerts, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving alert: {e}")
    
    def monitoring_loop(self):
        """Main monitoring loop"""
        logger.info("Starting real-time monitoring...")
        
        while self.is_running:
            try:
                # Collect data
                data = self.data_collector.collect_all_data()
                
                # Check for anomalies
                result = self.check_anomaly(data)
                
                if self.config.VERBOSE:
                    status = "⚠️ ANOMALY" if result['is_anomaly'] else "✓ Normal"
                    logger.info(f"[{datetime.now().strftime('%H:%M:%S')}] {status} " +
                               f"(Score: {result['score']:.4f})")
                
                # Save logs if enabled
                if self.config.SAVE_LOGS:
                    self.save_monitoring_log(data, result)
                
                # Wait for next iteration
                time.sleep(self.config.COLLECTION_INTERVAL)
                
            except KeyboardInterrupt:
                logger.info("Monitoring interrupted by user")
                self.stop()
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.config.COLLECTION_INTERVAL)
    
    def save_monitoring_log(self, data: Dict, result: Dict):
        """Save monitoring log"""
        try:
            date_str = datetime.now().strftime('%Y-%m-%d')
            log_file = os.path.join(self.config.LOGS_DIR, f"monitor_{date_str}.log")
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'data': data,
                'result': result
            }
            
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            logger.error(f"Error saving log: {e}")
    
    def start(self):
        """Start monitoring in background thread"""
        if self.is_running:
            logger.warning("Monitoring already running")
            return
        
        self.is_running = True
        self.monitor_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Monitoring started")
    
    def stop(self):
        """Stop monitoring"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Monitoring stopped")
    
    def get_status(self) -> Dict:
        """Get current monitoring status"""
        return {
            'is_running': self.is_running,
            'model_loaded': self.model is not None,
            'total_alerts': len(self.alert_history),
            'baseline_samples': len(self.baseline_data),
            'recent_alerts': self.alert_history[-10:] if self.alert_history else []
        }


class IntrusionDetector:
    """Main intrusion detector class with training and inference capabilities"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.monitor = RealTimeMonitor(config)
        self.trainer = ModelTrainer({
            'contamination': self.config.CONTAMINATION,
            'n_estimators': self.config.N_ESTIMATORS
        })
        
    def train(self, data: List[Dict] = None, labels: np.ndarray = None):
        """Train the intrusion detection system"""
        logger.info("=== Training Intrusion Detection System ===")
        
        # Collect data if not provided
        if data is None:
            logger.info("Collecting training data...")
            data = []
            labels = []
            
            # Collect normal behavior samples
            for i in range(self.config.TRAINING_SIZE // 2):
                data_point = self.monitor.data_collector.collect_all_data()
                data.append(data_point)
                labels.append(0)  # Normal
                
                if i % 100 == 0:
                    logger.info(f"Collected {i} normal samples")
                
                time.sleep(0.1)
            
            # Simulate some anomalous samples (for demonstration)
            for i in range(self.config.TRAINING_SIZE // 2):
                data_point = self.monitor.data_collector.collect_all_data()
                # Add artificial anomalies
                if 'system_metrics' in data_point:
                    data_point['system_metrics']['cpu_percent'] = 95 + np.random.random() * 5
                    data_point['system_metrics']['memory_percent'] = 90 + np.random.random() * 10
                
                data.append(data_point)
                labels.append(1)  # Anomalous
                
                if i % 100 == 0:
                    logger.info(f"Created {i} anomalous samples")
        
        logger.info(f"Total training samples: {len(data)}")
        
        # Split data
        split_idx = int(len(data) * (1 - self.config.VALIDATION_SPLIT))
        train_data = data[:split_idx]
        val_data = data[split_idx:]
        
        if labels:
            train_labels = labels[:split_idx]
            val_labels = labels[split_idx:]
        else:
            train_labels = None
            val_labels = None
        
        # Train models
        X_train, y_train, feature_names = self.monitor.preprocessor.preprocess_for_training(
            train_data, train_labels
        )
        
        X_val, _, _ = self.monitor.preprocessor.preprocess_for_training(val_data)
        
        # Train multiple models
        models = self.trainer.train_models(X_train, y_train, X_val, val_labels)
        
        # Select best model
        if val_labels:
            best_model = self.trainer.select_best_model(X_val, val_labels)
            if best_model:
                self.monitor.model = best_model
                logger.info("Best model selected and loaded")
        else:
            # Use anomaly detection model
            self.monitor.model = models.get('isolation_forest')
        
        # Save all models
        self.trainer.save_all_models(self.config.MODEL_DIR)
        
        logger.info("Training completed")
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        # Load latest model
        model_path = os.path.join(self.config.MODEL_DIR, 'baseline_model.pkl')
        self.monitor.load_model(model_path)
        
        # Start monitoring
        self.monitor.start()
        logger.info("Real-time monitoring started")
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.monitor.stop()
        logger.info("Real-time monitoring stopped")
    
    def get_current_status(self) -> Dict:
        """Get current system status"""
        return self.monitor.get_status()


if __name__ == "__main__":
    # Example usage
    print("=== Host Intrusion Detection System ===\n")
    
    # Create detector
    detector = IntrusionDetector()
    
    # Option 1: Train new model
    print("\n1. Training new model...")
    detector.train()
    
    # Option 2: Start monitoring
    print("\n2. Starting real-time monitoring...")
    detector.start_monitoring()
    
    # Let it run for a while
    try:
        while True:
            time.sleep(5)
            status = detector.get_current_status()
            print(f"\nStatus: {status}")
    except KeyboardInterrupt:
        print("\n\nStopping...")
        detector.stop_monitoring()
