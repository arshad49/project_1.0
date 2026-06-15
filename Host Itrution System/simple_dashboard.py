#!/usr/bin/env python3
"""
Simple Dashboard - Standalone HIDS monitor with embedded HTML
No template files needed - everything in one file!
"""
import os
import sys
from flask import Flask, jsonify, request
from datetime import datetime
import threading
import time
import numpy as np
import pandas as pd
# Import HIDS components
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import Config
from data_collector import DataCollector
from feature_engineering import DataPreprocessor
from ml_models import AnomalyDetectionModel

app = Flask(__name__)

# Global state
config = Config()
collector = DataCollector()
preprocessor = DataPreprocessor()
model = None
is_running = False
current_metrics = {}
recent_alerts = []
anomaly_history = []


def load_or_train_model():
    """Load existing model or train a quick baseline"""
    global model
    
    model_path = os.path.join(config.MODEL_DIR, 'baseline_model.pkl')
    
    if os.path.exists(model_path):
        print(f"✓ Loading existing model from {model_path}")
        model = AnomalyDetectionModel()
        model.load(model_path)
        return True
    
    # Train minimal baseline
    print("⚠️  No model found. Training minimal baseline (5 samples)...")
    baseline_data = []
    
    for i in range(5):
        data = collector.collect_all_data()
        baseline_data.append(data)
        print(f"  Collected sample {i+1}/5")
        time.sleep(0.5)
    
    X, _, _ = preprocessor.preprocess_for_training(baseline_data)
    
    if len(X) > 0:
        model = AnomalyDetectionModel(contamination=0.1, n_estimators=50)
        model.train(X)
        model.save(model_path)
        print("✓ Model trained and saved!")
        return True
    
    return False


def monitoring_loop():
    """Background monitoring loop"""
    global is_running, current_metrics, recent_alerts, anomaly_history
    
    while is_running:
        try:
            # Collect metrics
            data = collector.collect_all_data()
            metrics = data.get('system_metrics', {})
            
            # Check for anomalies if model loaded
            anomaly_score = 0.0
            if model:
                X, _ = preprocessor.preprocess_for_inference(data)
                if len(X) > 0:
                    prediction = model.predict(X)[0]
                    anomaly_score = model.predict_proba(X)[0]
                    
                    if prediction == 1 and anomaly_score > 0.7:
                        alert = {
                            'timestamp': datetime.now().isoformat(),
                            'severity': 'HIGH' if anomaly_score > 0.9 else 'MEDIUM',
                            'message': f'Anomaly detected (score: {anomaly_score:.4f})',
                            'score': anomaly_score
                        }
                        recent_alerts.append(alert)
                        if len(recent_alerts) > 50:
                            recent_alerts = recent_alerts[-50:]
                        print(f"⚠️  ALERT: {alert['message']}")
            
            # Update current metrics
            current_metrics = {
                'cpu_percent': metrics.get('cpu_percent', 0),
                'memory_percent': metrics.get('memory_percent', 0),
                'num_processes': metrics.get('num_processes', 0),
                'disk_usage_percent': metrics.get('disk_usage_percent', 0),
                'anomaly_score': anomaly_score
            }
            
            # Update history
            anomaly_history.append({
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'score': round(anomaly_score, 4)
            })
            if len(anomaly_history) > 50:
                anomaly_history = anomaly_history[-50:]
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Error in monitoring: {e}")
            time.sleep(2)


@app.route('/')
def dashboard():
    """Main dashboard with embedded HTML"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HIDS Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        header {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        h1 { color: #667eea; margin-bottom: 10px; }
        .status-bar { display: flex; gap: 20px; align-items: center; flex-wrap: wrap; }
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 20px;
            background: #f0f0f0;
            border-radius: 5px;
        }
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        .status-dot.running { background: #4CAF50; }
        .status-dot.stopped { background: #f44336; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
        }
        .btn-primary { background: #667eea; color: white; }
        .btn-primary:hover { background: #5568d3; }
        .btn-danger { background: #f44336; color: white; }
        .btn-danger:hover { background: #da190b; }
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .card h2 { color: #667eea; margin-bottom: 15px; font-size: 1.2em; }
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .metric:last-child { border-bottom: none; }
        .metric-label { color: #666; }
        .metric-value { font-weight: bold; color: #333; }
        .metric-value.high { color: #f44336; }
        .metric-value.warning { color: #ff9800; }
        .metric-value.normal { color: #4CAF50; }
        .chart-container { position: relative; height: 300px; }
        .alerts-container { max-height: 400px; overflow-y: auto; }
        .alert-item {
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid;
        }
        .alert-high { background: #fff3e0; border-color: #ff9800; }
        .alert-medium { background: #fff8e1; border-color: #ffeb3b; }
        footer {
            text-align: center;
            color: white;
            margin-top: 20px;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛡️ Host Intrusion Detection System</h1>
            <div class="status-bar">
                <div class="status-indicator">
                    <span class="status-dot" id="statusDot"></span>
                    <span id="statusText">Checking...</span>
                </div>
                <button class="btn btn-primary" onclick="startMonitoring()">Start</button>
                <button class="btn btn-danger" onclick="stopMonitoring()">Stop</button>
                <button class="btn btn-primary" onclick="refreshData()">Refresh</button>
            </div>
        </header>

        <div class="dashboard-grid">
            <div class="card">
                <h2>System Metrics</h2>
                <div class="metric">
                    <span class="metric-label">CPU Usage:</span>
                    <span class="metric-value" id="cpuUsage">--</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Memory Usage:</span>
                    <span class="metric-value" id="memoryUsage">--</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Active Processes:</span>
                    <span class="metric-value" id="processCount">--</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Disk Usage:</span>
                    <span class="metric-value" id="diskUsage">--</span>
                </div>
            </div>

            <div class="card">
                <h2>Anomaly Score Trend</h2>
                <div class="chart-container">
                    <canvas id="anomalyChart"></canvas>
                </div>
            </div>

            <div class="card">
                <h2>CPU & Memory Usage</h2>
                <div class="chart-container">
                    <canvas id="resourceChart"></canvas>
                </div>
            </div>

            <div class="card">
                <h2>Recent Alerts</h2>
                <div class="alerts-container" id="alertsList">
                    <p style="text-align: center; color: #999;">No alerts yet</p>
                </div>
            </div>
        </div>

        <footer>
            <p>Host Intrusion Detection System v1.0</p>
            <p>Last update: <span id="lastUpdate">--</span></p>
        </footer>
    </div>

    <script>
        let anomalyChart, resourceChart;
        
        function initCharts() {
            // Anomaly Score Chart
            const anomalyCtx = document.getElementById('anomalyChart').getContext('2d');
            anomalyChart = new Chart(anomalyCtx, {
                type: 'line',
                data: { labels: [], datasets: [{
                    label: 'Anomaly Score',
                    data: [],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }]},
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { beginAtZero: true, max: 1 } }
                }
            });
            
            // CPU & Memory Chart
            const resourceCtx = document.getElementById('resourceChart').getContext('2d');
            resourceChart = new Chart(resourceCtx, {
                type: 'line',
                data: { 
                    labels: [], 
                    datasets: [
                        {
                            label: 'CPU %',
                            data: [],
                            borderColor: '#f44336',
                            backgroundColor: 'rgba(244, 67, 54, 0.1)',
                            tension: 0.4,
                            fill: true
                        },
                        {
                            label: 'Memory %',
                            data: [],
                            borderColor: '#4CAF50',
                            backgroundColor: 'rgba(76, 175, 80, 0.1)',
                            tension: 0.4,
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { beginAtZero: true, max: 100 } }
                }
            });
        }

        async function refreshData() {
            try {
                const statusResponse = await fetch('/api/status');
                const status = await statusResponse.json();
                
                document.getElementById('statusText').textContent = 
                    status.status === 'running' ? 'Monitoring Active' : 'Stopped';
                document.getElementById('statusDot').className = 
                    'status-dot ' + (status.status === 'running' ? 'running' : 'stopped');
                
                const metricsResponse = await fetch('/api/metrics');
                const metrics = await metricsResponse.json();
                
                updateMetrics(metrics);
                updateCharts(metrics);
                
                const alertsResponse = await fetch('/api/alerts?limit=10');
                const alerts = await alertsResponse.json();
                updateAlerts(alerts);
                
                document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();
                
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }

        function updateMetrics(metrics) {
            document.getElementById('cpuUsage').textContent = (metrics.cpu_percent || 0).toFixed(1) + '%';
            document.getElementById('memoryUsage').textContent = (metrics.memory_percent || 0).toFixed(1) + '%';
            document.getElementById('processCount').textContent = metrics.num_processes || 0;
            document.getElementById('diskUsage').textContent = (metrics.disk_usage_percent || 0).toFixed(1) + '%';
        }

        function updateCharts(metrics) {
            const now = new Date().toLocaleTimeString();
            
            // Update Anomaly Chart
            if (anomalyChart.data.labels.length > 20) {
                anomalyChart.data.labels.shift();
                anomalyChart.data.datasets[0].data.shift();
            }
            anomalyChart.data.labels.push(now);
            anomalyChart.data.datasets[0].data.push(metrics.anomaly_score || 0);
            anomalyChart.update();
            
            // Update Resource Chart
            if (resourceChart.data.labels.length > 20) {
                resourceChart.data.labels.shift();
                resourceChart.data.datasets[0].data.shift();
                resourceChart.data.datasets[1].data.shift();
            }
            resourceChart.data.labels.push(now);
            resourceChart.data.datasets[0].data.push(metrics.cpu_percent || 0);
            resourceChart.data.datasets[1].data.push(metrics.memory_percent || 0);
            resourceChart.update();
        }

        function updateAlerts(alerts) {
            const container = document.getElementById('alertsList');
            if (alerts.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #999;">No alerts yet</p>';
                return;
            }
            container.innerHTML = '';
            alerts.reverse().forEach(alert => {
                const alertEl = document.createElement('div');
                alertEl.className = 'alert-item alert-' + (alert.severity || 'medium').toLowerCase();
                alertEl.innerHTML = '<strong>' + (alert.severity || 'INFO') + '</strong>: ' + 
                                   (alert.message || 'Unknown alert') + '<br>' +
                                   '<small>' + new Date(alert.timestamp).toLocaleString() + '</small>';
                container.appendChild(alertEl);
            });
        }

        async function startMonitoring() {
            await fetch('/api/start', { method: 'POST' });
            refreshData();
        }

        async function stopMonitoring() {
            await fetch('/api/stop', { method: 'POST' });
            refreshData();
        }

        document.addEventListener('DOMContentLoaded', () => {
            initCharts();
            refreshData();
            setInterval(refreshData, 5000);
        });
    </script>
</body>
</html>'''


@app.route('/api/status')
def get_status():
    """Get current status"""
    return jsonify({
        'status': 'running' if is_running else 'stopped',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': model is not None,
        'alerts_count': len(recent_alerts)
    })


@app.route('/api/metrics')
def get_metrics():
    """Get real-time metrics"""
    return jsonify({
        'cpu_percent': current_metrics.get('cpu_percent', 0),
        'memory_percent': current_metrics.get('memory_percent', 0),
        'num_processes': current_metrics.get('num_processes', 0),
        'disk_usage_percent': current_metrics.get('disk_usage_percent', 0),
        'anomaly_score': current_metrics.get('anomaly_score', 0)
    })


@app.route('/api/alerts')
def get_alerts():
    """Get recent alerts"""
    limit = request.args.get('limit', 20, type=int)
    return jsonify(recent_alerts[-limit:])


@app.route('/api/anomaly_scores')
def get_anomaly_scores():
    """Get anomaly score history"""
    return jsonify(anomaly_history)


@app.route('/api/start', methods=['POST'])
def start_monitoring():
    """Start monitoring"""
    global is_running
    if not is_running:
        is_running = True
        thread = threading.Thread(target=monitoring_loop, daemon=True)
        thread.start()
    return jsonify({'status': 'started'})


@app.route('/api/stop', methods=['POST'])
def stop_monitoring():
    """Stop monitoring"""
    global is_running
    is_running = False
    return jsonify({'status': 'stopped'})


if __name__ == '__main__':
    print("=" * 60)
    print("   HIDS DASHBOARD - SIMPLE MODE")
    print("=" * 60)
    print()
    
    # Load or train model
    load_or_train_model()
    
    print()
    print("Starting web dashboard...")
    print("Open your browser to: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    # Start monitoring
    is_running = True
    monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
    monitor_thread.start()
    
    # Run Flask app
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
