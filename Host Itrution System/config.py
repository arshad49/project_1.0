"""
Configuration settings for Host Intrusion Detection System
"""
import os

class Config:
    """Main configuration class"""
    
    # Data Collection Settings
    LOG_FILES = [
        '/var/log/auth.log',
        '/var/log/syslog',
        '/var/log/kern.log',
        '/var/log/secure'
    ]
    
    COLLECTION_INTERVAL = 5  # seconds
    BATCH_SIZE = 100
    
    # Feature Engineering Settings
    TIME_WINDOW = 300  # 5 minutes in seconds
    FEATURE_COLUMNS = [
        'cpu_percent',
        'memory_percent',
        'num_processes',
        'num_connections',
        'failed_login_attempts',
        'file_modifications',
        'process_spawn_rate',
        'network_packets_sent',
        'network_packets_received',
        'unique_users'
    ]
    
    # Model Settings
    MODEL_TYPE = 'isolation_forest'  # Options: isolation_forest, random_forest, svm
    CONTAMINATION = 0.1
    N_ESTIMATORS = 100
    RANDOM_STATE = 42
    
    # Threshold Settings
    ANOMALY_THRESHOLD = 0.6
    ALERT_THRESHOLD = 0.8
    
    # Storage Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(BASE_DIR, 'models')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    ALERTS_DIR = os.path.join(BASE_DIR, 'alerts')
    
    # Create directories if they don't exist
    for directory in [MODEL_DIR, DATA_DIR, LOGS_DIR, ALERTS_DIR]:
        os.makedirs(directory, exist_ok=True)
    
    # Alert Settings
    EMAIL_ALERTS = False
    EMAIL_RECIPIENT = 'admin@example.com'
    SLACK_WEBHOOK = None
    
    # Monitoring Settings
    MONITORING_ENABLED = True
    VERBOSE = True
    SAVE_LOGS = True
    
    # Training Settings
    TRAINING_SIZE = 10000
    VALIDATION_SPLIT = 0.2
    RETRAIN_INTERVAL = 86400  # 24 hours in seconds
