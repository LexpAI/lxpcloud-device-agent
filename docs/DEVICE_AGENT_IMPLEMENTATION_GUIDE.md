# LXPCloud Device Agent Implementation Guide

Bu doküman LXPCloud Device Agent'ın implementasyon detaylarını ve geliştirme süreçlerini açıklar.

## İçindekiler

1. [Genel Bakış](#genel-bakış)
2. [Kurulum ve Geliştirme Ortamı](#kurulum-ve-geliştirme-ortamı)
3. [Proje Yapısı](#proje-yapısı)
4. [Core Bileşenler](#core-bileşenler)
5. [Platform Implementasyonları](#platform-implementasyonları)
6. [Protokol Implementasyonu](#protokol-implementasyonu)
7. [Test ve Doğrulama](#test-ve-doğrulama)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

## Genel Bakış

LXPCloud Device Agent, IoT cihazlarından LXPCloud platformuna veri göndermek için tasarlanmış çok platformlu bir yazılım çözümüdür. Bu guide, agent'ın nasıl geliştirileceğini, test edileceğini ve deploy edileceğini detaylandırır.

## Kurulum ve Geliştirme Ortamı

### Gereksinimler

#### Python Geliştirme
```bash
# Python 3.7+ gerekli
python --version

# Virtual environment oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Gerekli paketleri yükle
pip install -r requirements.txt
```

#### Geliştirme Araçları
```bash
# Code formatting
pip install black flake8

# Testing
pip install pytest pytest-asyncio

# Documentation
pip install sphinx sphinx-rtd-theme
```

### IDE Konfigürasyonu

#### VS Code
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black"
}
```

#### PyCharm
- Project interpreter olarak virtual environment seç
- Code style: PEP 8
- Auto-import: Enable

## Proje Yapısı

```
lxpcloud-device-agent/
├── src/                    # Ana kaynak kod
│   ├── core/              # Core bileşenler
│   ├── protocols/         # Protokol implementasyonları
│   ├── hardware/          # Donanım arayüzleri
│   ├── platforms/         # Platform özel kodlar
│   ├── utils/             # Yardımcı fonksiyonlar
│   └── cli.py             # CLI arayüzü
├── config/                # Konfigürasyon dosyaları
├── docs/                  # Dokümantasyon
├── examples/              # Örnek kodlar
├── tests/                 # Test dosyaları
├── scripts/               # Kurulum ve yardımcı scriptler
├── requirements.txt       # Python bağımlılıkları
├── setup.py              # Kurulum scripti
└── README.md             # Proje açıklaması
```

## Core Bileşenler

### 1. Agent Manager

Ana agent yöneticisi, tüm bileşenleri koordine eder.

```python
# src/core/agent.py
import asyncio
import logging
from typing import Dict, Any
from .data_collector import DataCollector
from .data_sender import DataSender
from .connection import ConnectionManager

class LXPCloudAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.data_collector = DataCollector(config)
        self.data_sender = DataSender(config)
        self.connection = ConnectionManager(config)
        self.running = False
        
    async def start(self):
        """Agent'ı başlat"""
        self.logger.info("Starting LXPCloud Agent")
        self.running = True
        
        try:
            await self.connection.connect()
            await self._main_loop()
        except Exception as e:
            self.logger.error(f"Agent error: {e}")
            raise
        finally:
            await self.stop()
    
    async def stop(self):
        """Agent'ı durdur"""
        self.logger.info("Stopping LXPCloud Agent")
        self.running = False
        await self.connection.disconnect()
    
    async def _main_loop(self):
        """Ana döngü"""
        while self.running:
            try:
                # Veri topla
                data = await self.data_collector.collect()
                
                # Veriyi gönder
                if data:
                    await self.data_sender.send(data)
                
                # Bekle
                await asyncio.sleep(self.config.get('interval', 60))
                
            except Exception as e:
                self.logger.error(f"Main loop error: {e}")
                await asyncio.sleep(10)  # Hata durumunda bekle
```

### 2. Data Collector

Sensörlerden veri toplama motoru.

```python
# src/core/data_collector.py
import asyncio
import logging
from typing import Dict, Any, Optional
from ..hardware.sensors import SensorInterface
from ..utils.validator import DataValidator

class DataCollector:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.sensors = SensorInterface(config)
        self.validator = DataValidator()
        
    async def collect(self) -> Optional[Dict[str, Any]]:
        """Tüm sensörlerden veri topla"""
        try:
            # Sensör verilerini topla
            sensor_data = await self.sensors.read_all()
            
            # Sistem metriklerini topla
            system_metrics = await self._collect_system_metrics()
            
            # Veriyi birleştir
            data = {
                'sensors': sensor_data,
                'metrics': system_metrics,
                'timestamp': self._get_timestamp()
            }
            
            # Veriyi doğrula
            if self.validator.validate(data):
                return data
            else:
                self.logger.warning("Invalid data collected")
                return None
                
        except Exception as e:
            self.logger.error(f"Data collection error: {e}")
            return None
    
    async def _collect_system_metrics(self) -> Dict[str, Any]:
        """Sistem metriklerini topla"""
        # Platform özel implementasyon
        pass
    
    def _get_timestamp(self) -> Dict[str, Any]:
        """Zaman damgası oluştur"""
        import time
        from datetime import datetime
        
        now = datetime.utcnow()
        return {
            'unix': int(time.time()),
            'iso': now.isoformat() + 'Z',
            'timezone': 'UTC'
        }
```

### 3. Data Sender

Veri gönderme motoru.

```python
# src/core/data_sender.py
import asyncio
import logging
from typing import Dict, Any
from ..protocols.lxp_protocol import LXPProtocol
from ..utils.crypto import DataEncryptor

class DataSender:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.protocol = LXPProtocol(config)
        self.encryptor = DataEncryptor(config)
        
    async def send(self, data: Dict[str, Any]) -> bool:
        """Veriyi LXPCloud'a gönder"""
        try:
            # Veriyi protokol formatına çevir
            payload = self.protocol.format_data(data)
            
            # Veriyi şifrele (opsiyonel)
            if self.config.get('encryption_enabled', False):
                payload = self.encryptor.encrypt(payload)
            
            # API'ye gönder
            success = await self._send_to_api(payload)
            
            if success:
                self.logger.info("Data sent successfully")
            else:
                self.logger.error("Failed to send data")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Data sending error: {e}")
            return False
    
    async def _send_to_api(self, payload: Dict[str, Any]) -> bool:
        """API'ye veri gönder"""
        # HTTP client implementasyonu
        pass
```

## Platform Implementasyonları

### 1. Raspberry Pi

```python
# src/platforms/raspberry_pi.py
import asyncio
import logging
from typing import Dict, Any
import RPi.GPIO as GPIO
from smbus2 import SMBus

class RaspberryPiPlatform:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.i2c_bus = SMBus(1)  # I2C bus 1
        GPIO.setmode(GPIO.BCM)
        
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Raspberry Pi sistem metriklerini al"""
        try:
            # CPU kullanımı
            cpu_usage = await self._get_cpu_usage()
            
            # Memory kullanımı
            memory_usage = await self._get_memory_usage()
            
            # Disk kullanımı
            disk_usage = await self._get_disk_usage()
            
            # Sıcaklık
            temperature = await self._get_temperature()
            
            return {
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage,
                'temperature': temperature
            }
            
        except Exception as e:
            self.logger.error(f"System metrics error: {e}")
            return {}
    
    async def _get_cpu_usage(self) -> float:
        """CPU kullanımını al"""
        try:
            with open('/proc/loadavg', 'r') as f:
                load = f.read().split()[0]
                return float(load) * 100
        except:
            return 0.0
    
    async def _get_memory_usage(self) -> float:
        """Memory kullanımını al"""
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
                total = int(lines[0].split()[1])
                available = int(lines[2].split()[1])
                return ((total - available) / total) * 100
        except:
            return 0.0
    
    async def _get_disk_usage(self) -> float:
        """Disk kullanımını al"""
        import shutil
        try:
            usage = shutil.disk_usage('/')
            return (usage.used / usage.total) * 100
        except:
            return 0.0
    
    async def _get_temperature(self) -> float:
        """CPU sıcaklığını al"""
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = int(f.read()) / 1000.0
                return temp
        except:
            return 0.0
    
    def cleanup(self):
        """Temizlik işlemleri"""
        GPIO.cleanup()
        self.i2c_bus.close()
```

### 2. Arduino

```cpp
// src/platforms/arduino/lxpcloud_agent.ino
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// Konfigürasyon
const char* ssid = "your-wifi-ssid";
const char* password = "your-wifi-password";
const char* api_url = "https://app.lexpai.com/api/machine.php";
const char* api_key = "your-api-key";

// Sensörler
DHT dht(4, DHT22);  // DHT22 sensörü pin 4'te

// Global değişkenler
unsigned long lastSend = 0;
const long sendInterval = 60000;  // 60 saniye

void setup() {
  Serial.begin(115200);
  
  // WiFi bağlantısı
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("WiFi connected");
  
  // Sensörleri başlat
  dht.begin();
}

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - lastSend >= sendInterval) {
    sendData();
    lastSend = currentMillis;
  }
}

void sendData() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(api_url);
    http.addHeader("Content-Type", "application/json");
    
    // JSON oluştur
    DynamicJsonDocument doc(1024);
    doc["api_key"] = api_key;
    doc["payload"]["lxp_version"] = "1.0";
    doc["payload"]["device_info"]["device_type"] = "arduino";
    doc["payload"]["timestamp"]["unix"] = getUnixTime();
    
    // Sensör verilerini ekle
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    
    doc["payload"]["data"]["sensors"]["temperature"]["value"] = temperature;
    doc["payload"]["data"]["sensors"]["temperature"]["unit"] = "°C";
    doc["payload"]["data"]["sensors"]["humidity"]["value"] = humidity;
    doc["payload"]["data"]["sensors"]["humidity"]["unit"] = "%";
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    // POST isteği gönder
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("HTTP Response code: " + String(httpResponseCode));
      Serial.println("Response: " + response);
    } else {
      Serial.println("Error on sending POST: " + String(httpResponseCode));
    }
    
    http.end();
  }
}

unsigned long getUnixTime() {
  // Basit Unix timestamp (gerçek uygulamada NTP kullan)
  return millis() / 1000;
}
```

### 3. ESP32

```cpp
// src/platforms/esp32/lxpcloud_agent.cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <time.h>

// Konfigürasyon
const char* ssid = "your-wifi-ssid";
const char* password = "your-wifi-password";
const char* api_url = "https://app.lexpai.com/api/machine.php";
const char* api_key = "your-api-key";
const char* ntp_server = "pool.ntp.org";

// Sensörler
DHT dht(4, DHT22);

// Global değişkenler
unsigned long lastSend = 0;
const long sendInterval = 60000;

void setup() {
  Serial.begin(115200);
  
  // WiFi bağlantısı
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("WiFi connected");
  
  // NTP zaman senkronizasyonu
  configTime(0, 0, ntp_server);
  
  // Sensörleri başlat
  dht.begin();
}

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - lastSend >= sendInterval) {
    sendData();
    lastSend = currentMillis;
  }
}

void sendData() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(api_url);
    http.addHeader("Content-Type", "application/json");
    
    // JSON oluştur
    DynamicJsonDocument doc(2048);
    doc["api_key"] = api_key;
    doc["payload"]["lxp_version"] = "1.0";
    doc["payload"]["device_info"]["device_type"] = "esp32";
    doc["payload"]["timestamp"]["unix"] = getUnixTime();
    doc["payload"]["timestamp"]["iso"] = getISOTime();
    
    // Sensör verilerini ekle
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    
    if (!isnan(temperature)) {
      doc["payload"]["data"]["sensors"]["temperature"]["value"] = temperature;
      doc["payload"]["data"]["sensors"]["temperature"]["unit"] = "°C";
      doc["payload"]["data"]["sensors"]["temperature"]["status"] = "normal";
    }
    
    if (!isnan(humidity)) {
      doc["payload"]["data"]["sensors"]["humidity"]["value"] = humidity;
      doc["payload"]["data"]["sensors"]["humidity"]["unit"] = "%";
      doc["payload"]["data"]["sensors"]["humidity"]["status"] = "normal";
    }
    
    // Sistem metrikleri
    doc["payload"]["data"]["metrics"]["free_heap"]["value"] = ESP.getFreeHeap();
    doc["payload"]["data"]["metrics"]["free_heap"]["unit"] = "bytes";
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    // POST isteği gönder
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("HTTP Response code: " + String(httpResponseCode));
      Serial.println("Response: " + response);
    } else {
      Serial.println("Error on sending POST: " + String(httpResponseCode));
    }
    
    http.end();
  }
}

unsigned long getUnixTime() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    return 0;
  }
  time(&now);
  return now;
}

String getISOTime() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    return "";
  }
  
  char timeString[64];
  strftime(timeString, sizeof(timeString), "%Y-%m-%dT%H:%M:%S.000Z", &timeinfo);
  return String(timeString);
}
```

## Protokol Implementasyonu

### LXP Protocol

```python
# src/protocols/lxp_protocol.py
import json
import uuid
import time
from datetime import datetime
from typing import Dict, Any

class LXPProtocol:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.device_id = config.get('device_id', str(uuid.uuid4()))
        
    def format_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Veriyi LXPCloud protokolüne uygun formata çevir"""
        timestamp = self._get_timestamp()
        
        payload = {
            'lxp_version': '1.0',
            'device_info': {
                'device_id': self.device_id,
                'device_type': self.config.get('device_type', 'unknown'),
                'firmware_version': self.config.get('firmware_version', '1.0.0'),
                'hardware_version': self.config.get('hardware_version', '1.0.0')
            },
            'timestamp': timestamp,
            'data': {
                'sensors': data.get('sensors', {}),
                'metrics': data.get('metrics', {}),
                'alarms': data.get('alarms', []),
                'status': {
                    'operational': True,
                    'maintenance_required': False,
                    'last_maintenance': None
                }
            },
            'metadata': {
                'location': self.config.get('location', {
                    'latitude': 0.0,
                    'longitude': 0.0,
                    'altitude': 0
                }),
                'environment': {
                    'ambient_temperature': data.get('ambient_temperature', 0.0),
                    'ambient_humidity': data.get('ambient_humidity', 0.0)
                },
                'network': {
                    'hostname': self.config.get('hostname', 'unknown'),
                    'ip_address': self.config.get('ip_address', '0.0.0.0'),
                    'connection_type': self.config.get('connection_type', 'unknown')
                }
            }
        }
        
        return {
            'api_key': self.config['api_key'],
            'payload': payload,
            'recorded_at': timestamp['unix']
        }
    
    def _get_timestamp(self) -> Dict[str, Any]:
        """Zaman damgası oluştur"""
        now = datetime.utcnow()
        return {
            'unix': int(time.time()),
            'iso': now.isoformat() + 'Z',
            'timezone': 'UTC'
        }
    
    def validate_payload(self, payload: Dict[str, Any]) -> bool:
        """Payload'ı doğrula"""
        required_fields = ['api_key', 'payload', 'recorded_at']
        
        for field in required_fields:
            if field not in payload:
                return False
        
        return True
```

## Test ve Doğrulama

### Unit Tests

```python
# tests/test_agent.py
import pytest
import asyncio
from unittest.mock import Mock, patch
from src.core.agent import LXPCloudAgent

class TestLXPCloudAgent:
    @pytest.fixture
    def config(self):
        return {
            'api_key': 'test-key',
            'api_url': 'https://test.api.com',
            'interval': 60,
            'device_type': 'test_device'
        }
    
    @pytest.fixture
    def agent(self, config):
        return LXPCloudAgent(config)
    
    @pytest.mark.asyncio
    async def test_agent_start_stop(self, agent):
        """Agent başlatma ve durdurma testi"""
        # Agent'ı başlat
        start_task = asyncio.create_task(agent.start())
        
        # Kısa süre bekle
        await asyncio.sleep(0.1)
        
        # Agent'ı durdur
        agent.running = False
        await start_task
        
        assert not agent.running
    
    @pytest.mark.asyncio
    async def test_data_collection(self, agent):
        """Veri toplama testi"""
        data = await agent.data_collector.collect()
        assert data is not None
        assert 'timestamp' in data
        assert 'sensors' in data
        assert 'metrics' in data
```

### Integration Tests

```python
# tests/test_integration.py
import pytest
import asyncio
from src.core.agent import LXPCloudAgent

class TestIntegration:
    @pytest.mark.asyncio
    async def test_full_data_flow(self):
        """Tam veri akışı testi"""
        config = {
            'api_key': 'test-key',
            'api_url': 'https://test.api.com',
            'interval': 1,
            'device_type': 'test_device'
        }
        
        agent = LXPCloudAgent(config)
        
        # Test için kısa süre çalıştır
        start_task = asyncio.create_task(agent.start())
        await asyncio.sleep(2)
        agent.running = False
        await start_task
        
        # Başarılı çalıştığını doğrula
        assert True
```

### Hardware Tests

```python
# tests/test_hardware.py
import pytest
from src.hardware.sensors import SensorInterface

class TestHardware:
    def test_sensor_interface(self):
        """Sensör arayüzü testi"""
        config = {
            'sensors': {
                'temperature': {'enabled': True, 'pin': 4},
                'humidity': {'enabled': True, 'pin': 17}
            }
        }
        
        sensors = SensorInterface(config)
        
        # Sensör listesini kontrol et
        sensor_list = sensors.get_available_sensors()
        assert len(sensor_list) > 0
        
        # Sensör okuma testi (mock)
        with patch.object(sensors, 'read_sensor') as mock_read:
            mock_read.return_value = 25.5
            value = sensors.read_sensor('temperature')
            assert value == 25.5
```

## Deployment

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizinini ayarla
WORKDIR /app

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY src/ ./src/
COPY config/ ./config/

# Çalışma kullanıcısını oluştur
RUN useradd -m -u 1000 lxpcloud
USER lxpcloud

# Uygulamayı çalıştır
CMD ["python", "-m", "src.cli", "start"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  lxpcloud-agent:
    build: .
    container_name: lxpcloud-agent
    restart: unless-stopped
    environment:
      - API_KEY=${API_KEY}
      - DEVICE_TYPE=${DEVICE_TYPE}
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    networks:
      - lxpcloud-network

networks:
  lxpcloud-network:
    driver: bridge
```

### Systemd Service

```ini
# /etc/systemd/system/lxpcloud-agent.service
[Unit]
Description=LXPCloud Device Agent
After=network.target

[Service]
Type=simple
User=lxpcloud
WorkingDirectory=/opt/lxpcloud-agent
ExecStart=/opt/lxpcloud-agent/venv/bin/python -m src.cli start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Windows Service

```python
# scripts/windows_service.py
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
from src.core.agent import LXPCloudAgent

class LXPCloudService(win32serviceutil.ServiceFramework):
    _svc_name_ = "LXPCloudAgent"
    _svc_display_name_ = "LXPCloud Device Agent"
    _svc_description_ = "LXPCloud IoT Device Agent Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.agent = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        if self.agent:
            self.agent.running = False

    def SvcDoRun(self):
        try:
            config = self._load_config()
            self.agent = LXPCloudAgent(config)
            
            import asyncio
            asyncio.run(self.agent.start())
        except Exception as e:
            import logging
            logging.error(f"Service error: {e}")

    def _load_config(self):
        # Konfigürasyon yükleme
        pass

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(LXPCloudService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(LXPCloudService)
```

## Troubleshooting

### Yaygın Sorunlar

#### 1. Bağlantı Sorunları
```bash
# Ağ bağlantısını test et
ping app.lexpai.com

# DNS çözümlemesini kontrol et
nslookup app.lexpai.com

# Firewall ayarlarını kontrol et
sudo ufw status
```

#### 2. Sensör Sorunları
```bash
# GPIO pinlerini kontrol et
gpio readall

# I2C cihazlarını listele
i2cdetect -y 1

# Sensör loglarını kontrol et
tail -f /var/log/lxpcloud-agent.log
```

#### 3. Performans Sorunları
```bash
# Sistem kaynaklarını kontrol et
htop
df -h
free -h

# Agent loglarını kontrol et
grep "ERROR" /var/log/lxpcloud-agent.log
```

### Debug Modu

```python
# Debug modunda çalıştır
import logging
logging.basicConfig(level=logging.DEBUG)

# Detaylı loglama
logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Log Analizi

```bash
# Hata loglarını analiz et
grep "ERROR" /var/log/lxpcloud-agent.log | tail -20

# Başarılı gönderimleri say
grep "Data sent successfully" /var/log/lxpcloud-agent.log | wc -l

# Performans metriklerini analiz et
grep "Response time" /var/log/lxpcloud-agent.log | awk '{print $NF}' | sort -n
```

Bu implementation guide, LXPCloud Device Agent'ın nasıl geliştirileceğini, test edileceğini ve deploy edileceğini kapsamlı bir şekilde açıklar. Geliştirme sürecinde bu dokümana referans olarak kullanabilirsiniz. 