#!/usr/bin/env python3
"""
Main Entry Point for Host Intrusion Detection System
Provides CLI interface for all system functions
"""
import argparse
import sys
import time
import signal
import os
from datetime import datetime

from config import Config
from monitor import IntrusionDetector, RealTimeMonitor
from data_collector import DataCollector
from ml_models import ModelTrainer
from alert_system import AlertManager, AlertDashboard


class HIDSCLI:
    """Command-line interface for the intrusion detection system"""
    
    def __init__(self):
        self.config = Config()
        self.detector = None
        self.running = False
        
    def setup_signal_handlers(self):
        """Setup graceful shutdown handlers"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n\nShutting down gracefully...")
        self.running = False
        if self.detector:
            self.detector.stop_monitoring()
        sys.exit(0)
    
    def train_model(self, args):
        """Train intrusion detection model"""
        print("=== Training Host Intrusion Detection Model ===\n")
        
        self.detector = IntrusionDetector(self.config)
        
        print(f"Configuration:")
        print(f"  - Model Type: {self.config.MODEL_TYPE}")
        print(f"  - Training Size: {self.config.TRAINING_SIZE}")
        print(f"  - Contamination: {self.config.CONTAMINATION}")
        print(f"  - Estimators: {self.config.N_ESTIMATORS}\n")
        
        print("Starting training process...")
        self.detector.train()
        
        print("\n✓ Training completed successfully!")
        print(f"Models saved to: {self.config.MODEL_DIR}")
    
    def start_monitoring(self, args):
        """Start real-time monitoring"""
        print("=== Starting Real-Time Monitoring ===\n")
        
        # Check if model exists
        import os
        model_path = os.path.join(self.config.MODEL_DIR, 'baseline_model.pkl')
        
        if not os.path.exists(model_path):
            print("⚠️  No trained model found. Training new model first...")
            self.train_model(args)
        
        self.detector = IntrusionDetector(self.config)
        self.detector.start_monitoring()
        
        print("✓ Monitoring started successfully!")
        print("Press Ctrl+C to stop\n")
        
        self.setup_signal_handlers()
        self.running = True
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.detector.stop_monitoring()
    
    def collect_data(self, args):
        """Collect system data for analysis"""
        print("=== Collecting System Data ===\n")
        
        collector = DataCollector()
        
        print(f"Collecting {args.samples} samples with {args.interval}s interval...\n")
        
        samples = []
        for i in range(args.samples):
            data = collector.collect_all_data()
            samples.append(data)
            
            print(f"[{i+1}/{args.samples}] Collected sample at {datetime.now().strftime('%H:%M:%S')}")
            
            if i < args.samples - 1:
                time.sleep(args.interval)
        
        # Save collected data
        import json
        output_file = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path = os.path.join(self.config.DATA_DIR, output_file)
        
        with open(output_path, 'w') as f:
            json.dump(samples, f, indent=2, default=str)
        
        print(f"\n✓ Data collection completed!")
        print(f"Saved to: {output_path}")
    
    def show_status(self, args):
        """Show current system status"""
        print("=== Host Intrusion Detection System Status ===\n")
        
        # Check model status
        import os
        model_files = []
        if os.path.exists(self.config.MODEL_DIR):
            model_files = [f for f in os.listdir(self.config.MODEL_DIR) if f.endswith('.pkl')]
        
        print("Model Status:")
        if model_files:
            print(f"  ✓ Found {len(model_files)} model(s)")
            for f in model_files:
                print(f"    - {f}")
        else:
            print("  ⚠️  No trained models found")
        
        # Show recent alerts
        alert_manager = AlertManager(self.config.ALERTS_DIR)
        stats = alert_manager.get_alert_statistics(hours=24)
        
        print(f"\nAlert Statistics (Last 24 hours):")
        print(f"  Total Alerts: {stats['total_alerts']}")
        print(f"  Unacknowledged: {stats['unacknowledged']}")
        
        if 'by_severity' in stats:
            print("  By Severity:")
            for severity, count in stats['by_severity'].items():
                print(f"    {severity}: {count}")
        
        # Show current metrics
        print("\nCurrent System Metrics:")
        collector = DataCollector()
        metrics = collector.collect_system_metrics()
        
        print(f"  CPU Usage: {metrics.get('cpu_percent', 'N/A')}%")
        print(f"  Memory Usage: {metrics.get('memory_percent', 'N/A')}%")
        print(f"  Active Processes: {metrics.get('num_processes', 'N/A')}")
        
        print(f"\nConfiguration:")
        print(f"  Model Directory: {self.config.MODEL_DIR}")
        print(f"  Data Directory: {self.config.DATA_DIR}")
        print(f"  Logs Directory: {self.config.LOGS_DIR}")
        print(f"  Alerts Directory: {self.config.ALERTS_DIR}")
    
    def analyze_data(self, args):
        """Analyze collected data for anomalies"""
        print("=== Analyzing Data for Anomalies ===\n")
        
        import json
        
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            return
        
        with open(args.file, 'r') as f:
            data = json.load(f)
        
        print(f"Loaded {len(data)} samples from {args.file}\n")
        
        # Load model
        model_path = os.path.join(self.config.MODEL_DIR, 'baseline_model.pkl')
        
        if not os.path.exists(model_path):
            print("⚠️  No trained model found. Please train a model first.")
            return
        
        from ml_models import AnomalyDetectionModel
        model = AnomalyDetectionModel()
        model.load(model_path)
        
        # Prepare features
        from feature_engineering import DataPreprocessor
        preprocessor = DataPreprocessor()
        
        X, _, feature_names = preprocessor.preprocess_for_training(data)
        
        # Make predictions
        predictions = model.predict(X)
        scores = model.predict_proba(X)
        
        # Show results
        anomaly_count = sum(predictions)
        print(f"Analysis Results:")
        print(f"  Total Samples: {len(data)}")
        print(f"  Anomalies Detected: {anomaly_count}")
        print(f"  Anomaly Rate: {(anomaly_count/len(data)*100):.2f}%\n")
        
        # Show anomalous samples
        if anomaly_count > 0:
            print("Anomalous Samples:")
            for i, (pred, score) in enumerate(zip(predictions, scores)):
                if pred == 1:
                    print(f"  Sample {i}: Score = {score:.4f}")
                    if i < len(data) and 'system_metrics' in data[i]:
                        metrics = data[i]['system_metrics']
                        print(f"    CPU: {metrics.get('cpu_percent', 'N/A')}%")
                        print(f"    Memory: {metrics.get('memory_percent', 'N/A')}%")
    
    def run_dashboard(self, args):
        """Run web dashboard"""
        print("=== Starting Web Dashboard ===\n")
        
        # Try to import Flask
        try:
            from dashboard_server import app, update_dashboard_data
            
            # Start monitor in background
            monitor = RealTimeMonitor(self.config)
            
            # Load model
            model_path = os.path.join(self.config.MODEL_DIR, 'baseline_model.pkl')
            if os.path.exists(model_path):
                monitor.load_model(model_path)
            else:
                print("⚠️  No model found. Training baseline model...")
                monitor.train_baseline_model()
            
            # Start monitoring
            monitor.start()
            
            # Add callback to update dashboard
            def dashboard_callback(alert):
                # This would need proper integration with Flask app
                pass
            
            monitor.add_callback(dashboard_callback)
            
            print("✓ Dashboard starting...")
            print("Open your browser to: http://localhost:5000")
            print("Press Ctrl+C to stop\n")
            
            app.run(debug=False, host='0.0.0.0', port=5000)
            
        except ImportError:
            print("Error: Flask is required for web dashboard")
            print("Install with: pip install flask")
    
    def quick_start(self, args):
        """Quick start with default settings"""
        print("=== Quick Start - Host Intrusion Detection System ===\n")
        
        # Train model
        print("Step 1: Training model...")
        self.train_model(args)
        
        print("\n" + "="*50 + "\n")
        
        # Start monitoring
        print("Step 2: Starting monitoring...")
        self.start_monitoring(args)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Host Intrusion Detection System using Machine Learning',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s train                    Train a new intrusion detection model
  %(prog)s monitor                  Start real-time monitoring
  %(prog)s status                   Show system status
  %(prog)s collect --samples 100    Collect 100 data samples
  %(prog)s analyze --file data.json Analyze data file for anomalies
  %(prog)s dashboard                Start web dashboard
  %(prog)s quickstart               Quick start with training and monitoring
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train intrusion detection model')
    train_parser.set_defaults(func=lambda args: hids.train_model(args))
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Start real-time monitoring')
    monitor_parser.set_defaults(func=lambda args: hids.start_monitoring(args))
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show system status')
    status_parser.set_defaults(func=lambda args: hids.show_status(args))
    
    # Collect command
    collect_parser = subparsers.add_parser('collect', help='Collect system data')
    collect_parser.add_argument('--samples', type=int, default=50, help='Number of samples to collect')
    collect_parser.add_argument('--interval', type=float, default=1.0, help='Interval between samples (seconds)')
    collect_parser.set_defaults(func=lambda args: hids.collect_data(args))
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze data for anomalies')
    analyze_parser.add_argument('--file', type=str, required=True, help='Data file to analyze')
    analyze_parser.set_defaults(func=lambda args: hids.analyze_data(args))
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Start web dashboard')
    dashboard_parser.set_defaults(func=lambda args: hids.run_dashboard(args))
    
    # Quick start command
    quickstart_parser = subparsers.add_parser('quickstart', help='Quick start with defaults')
    quickstart_parser.set_defaults(func=lambda args: hids.quick_start(args))
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    hids = HIDSCLI()
    args.func(args)


if __name__ == "__main__":
    main()
