import asyncio
from typing import Dict, Any
from abc import ABC, abstractmethod

class SensorInterface(ABC):
    """Base interface for all sensors"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.pin = config.get('pin', 0)
        self.calibration = config.get('calibration', 0.0)
        self.thresholds = config.get('thresholds', {})
    
    @abstractmethod
    async def read(self) -> Dict[str, Any]:
        """Read sensor data"""
        pass
    
    def _apply_calibration(self, value: float) -> float:
        """Apply calibration offset to sensor value"""
        return value + self.calibration
    
    def _determine_status(self, value: float) -> str:
        """Determine status based on thresholds"""
        if 'critical_high' in self.thresholds and value > self.thresholds['critical_high']:
            return 'critical'
        elif 'warning_high' in self.thresholds and value > self.thresholds['warning_high']:
            return 'warning'
        elif 'warning_low' in self.thresholds and value < self.thresholds['warning_low']:
            return 'warning'
        elif 'critical_low' in self.thresholds and value < self.thresholds['critical_low']:
            return 'critical'
        else:
            return 'normal'

class TemperatureSensor(SensorInterface):
    """Temperature sensor implementation"""
    
    async def read(self) -> Dict[str, Any]:
        """Read temperature data"""
        try:
            # Try to read from DHT22 if available
            temperature = await self._read_dht22()
        except ImportError:
            # Fallback to simulated temperature
            temperature = await self._read_simulated()
        
        # Apply calibration
        temperature = self._apply_calibration(temperature)
        
        return {
            'value': temperature,
            'unit': '°C',
            'accuracy': 0.1,
            'status': self._determine_status(temperature),
            'thresholds': self.thresholds
        }
    
    async def _read_dht22(self) -> float:
        """Read from DHT22 sensor"""
        try:
            import Adafruit_DHT
            sensor = Adafruit_DHT.DHT22
            humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
            return temperature if temperature is not None else 25.0
        except ImportError:
            raise ImportError("DHT library not available")
    
    async def _read_simulated(self) -> float:
        """Simulated temperature reading"""
        import random
        # Simulate temperature between 20-30°C
        return 20.0 + random.uniform(0, 10)

class HumiditySensor(SensorInterface):
    """Humidity sensor implementation"""
    
    async def read(self) -> Dict[str, Any]:
        """Read humidity data"""
        try:
            # Try to read from DHT22 if available
            humidity = await self._read_dht22()
        except ImportError:
            # Fallback to simulated humidity
            humidity = await self._read_simulated()
        
        # Apply calibration
        humidity = self._apply_calibration(humidity)
        
        return {
            'value': humidity,
            'unit': '%',
            'accuracy': 0.5,
            'status': self._determine_status(humidity),
            'thresholds': self.thresholds
        }
    
    async def _read_dht22(self) -> float:
        """Read from DHT22 sensor"""
        try:
            import Adafruit_DHT
            sensor = Adafruit_DHT.DHT22
            humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
            return humidity if humidity is not None else 50.0
        except ImportError:
            raise ImportError("DHT library not available")
    
    async def _read_simulated(self) -> float:
        """Simulated humidity reading"""
        import random
        # Simulate humidity between 40-60%
        return 40.0 + random.uniform(0, 20)

class PressureSensor(SensorInterface):
    """Pressure sensor implementation"""
    
    async def read(self) -> Dict[str, Any]:
        """Read pressure data"""
        try:
            pressure = await self._read_bmp280()
        except ImportError:
            pressure = await self._read_simulated()
        
        pressure = self._apply_calibration(pressure)
        
        return {
            'value': pressure,
            'unit': 'hPa',
            'accuracy': 1.0,
            'status': self._determine_status(pressure),
            'thresholds': self.thresholds
        }
    
    async def _read_bmp280(self) -> float:
        """Read from BMP280 sensor"""
        try:
            import smbus2
            bus = smbus2.SMBus(1)
            # BMP280 I2C address
            address = 0x76
            # Read pressure data
            data = bus.read_i2c_block_data(address, 0xF7, 3)
            pressure = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
            return pressure / 256.0
        except ImportError:
            raise ImportError("SMBus library not available")
    
    async def _read_simulated(self) -> float:
        """Simulated pressure reading"""
        import random
        # Simulate atmospheric pressure around 1013 hPa
        return 1013.0 + random.uniform(-10, 10) 