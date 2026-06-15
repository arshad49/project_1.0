"""
Alert System Module - Manages alerts and notifications
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Callable, Optional
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertManager:
    """Manages security alerts and notifications"""
    
    def __init__(self, alerts_dir: str = 'alerts'):
        self.alerts_dir = alerts_dir
        os.makedirs(alerts_dir, exist_ok=True)
        self.alert_handlers = []
        self.alert_history = []
        self.alert_counts = defaultdict(int)
        
    def register_handler(self, handler: Callable):
        """Register alert handler function"""
        self.alert_handlers.append(handler)
    
    def create_alert(self, severity: str, message: str, details: Dict = None) -> Dict:
        """Create a new alert"""
        alert = {
            'id': datetime.now().timestamp(),
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'message': message,
            'details': details or {},
            'acknowledged': False
        }
        
        self.alert_history.append(alert)
        self.alert_counts[severity] += 1
        
        # Notify all handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"Error in alert handler: {e}")
        
        # Log alert
        self.log_alert(alert)
        
        return alert
    
    def log_alert(self, alert: Dict):
        """Log alert to file"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        alert_file = os.path.join(self.alerts_dir, f"alerts_{date_str}.json")
        
        try:
            alerts = []
            if os.path.exists(alert_file):
                with open(alert_file, 'r') as f:
                    alerts = json.load(f)
            
            alerts.append(alert)
            
            with open(alert_file, 'w') as f:
                json.dump(alerts, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Error logging alert: {e}")
    
    def get_recent_alerts(self, limit: int = 50, severity: str = None) -> List[Dict]:
        """Get recent alerts"""
        if severity:
            filtered = [a for a in self.alert_history if a['severity'] == severity]
            return filtered[-limit:]
        return self.alert_history[-limit:]
    
    def get_alert_statistics(self, hours: int = 24) -> Dict:
        """Get alert statistics"""
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_alerts = [a for a in self.alert_history 
                        if datetime.fromisoformat(a['timestamp']) > cutoff]
        
        stats = {
            'total_alerts': len(recent_alerts),
            'by_severity': defaultdict(int),
            'unacknowledged': sum(1 for a in recent_alerts if not a['acknowledged'])
        }
        
        for alert in recent_alerts:
            stats['by_severity'][alert['severity']] += 1
        
        return dict(stats)
    
    def acknowledge_alert(self, alert_id: float):
        """Acknowledge an alert"""
        for alert in self.alert_history:
            if alert['id'] == alert_id:
                alert['acknowledged'] = True
                logger.info(f"Alert {alert_id} acknowledged")
                return True
        return False


class EmailNotifier:
    """Send email notifications for critical alerts"""
    
    def __init__(self, smtp_server: str, smtp_port: int, 
                 sender_email: str, sender_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        
    def send_alert_email(self, recipient: str, alert: Dict):
        """Send alert via email"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            subject = f"[HIDS ALERT] {alert['severity']} - {alert['message']}"
            
            body = f"""
Security Alert Detected

Severity: {alert['severity']}
Time: {alert['timestamp']}
Message: {alert['message']}

Details:
{json.dumps(alert['details'], indent=2)}

Please investigate immediately.

---
Host Intrusion Detection System
            """
            
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Alert email sent to {recipient}")
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")


class SlackNotifier:
    """Send notifications to Slack"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        
    def send_alert(self, alert: Dict):
        """Send alert to Slack channel"""
        try:
            import requests
            
            color_map = {
                'CRITICAL': '#ff0000',
                'HIGH': '#ff6600',
                'MEDIUM': '#ffcc00',
                'LOW': '#00ccff'
            }
            
            payload = {
                "attachments": [
                    {
                        "color": color_map.get(alert['severity'], '#808080'),
                        "title": f"🚨 Security Alert - {alert['severity']}",
                        "text": alert['message'],
                        "fields": [
                            {
                                "title": "Timestamp",
                                "value": alert['timestamp'],
                                "short": True
                            },
                            {
                                "title": "Score",
                                "value": str(alert['details'].get('score', 'N/A')),
                                "short": True
                            }
                        ],
                        "footer": "Host Intrusion Detection System"
                    }
                ]
            }
            
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            
            logger.info("Alert sent to Slack")
            
        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")


class AlertDashboard:
    """Simple console-based dashboard for alerts"""
    
    def __init__(self, alert_manager: AlertManager):
        self.alert_manager = alert_manager
        
    def display_summary(self):
        """Display alert summary in console"""
        os.system('clear' if os.name != 'nt' else 'cls')
        
        print("=" * 60)
        print("       HOST INTRUSION DETECTION SYSTEM - ALERTS")
        print("=" * 60)
        print(f"\nCurrent Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        stats = self.alert_manager.get_alert_statistics(hours=24)
        
        print("\n" + "-" * 60)
        print("ALERT STATISTICS (Last 24 hours)")
        print("-" * 60)
        print(f"Total Alerts: {stats['total_alerts']}")
        print(f"Unacknowledged: {stats['unacknowledged']}")
        print("\nBy Severity:")
        for severity, count in stats['by_severity'].items():
            print(f"  {severity}: {count}")
        
        print("\n" + "-" * 60)
        print("RECENT ALERTS")
        print("-" * 60)
        
        recent = self.alert_manager.get_recent_alerts(limit=10)
        
        if not recent:
            print("No recent alerts")
        else:
            for alert in reversed(recent):
                icon = "⚠️" if alert['severity'] in ['HIGH', 'CRITICAL'] else "ℹ️"
                ack = "✓" if alert['acknowledged'] else "✗"
                print(f"{icon} [{alert['severity']}] {alert['message']}")
                print(f"   Time: {alert['timestamp']} | Ack: {ack}")
                print()
        
        print("=" * 60)
        print("Press Ctrl+C to exit")


def alert_handler_example(alert: Dict):
    """Example alert handler"""
    print(f"\n🚨 ALERT RECEIVED: {alert['severity']} - {alert['message']}")


if __name__ == "__main__":
    # Test alert system
    manager = AlertManager()
    manager.register_handler(alert_handler_example)
    
    # Create test alerts
    manager.create_alert(
        severity='HIGH',
        message='Unusual network activity detected',
        details={'score': 0.92, 'type': 'network'}
    )
    
    manager.create_alert(
        severity='MEDIUM',
        message='High CPU usage anomaly',
        details={'score': 0.75, 'cpu_percent': 95}
    )
    
    # Display statistics
    stats = manager.get_alert_statistics()
    print(f"\nStatistics: {stats}")
