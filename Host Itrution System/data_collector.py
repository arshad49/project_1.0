"""
Data Collection Module - Collects system metrics, logs, and process information
"""
import psutil
import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCollector:
    """Collects system data for intrusion detection"""
    
    def __init__(self):
        self.start_time = datetime.now()
        
    def collect_system_metrics(self) -> Dict[str, float]:
        """Collect real-time system metrics"""
        try:
            metrics = {
                'timestamp': datetime.now().timestamp(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage_percent': psutil.disk_usage('/').percent,
                'num_processes': len(psutil.pids()),
                'cpu_count': psutil.cpu_count(),
                'boot_time': psutil.boot_time()
            }
            
            # Get per-CPU usage
            cpu_percpu = psutil.cpu_percent(interval=1, percpu=True)
            metrics['cpu_max'] = max(cpu_percpu) if cpu_percpu else 0
            metrics['cpu_min'] = min(cpu_percpu) if cpu_percpu else 0
            metrics['cpu_avg'] = sum(cpu_percpu) / len(cpu_percpu) if cpu_percpu else 0
            
            return metrics
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return {}
    
    def collect_network_metrics(self) -> Dict[str, Any]:
        """Collect network-related metrics"""
        try:
            net_io = psutil.net_io_counters()
            
            # Try to get connections (may require elevated permissions on macOS)
            try:
                net_connections = psutil.net_connections(kind='inet')
                num_connections = len(net_connections)
                
                # Count connections by status
                connections_by_status = {}
                for conn in net_connections:
                    status = conn.status
                    connections_by_status[status] = connections_by_status.get(status, 0) + 1
            except (psutil.AccessDenied, PermissionError):
                num_connections = 0
                connections_by_status = {}
            
            # Get network interface statistics
            try:
                net_if_stats = psutil.net_if_stats()
                network_interfaces = len(net_if_stats)
            except:
                network_interfaces = 0
            
            metrics = {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'num_connections': num_connections,
                'connections_by_status': connections_by_status,
                'network_interfaces': network_interfaces
            }
            
            return metrics
        except Exception as e:
            # Silently return empty dict on errors
            return {}
    
    def collect_process_info(self) -> List[Dict[str, Any]]:
        """Collect information about running processes"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 
                                            'memory_percent', 'status', 'create_time']):
                try:
                    pinfo = proc.info
                    pinfo['cpu_percent'] = proc.cpu_percent(interval=0.1)
                    pinfo['memory_percent'] = proc.memory_percent()
                    processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Aggregate statistics
            process_stats = {
                'total_processes': len(processes),
                'unique_users': len(set(p.get('username', 'unknown') for p in processes)),
                'zombie_processes': sum(1 for p in processes if p.get('status') == psutil.STATUS_ZOMBIE),
                'high_cpu_processes': sum(1 for p in processes if p.get('cpu_percent', 0) > 50),
                'high_memory_processes': sum(1 for p in processes if p.get('memory_percent', 0) > 50)
            }
            
            return processes, process_stats
        except Exception as e:
            logger.error(f"Error collecting process info: {e}")
            return [], {}
    
    def collect_user_activity(self) -> Dict[str, Any]:
        """Collect user activity metrics"""
        try:
            users = psutil.users()
            
            user_activity = {
                'active_users': len(users),
                'user_names': [u.name for u in users],
                'login_times': [u.started for u in users],
                'unique_terminals': len(set(u.terminal for u in users))
            }
            
            return user_activity
        except Exception as e:
            logger.error(f"Error collecting user activity: {e}")
            return {}
    
    def parse_auth_log(self, log_file: str = '/var/log/auth.log') -> Dict[str, int]:
        """Parse authentication logs for security events"""
        auth_events = {
            'failed_logins': 0,
            'successful_logins': 0,
            'sudo_attempts': 0,
            'ssh_connections': 0,
            'invalid_users': 0
        }
        
        try:
            if not os.path.exists(log_file):
                # Try macOS-specific log location
                if sys.platform == 'darwin':
                    # macOS uses unified logging, skip file-based logs
                    return auth_events
                return auth_events
            
            with open(log_file, 'r') as f:
                lines = f.readlines()[-1000:]  # Last 1000 lines
                
                for line in lines:
                    if 'Failed password' in line or 'authentication failure' in line:
                        auth_events['failed_logins'] += 1
                    elif 'Accepted password' in line or 'session opened' in line:
                        auth_events['successful_logins'] += 1
                    elif 'sudo' in line:
                        auth_events['sudo_attempts'] += 1
                    elif 'sshd' in line and 'connection' in line.lower():
                        auth_events['ssh_connections'] += 1
                    elif 'Invalid user' in line:
                        auth_events['invalid_users'] += 1
                        
        except Exception as e:
            logger.error(f"Error parsing auth log: {e}")
        
        return auth_events
    
    def collect_file_system_metrics(self) -> Dict[str, Any]:
        """Collect file system related metrics"""
        try:
            partitions = psutil.disk_partitions()
            
            fs_metrics = {
                'partitions': len(partitions),
                'mount_points': [p.mountpoint for p in partitions],
                'total_disk_usage': 0,
                'io_counters': {}
            }
            
            # Get disk I/O statistics
            try:
                disk_io = psutil.disk_io_counters()
                fs_metrics['io_counters'] = {
                    'read_count': disk_io.read_count,
                    'write_count': disk_io.write_count,
                    'read_bytes': disk_io.read_bytes,
                    'write_bytes': disk_io.write_bytes
                }
            except:
                pass
            
            return fs_metrics
        except Exception as e:
            logger.error(f"Error collecting file system metrics: {e}")
            return {}
    
    def collect_all_data(self) -> Dict[str, Any]:
        """Collect all system data in one call"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'system_metrics': self.collect_system_metrics(),
            'network_metrics': self.collect_network_metrics(),
            'process_info': self.collect_process_info(),
            'user_activity': self.collect_user_activity(),
            'file_system_metrics': self.collect_file_system_metrics()
        }
        
        # Try to collect auth log data (may require sudo)
        try:
            data['auth_events'] = self.parse_auth_log()
        except:
            data['auth_events'] = {}
        
        return data


if __name__ == "__main__":
    # Test data collection
    collector = DataCollector()
    data = collector.collect_all_data()
    
    print("=== System Metrics ===")
    print(data['system_metrics'])
    print("\n=== Network Metrics ===")
    print(data['network_metrics'])
    print("\n=== Process Stats ===")
    if data['process_info']:
        print(data['process_info'][1])
