import asyncio
from typing import Dict, Any, List
from ..hardware.sensors import SensorInterface

class DataCollector:
    """Collects data from various sensors"""
    
    def __init__(self, sensor_config: Dict[str, Any]):
        self.sensor_config = sensor_config
        self.sensors = {}
        self._initialize_sensors()
    
    def _initialize_sensors(self):
        """Initialize sensors based on configuration"""
        for sensor_name, config in self.sensor_config.items():
            if config.get('enabled', False):
                sensor_type = config.get('type', 'generic')
                if sensor_type == 'temperature':
                    from ..hardware.sensors import TemperatureSensor
                    self.sensors[sensor_name] = TemperatureSensor(config)
                elif sensor_type == 'humidity':
                    from ..hardware.sensors import HumiditySensor
                    self.sensors[sensor_name] = HumiditySensor(config)
                else:
                    # Generic sensor
                    self.sensors[sensor_name] = SensorInterface(config)
    
    async def collect_all(self) -> Dict[str, Any]:
        """Collect data from all sensors"""
        data = {
            'sensors': {},
            'metrics': {},
            'alarms': [],
            'location': {},
            'environment': {},
            'network': {}
        }
        
        # Collect sensor data
        for sensor_name, sensor in self.sensors.items():
            try:
                sensor_data = await sensor.read()
                data['sensors'][sensor_name] = sensor_data
            except Exception as e:
                # Log error and continue with other sensors
                print(f"Error reading sensor {sensor_name}: {e}")
                data['sensors'][sensor_name] = {
                    'value': 0,
                    'unit': '',
                    'accuracy': 0,
                    'status': 'error'
                }
        
        # Collect system metrics
        data['metrics'] = await self._collect_system_metrics()
        
        # Collect alarms
        data['alarms'] = await self._check_alarms(data['sensors'])
        
        # Collect metadata
        data['location'] = await self._get_location()
        data['environment'] = await self._get_environment()
        data['network'] = await self._get_network_info()
        
        return data
    
    async def _collect_system_metrics(self) -> Dict[str, Any]:
        """Collect system-level metrics"""
        import psutil
        
        return {
            'cpu_usage': {
                'value': psutil.cpu_percent(),
                'unit': '%',
                'status': 'normal'
            },
            'memory_usage': {
                'value': psutil.virtual_memory().percent,
                'unit': '%',
                'status': 'normal'
            },
            'disk_usage': {
                'value': psutil.disk_usage('/').percent,
                'unit': '%',
                'status': 'normal'
            }
        }
    
    async def _check_alarms(self, sensor_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for alarms based on sensor data"""
        alarms = []
        
        for sensor_name, data in sensor_data.items():
            if data.get('status') == 'critical':
                alarms.append({
                    'id': f"{sensor_name.upper()}_CRITICAL",
                    'severity': 'critical',
                    'message': f"{sensor_name} is in critical state",
                    'timestamp': int(asyncio.get_event_loop().time())
                })
            elif data.get('status') == 'warning':
                alarms.append({
                    'id': f"{sensor_name.upper()}_WARNING",
                    'severity': 'warning',
                    'message': f"{sensor_name} is in warning state",
                    'timestamp': int(asyncio.get_event_loop().time())
                })
        
        return alarms
    
    async def _get_location(self) -> Dict[str, Any]:
        """Get device location information"""
        # This would typically get GPS coordinates or configured location
        return {
            'latitude': 41.0082,  # Default to Istanbul
            'longitude': 28.9784,
            'altitude': 100
        }
    
    async def _get_environment(self) -> Dict[str, Any]:
        """Get environmental information"""
        return {
            'ambient_temperature': 22.0,
            'ambient_humidity': 45.0
        }
    
    async def _get_network_info(self) -> Dict[str, Any]:
        """Get network information"""
        import socket
        
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
        except:
            hostname = "unknown"
            ip_address = "0.0.0.0"
        
        return {
            'hostname': hostname,
            'ip_address': ip_address,
            'connection_type': 'ethernet',  # or wifi
            'signal_strength': -45  # for wifi
        } 