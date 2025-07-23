import json
import time
from datetime import datetime
from typing import Dict, Any, List
import uuid

class LXPProtocol:
    """
    LXPCloud Custom Protocol Implementation
    Handles data formatting and validation
    """
    
    def __init__(self, version: str = "1.0"):
        self.version = version
        self.required_fields = [
            'lxp_version', 'device_info', 'timestamp', 'data'
        ]
    
    def format_data(self, raw_data: Dict[str, Any], device_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format raw sensor data into LXPCloud protocol format
        """
        try:
            # Create base structure
            formatted_data = {
                "lxp_version": self.version,
                "device_info": self._format_device_info(device_info),
                "timestamp": self._format_timestamp(),
                "data": self._format_sensor_data(raw_data),
                "metadata": self._format_metadata(raw_data)
            }
            
            # Validate formatted data
            self._validate_data(formatted_data)
            
            return formatted_data
            
        except Exception as e:
            raise ValueError(f"Data formatting failed: {e}")
    
    def _format_device_info(self, device_info: Dict[str, Any]) -> Dict[str, Any]:
        """Format device information"""
        return {
            "device_id": device_info.get('device_id', str(uuid.uuid4())),
            "device_type": device_info.get('type', 'unknown'),
            "firmware_version": device_info.get('firmware_version', '1.0.0'),
            "hardware_version": device_info.get('hardware_version', '1.0.0')
        }
    
    def _format_timestamp(self) -> Dict[str, Any]:
        """Format timestamp information"""
        now = datetime.utcnow()
        return {
            "unix": int(now.timestamp()),
            "iso": now.isoformat() + "Z",
            "timezone": "UTC"
        }
    
    def _format_sensor_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format sensor data"""
        formatted = {
            "sensors": {},
            "metrics": {},
            "alarms": [],
            "status": {
                "operational": True,
                "maintenance_required": False,
                "last_maintenance": None
            }
        }
        
        # Process sensors
        for sensor_name, sensor_data in raw_data.get('sensors', {}).items():
            formatted["sensors"][sensor_name] = {
                "value": sensor_data.get('value', 0),
                "unit": sensor_data.get('unit', ''),
                "accuracy": sensor_data.get('accuracy', 0),
                "status": self._determine_status(sensor_data)
            }
        
        # Process metrics
        for metric_name, metric_data in raw_data.get('metrics', {}).items():
            formatted["metrics"][metric_name] = {
                "value": metric_data.get('value', 0),
                "unit": metric_data.get('unit', ''),
                "status": self._determine_status(metric_data)
            }
        
        # Process alarms
        for alarm in raw_data.get('alarms', []):
            formatted["alarms"].append({
                "id": alarm.get('id', 'UNKNOWN'),
                "severity": alarm.get('severity', 'info'),
                "message": alarm.get('message', ''),
                "timestamp": int(datetime.utcnow().timestamp())
            })
        
        return formatted
    
    def _format_metadata(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format metadata information"""
        return {
            "location": raw_data.get('location', {}),
            "environment": raw_data.get('environment', {}),
            "network": raw_data.get('network', {})
        }
    
    def _determine_status(self, data: Dict[str, Any]) -> str:
        """Determine status based on data values and thresholds"""
        value = data.get('value', 0)
        thresholds = data.get('thresholds', {})
        
        if 'critical_high' in thresholds and value > thresholds['critical_high']:
            return 'critical'
        elif 'warning_high' in thresholds and value > thresholds['warning_high']:
            return 'warning'
        elif 'warning_low' in thresholds and value < thresholds['warning_low']:
            return 'warning'
        elif 'critical_low' in thresholds and value < thresholds['critical_low']:
            return 'critical'
        else:
            return 'normal'
    
    def _validate_data(self, data: Dict[str, Any]):
        """Validate formatted data structure"""
        for field in self.required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate device_info
        device_info = data.get('device_info', {})
        if not device_info.get('device_id'):
            raise ValueError("Device ID is required")
        
        # Validate timestamp
        timestamp = data.get('timestamp', {})
        if not timestamp.get('unix') or not timestamp.get('iso'):
            raise ValueError("Invalid timestamp format")
    
    def parse_response(self, response_data: str) -> Dict[str, Any]:
        """Parse response from LXPCloud API"""
        try:
            return json.loads(response_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}") 