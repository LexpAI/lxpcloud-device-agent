import serial
from typing import Dict, Any
import time

class ArduinoPlatform:
    """Arduino specific implementation"""
    
    def __init__(self, port: str = '/dev/ttyUSB0', baudrate: int = 9600):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        
    def connect(self):
        """Connect to Arduino"""
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            return True
        except Exception as e:
            print(f"Failed to connect to Arduino: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from Arduino"""
        if self.serial and self.serial.is_open:
            self.serial.close()
    
    def send_command(self, command: str) -> str:
        """Send command to Arduino and get response"""
        if not self.serial or not self.serial.is_open:
            return ""
        
        try:
            self.serial.write(f"{command}\n".encode())
            response = self.serial.readline().decode().strip()
            return response
        except Exception as e:
            print(f"Error sending command: {e}")
            return ""
    
    def read_sensor(self, sensor_type: str) -> float:
        """Read sensor data from Arduino"""
        command = f"READ_{sensor_type.upper()}"
        response = self.send_command(command)
        
        try:
            return float(response)
        except ValueError:
            return 0.0
    
    def read_temperature(self) -> float:
        """Read temperature from Arduino"""
        return self.read_sensor("TEMP")
    
    def read_humidity(self) -> float:
        """Read humidity from Arduino"""
        return self.read_sensor("HUMIDITY")
    
    def read_pressure(self) -> float:
        """Read pressure from Arduino"""
        return self.read_sensor("PRESSURE")
    
    def set_digital_pin(self, pin: int, state: bool):
        """Set digital pin state"""
        command = f"PIN_{pin}_{'HIGH' if state else 'LOW'}"
        self.send_command(command)
    
    def read_digital_pin(self, pin: int) -> bool:
        """Read digital pin state"""
        command = f"READ_PIN_{pin}"
        response = self.send_command(command)
        return response.upper() == "HIGH" 