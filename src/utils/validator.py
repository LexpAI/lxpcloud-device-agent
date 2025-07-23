from typing import Dict, Any, List
import re

class DataValidator:
    """Data validation utilities for LXPCloud protocol"""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Validate API key format"""
        if not api_key or len(api_key) < 10:
            return False
        # API key should be alphanumeric
        return bool(re.match(r'^[a-zA-Z0-9_-]+$', api_key))
    
    @staticmethod
    def validate_device_name(name: str) -> bool:
        """Validate device name"""
        if not name or len(name) < 1 or len(name) > 100:
            return False
        return True
    
    @staticmethod
    def validate_sensor_value(value: Any, sensor_type: str) -> bool:
        """Validate sensor value based on type"""
        if sensor_type == 'temperature':
            return isinstance(value, (int, float)) and -50 <= value <= 100
        elif sensor_type == 'humidity':
            return isinstance(value, (int, float)) and 0 <= value <= 100
        elif sensor_type == 'pressure':
            return isinstance(value, (int, float)) and 800 <= value <= 1200
        else:
            return isinstance(value, (int, float))
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        # Check required fields
        required_fields = ['api', 'device', 'data_collection']
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        # Validate API configuration
        if 'api' in config:
            api_config = config['api']
            if 'api_key' not in api_config:
                errors.append("Missing API key")
            elif not DataValidator.validate_api_key(api_config['api_key']):
                errors.append("Invalid API key format")
        
        # Validate device configuration
        if 'device' in config:
            device_config = config['device']
            if 'name' not in device_config:
                errors.append("Missing device name")
            elif not DataValidator.validate_device_name(device_config['name']):
                errors.append("Invalid device name")
        
        return errors 