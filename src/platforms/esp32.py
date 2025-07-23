import serial
import json
from typing import Dict, Any
import time

class ESP32Platform:
    """ESP32 specific implementation"""
    
    def __init__(self, port: str = '/dev/ttyUSB0', baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        
    def connect(self):
        """Connect to ESP32"""
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for ESP32 to reset
            return True
        except Exception as e:
            print(f"Failed to connect to ESP32: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from ESP32"""
        if self.serial and self.serial.is_open:
            self.serial.close()
    
    def send_command(self, command: str) -> str:
        """Send command to ESP32 and get response"""
        if not self.serial or not self.serial.is_open:
            return ""
        
        try:
            self.serial.write(f"{command}\n".encode())
            response = self.serial.readline().decode().strip()
            return response
        except Exception as e:
            print(f"Error sending command: {e}")
            return ""
    
    def read_sensor_data(self) -> Dict[str, Any]:
        """Read all sensor data from ESP32"""
        command = "READ_ALL"
        response = self.send_command(command)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {}
    
    def read_temperature(self) -> float:
        """Read temperature from ESP32"""
        data = self.read_sensor_data()
        return data.get('temperature', 0.0)
    
    def read_humidity(self) -> float:
        """Read humidity from ESP32"""
        data = self.read_sensor_data()
        return data.get('humidity', 0.0)
    
    def read_pressure(self) -> float:
        """Read pressure from ESP32"""
        data = self.read_sensor_data()
        return data.get('pressure', 0.0)
    
    def read_wifi_signal(self) -> int:
        """Read WiFi signal strength"""
        command = "WIFI_SIGNAL"
        response = self.send_command(command)
        
        try:
            return int(response)
        except ValueError:
            return -100
    
    def get_ip_address(self) -> str:
        """Get ESP32 IP address"""
        command = "IP_ADDRESS"
        response = self.send_command(command)
        return response if response else "0.0.0.0"
    
    def set_gpio_pin(self, pin: int, state: bool):
        """Set GPIO pin state"""
        command = f"GPIO_{pin}_{'HIGH' if state else 'LOW'}"
        self.send_command(command)
    
    def read_gpio_pin(self, pin: int) -> bool:
        """Read GPIO pin state"""
        command = f"READ_GPIO_{pin}"
        response = self.send_command(command)
        return response.upper() == "HIGH" 