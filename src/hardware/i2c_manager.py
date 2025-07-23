from typing import Dict, Any, List
import time

class I2CManager:
    """I2C communication manager"""
    
    def __init__(self, bus_number: int = 1):
        self.bus_number = bus_number
        self.devices = {}
        self._initialize_i2c()
    
    def _initialize_i2c(self):
        """Initialize I2C bus"""
        try:
            import smbus2
            self.bus = smbus2.SMBus(self.bus_number)
            self.i2c_available = True
        except ImportError:
            self.i2c_available = False
            print("I2C not available - running in simulation mode")
        except Exception as e:
            self.i2c_available = False
            print(f"I2C initialization failed: {e}")
    
    def scan_devices(self) -> List[int]:
        """Scan for I2C devices"""
        if not self.i2c_available:
            return []
        
        devices = []
        try:
            for address in range(0x03, 0x78):
                try:
                    self.bus.read_byte_data(address, 0)
                    devices.append(address)
                except:
                    continue
        except Exception as e:
            print(f"Error scanning I2C devices: {e}")
        
        return devices
    
    def read_byte(self, address: int, register: int) -> int:
        """Read single byte from I2C device"""
        if not self.i2c_available:
            return 0
        
        try:
            return self.bus.read_byte_data(address, register)
        except Exception as e:
            print(f"Error reading byte from I2C device {address}: {e}")
            return 0
    
    def write_byte(self, address: int, register: int, value: int):
        """Write single byte to I2C device"""
        if not self.i2c_available:
            return
        
        try:
            self.bus.write_byte_data(address, register, value)
        except Exception as e:
            print(f"Error writing byte to I2C device {address}: {e}")
    
    def read_word(self, address: int, register: int) -> int:
        """Read word (16-bit) from I2C device"""
        if not self.i2c_available:
            return 0
        
        try:
            return self.bus.read_word_data(address, register)
        except Exception as e:
            print(f"Error reading word from I2C device {address}: {e}")
            return 0
    
    def write_word(self, address: int, register: int, value: int):
        """Write word (16-bit) to I2C device"""
        if not self.i2c_available:
            return
        
        try:
            self.bus.write_word_data(address, register, value)
        except Exception as e:
            print(f"Error writing word to I2C device {address}: {e}")
    
    def read_block(self, address: int, register: int, length: int) -> List[int]:
        """Read block of data from I2C device"""
        if not self.i2c_available:
            return [0] * length
        
        try:
            return self.bus.read_i2c_block_data(address, register, length)
        except Exception as e:
            print(f"Error reading block from I2C device {address}: {e}")
            return [0] * length
    
    def write_block(self, address: int, register: int, data: List[int]):
        """Write block of data to I2C device"""
        if not self.i2c_available:
            return
        
        try:
            self.bus.write_i2c_block_data(address, register, data)
        except Exception as e:
            print(f"Error writing block to I2C device {address}: {e}")
    
    def read_bmp280_temperature(self, address: int = 0x76) -> float:
        """Read temperature from BMP280 sensor"""
        try:
            # Read temperature data
            data = self.read_block(address, 0xFA, 3)
            temp_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
            
            # Convert to temperature (simplified)
            temperature = temp_raw / 5120.0
            return temperature
        except Exception as e:
            print(f"Error reading BMP280 temperature: {e}")
            return 25.0
    
    def read_bmp280_pressure(self, address: int = 0x76) -> float:
        """Read pressure from BMP280 sensor"""
        try:
            # Read pressure data
            data = self.read_block(address, 0xF7, 3)
            pressure_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
            
            # Convert to pressure (simplified)
            pressure = pressure_raw / 256.0
            return pressure
        except Exception as e:
            print(f"Error reading BMP280 pressure: {e}")
            return 1013.25
    
    def cleanup(self):
        """Cleanup I2C bus"""
        if self.i2c_available:
            try:
                self.bus.close()
            except Exception as e:
                print(f"Error cleaning up I2C: {e}") 