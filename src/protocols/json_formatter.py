import json
from typing import Dict, Any
from datetime import datetime

class JSONFormatter:
    """JSON formatting utilities for LXPCloud protocol"""
    
    @staticmethod
    def format_timestamp(timestamp: datetime) -> Dict[str, Any]:
        """Format timestamp in LXPCloud format"""
        return {
            "unix": int(timestamp.timestamp()),
            "iso": timestamp.isoformat() + "Z",
            "timezone": "UTC"
        }
    
    @staticmethod
    def format_sensor_value(value: float, unit: str, accuracy: float = 0.0) -> Dict[str, Any]:
        """Format sensor value in LXPCloud format"""
        return {
            "value": value,
            "unit": unit,
            "accuracy": accuracy
        }
    
    @staticmethod
    def format_alarm(alarm_id: str, severity: str, message: str) -> Dict[str, Any]:
        """Format alarm in LXPCloud format"""
        return {
            "id": alarm_id,
            "severity": severity,
            "message": message,
            "timestamp": int(datetime.utcnow().timestamp())
        }
    
    @staticmethod
    def validate_json(data: Dict[str, Any]) -> bool:
        """Validate JSON structure"""
        try:
            json.dumps(data)
            return True
        except (TypeError, ValueError):
            return False 