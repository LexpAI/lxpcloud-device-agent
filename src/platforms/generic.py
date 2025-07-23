import socket
import platform
import psutil
from typing import Dict, Any
import time

class GenericPlatform:
    """Generic platform implementation for any Python-capable device"""
    
    def __init__(self):
        self.system_info = self._get_system_info()
        
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'hostname': socket.gethostname()
        }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'network_io': psutil.net_io_counters()._asdict()
        }
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get network information"""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
        except:
            hostname = "unknown"
            ip_address = "0.0.0.0"
        
        return {
            'hostname': hostname,
            'ip_address': ip_address,
            'connection_type': 'ethernet'
        }
    
    def read_simulated_sensor(self, sensor_type: str) -> float:
        """Read simulated sensor data"""
        import random
        
        if sensor_type == 'temperature':
            # Simulate temperature between 20-30°C
            return 20.0 + random.uniform(0, 10)
        elif sensor_type == 'humidity':
            # Simulate humidity between 40-60%
            return 40.0 + random.uniform(0, 20)
        elif sensor_type == 'pressure':
            # Simulate atmospheric pressure around 1013 hPa
            return 1013.0 + random.uniform(-10, 10)
        else:
            return 0.0
    
    def get_location_info(self) -> Dict[str, Any]:
        """Get location information (default to Istanbul)"""
        return {
            'latitude': 41.0082,
            'longitude': 28.9784,
            'altitude': 100
        }
    
    def get_environment_info(self) -> Dict[str, Any]:
        """Get environmental information"""
        return {
            'ambient_temperature': 22.0,
            'ambient_humidity': 45.0
        }
    
    def is_online(self) -> bool:
        """Check if device is online"""
        try:
            # Try to connect to a reliable host
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False 