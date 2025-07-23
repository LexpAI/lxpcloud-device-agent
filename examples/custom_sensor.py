#!/usr/bin/env python3
"""
Custom Sensor Example for LXPCloud Device Agent
"""

import asyncio
import sys
import os
import random

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lxpcloud_device_agent import LXPCloudAgent
from lxpcloud_device_agent.hardware.sensors import SensorInterface

class CustomTemperatureSensor(SensorInterface):
    """Custom temperature sensor implementation"""
    
    def __init__(self, config):
        super().__init__(config)
        self.sensor_id = config.get('sensor_id', 'custom_temp')
    
    async def read(self) -> dict:
        """Read custom temperature data"""
        # Simulate temperature reading with some variation
        base_temp = 25.0
        variation = random.uniform(-2, 2)
        temperature = base_temp + variation
        
        # Apply calibration
        temperature = self._apply_calibration(temperature)
        
        return {
            'value': temperature,
            'unit': '°C',
            'accuracy': 0.5,
            'status': self._determine_status(temperature),
            'sensor_id': self.sensor_id
        }

class CustomPressureSensor(SensorInterface):
    """Custom pressure sensor implementation"""
    
    def __init__(self, config):
        super().__init__(config)
        self.sensor_id = config.get('sensor_id', 'custom_pressure')
    
    async def read(self) -> dict:
        """Read custom pressure data"""
        # Simulate pressure reading
        base_pressure = 1013.25  # Standard atmospheric pressure
        variation = random.uniform(-5, 5)
        pressure = base_pressure + variation
        
        # Apply calibration
        pressure = self._apply_calibration(pressure)
        
        return {
            'value': pressure,
            'unit': 'hPa',
            'accuracy': 1.0,
            'status': self._determine_status(pressure),
            'sensor_id': self.sensor_id
        }

async def main():
    """Custom sensor example"""
    print("🔧 LXPCloud Device Agent - Custom Sensor Example")
    print("=" * 55)
    
    # Create custom configuration
    custom_config = {
        "api": {
            "base_url": "https://app.lexpai.com/api",
            "endpoint": "/machine.php",
            "api_key": "your_api_key_here",
            "timeout": 30,
            "retry_attempts": 3
        },
        "device": {
            "name": "Custom Sensor Device",
            "type": "custom_device",
            "location": "Test Lab",
            "timezone": "Europe/Istanbul"
        },
        "data_collection": {
            "interval": 10,  # Collect every 10 seconds for demo
            "batch_size": 5
        },
        "sensors": {
            "custom_temp": {
                "enabled": True,
                "type": "custom_temperature",
                "sensor_id": "custom_temp_001",
                "calibration": 0.0,
                "thresholds": {
                    "warning_low": 20,
                    "warning_high": 30,
                    "critical_low": 15,
                    "critical_high": 35
                }
            },
            "custom_pressure": {
                "enabled": True,
                "type": "custom_pressure",
                "sensor_id": "custom_pressure_001",
                "calibration": 0.0,
                "thresholds": {
                    "warning_low": 1000,
                    "warning_high": 1025,
                    "critical_low": 990,
                    "critical_high": 1035
                }
            }
        },
        "logging": {
            "level": "INFO",
            "console_output": True
        }
    }
    
    # Save custom config temporarily
    config_path = "custom_config.json"
    import json
    with open(config_path, 'w') as f:
        json.dump(custom_config, f, indent=2)
    
    try:
        # Initialize agent with custom config
        agent = LXPCloudAgent(config_path)
        
        # Add custom sensors to data collector
        agent.data_collector.sensors['custom_temp'] = CustomTemperatureSensor(
            custom_config['sensors']['custom_temp']
        )
        agent.data_collector.sensors['custom_pressure'] = CustomPressureSensor(
            custom_config['sensors']['custom_pressure']
        )
        
        print("Starting agent with custom sensors...")
        await agent.start()
        
        # Run for a short time to demonstrate
        print("Agent is running with custom sensors. Press Ctrl+C to stop...")
        await asyncio.sleep(20)  # Run for 20 seconds
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await agent.stop()
        # Clean up temporary config
        if os.path.exists(config_path):
            os.remove(config_path)
        print("Agent stopped.")

if __name__ == "__main__":
    asyncio.run(main()) 