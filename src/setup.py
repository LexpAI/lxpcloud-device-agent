#!/usr/bin/env python3
"""
LXPCloud Device Agent Setup Wizard
Interactive configuration tool for device setup
"""

import json
import os
import sys
import getpass
from pathlib import Path

def main():
    print("🔧 LXPCloud Device Agent Setup Wizard")
    print("=====================================")
    print()
    
    # Get API key
    api_key = input("Enter your LXPCloud API key: ").strip()
    if not api_key:
        print("❌ API key is required!")
        sys.exit(1)
    
    # Get device information
    device_name = input("Enter device name (e.g., 'Coating Machine 1'): ").strip()
    if not device_name:
        device_name = "LXPCloud Device"
    
    device_type = input("Enter device type (e.g., 'coating_machine'): ").strip()
    if not device_type:
        device_type = "generic_device"
    
    location = input("Enter device location (e.g., 'Factory A'): ").strip()
    if not location:
        location = "Unknown"
    
    # Get sensor configuration
    print("\n📡 Sensor Configuration:")
    print("Configure which sensors are connected to your device.")
    
    sensors = {}
    
    # Temperature sensor
    temp_enabled = input("Enable temperature sensor? (y/n): ").lower().startswith('y')
    if temp_enabled:
        temp_pin = input("Temperature sensor GPIO pin (default: 18): ").strip()
        temp_pin = int(temp_pin) if temp_pin.isdigit() else 18
        sensors['temperature'] = {
            "enabled": True,
            "type": "temperature",
            "pin": temp_pin,
            "calibration": 0.0,
            "thresholds": {
                "warning_low": 15,
                "warning_high": 35,
                "critical_low": 10,
                "critical_high": 40
            }
        }
    
    # Humidity sensor
    humidity_enabled = input("Enable humidity sensor? (y/n): ").lower().startswith('y')
    if humidity_enabled:
        humidity_pin = input("Humidity sensor GPIO pin (default: 19): ").strip()
        humidity_pin = int(humidity_pin) if humidity_pin.isdigit() else 19
        sensors['humidity'] = {
            "enabled": True,
            "type": "humidity",
            "pin": humidity_pin,
            "calibration": 0.0,
            "thresholds": {
                "warning_low": 30,
                "warning_high": 70,
                "critical_low": 20,
                "critical_high": 80
            }
        }
    
    # Data collection interval
    interval = input("Data collection interval in seconds (default: 60): ").strip()
    interval = int(interval) if interval.isdigit() else 60
    
    # Create configuration
    config = {
        "api": {
            "base_url": "https://app.lexpai.com/api",
            "endpoint": "/machine.php",
            "api_key": api_key,
            "timeout": 30,
            "retry_attempts": 3,
            "batch_size": 10
        },
        "device": {
            "name": device_name,
            "type": device_type,
            "location": location,
            "timezone": "Europe/Istanbul",
            "device_id": "auto-generated",
            "firmware_version": "1.0.0",
            "hardware_version": "1.0.0"
        },
        "data_collection": {
            "interval": interval,
            "batch_size": 10,
            "compression": True,
            "encryption": False,
            "max_retries": 3
        },
        "sensors": sensors,
        "logging": {
            "level": "INFO",
            "file": "/var/log/lxpcloud-agent.log",
            "max_size": "10MB",
            "backup_count": 5,
            "console_output": True
        },
        "network": {
            "wifi_ssid": "",
            "wifi_password": "",
            "ethernet_priority": True,
            "connection_timeout": 30
        },
        "location": {
            "latitude": 41.0082,
            "longitude": 28.9784,
            "altitude": 100
        }
    }
    
    # Save configuration
    config_path = "/etc/lxpcloud-agent/device_config.json"
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"\n✅ Configuration saved to: {config_path}")
    except PermissionError:
        print(f"\n❌ Permission denied. Please run with sudo:")
        print(f"sudo python3 -m lxpcloud_device_agent.setup")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the service: sudo systemctl start lxpcloud-agent")
    print("2. Check status: sudo systemctl status lxpcloud-agent")
    print("3. View logs: sudo journalctl -u lxpcloud-agent -f")
    print("\nFor support: support@lexpai.com")

if __name__ == "__main__":
    main() 