"""
LXPCloud Device Agent
Industrial IoT device agent for LXPCloud platform
"""

__version__ = "1.0.0"
__author__ = "LexpAI"
__email__ = "support@lexpai.com"

# Import main components
from .core.agent import LXPCloudAgent
from .core.connection import LXPConnection
from .core.data_collector import DataCollector
from .core.data_sender import DataSender

# Import protocols
from .protocols.lxp_protocol import LXPProtocol
from .protocols.json_formatter import JSONFormatter

# Import hardware components
from .hardware.sensors import SensorInterface, TemperatureSensor, HumiditySensor, PressureSensor
from .hardware.gpio_manager import GPIOManager
from .hardware.i2c_manager import I2CManager

# Import platform implementations
from .platforms.raspberry_pi import RaspberryPiPlatform
from .platforms.arduino import ArduinoPlatform
from .platforms.esp32 import ESP32Platform
from .platforms.generic import GenericPlatform

# Import utilities
from .utils.logger import setup_logger
from .utils.validator import DataValidator
from .utils.crypto import CryptoUtils

__all__ = [
    'LXPCloudAgent',
    'LXPConnection', 
    'DataCollector',
    'DataSender',
    'LXPProtocol',
    'JSONFormatter',
    'SensorInterface',
    'TemperatureSensor',
    'HumiditySensor',
    'PressureSensor',
    'GPIOManager',
    'I2CManager',
    'RaspberryPiPlatform',
    'ArduinoPlatform',
    'ESP32Platform',
    'GenericPlatform',
    'setup_logger',
    'DataValidator',
    'CryptoUtils'
] 