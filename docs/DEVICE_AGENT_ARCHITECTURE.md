# LXPCloud Device Agent Architecture

Bu doküman LXPCloud Device Agent'ın mimari tasarımını ve sistem yapısını detaylandırır.

## Genel Bakış

LXPCloud Device Agent, IoT cihazlarından LXPCloud platformuna veri göndermek için tasarlanmış çok platformlu bir yazılım çözümüdür. Agent, farklı donanım platformlarında çalışabilir ve çeşitli sensörlerden veri toplayarak LXPCloud API'sine gönderir.

## Sistem Mimarisi

### Katmanlı Mimari

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
├─────────────────────────────────────────────────────────────┤
│                    Business Logic Layer                     │
├─────────────────────────────────────────────────────────────┤
│                    Protocol Layer                           │
├─────────────────────────────────────────────────────────────┤
│                    Hardware Interface Layer                 │
├─────────────────────────────────────────────────────────────┤
│                    Platform Abstraction Layer               │
└─────────────────────────────────────────────────────────────┘
```

### Bileşenler

#### 1. Application Layer
- **CLI Interface**: Komut satırı arayüzü
- **Configuration Management**: Yapılandırma yönetimi
- **Logging System**: Loglama sistemi

#### 2. Business Logic Layer
- **Data Collector**: Veri toplama motoru
- **Data Sender**: Veri gönderme motoru
- **Agent Manager**: Ana agent yöneticisi
- **Error Handler**: Hata yönetimi

#### 3. Protocol Layer
- **LXP Protocol**: LXPCloud protokol implementasyonu
- **HTTP Client**: HTTP istemci
- **JSON Serializer**: JSON serileştirme

#### 4. Hardware Interface Layer
- **Sensor Interface**: Sensör arayüzü
- **Platform Specific**: Platform özel implementasyonlar
- **Hardware Abstraction**: Donanım soyutlama

#### 5. Platform Abstraction Layer
- **OS Interface**: İşletim sistemi arayüzü
- **Network Interface**: Ağ arayüzü
- **File System Interface**: Dosya sistemi arayüzü

## Veri Akışı

### Veri Toplama Süreci

```
Sensors → Data Collector → Data Processor → Protocol Formatter → HTTP Sender → LXPCloud API
```

### Detaylı Akış

1. **Sensör Okuma**: Donanım sensörlerinden veri okunur
2. **Veri İşleme**: Ham veriler işlenir ve formatlanır
3. **Protokol Formatlama**: LXPCloud protokolüne uygun JSON oluşturulur
4. **Ağ Gönderimi**: HTTPS üzerinden API'ye gönderilir
5. **Yanıt İşleme**: API yanıtı işlenir ve loglanır

## Desteklenen Platformlar

### 1. Raspberry Pi
- **OS**: Raspberry Pi OS (Debian-based)
- **Python**: 3.7+
- **GPIO**: RPi.GPIO veya gpiozero
- **Sensörler**: I2C, SPI, GPIO sensörleri

### 2. Arduino
- **Framework**: Arduino IDE
- **C++**: Arduino C++
- **Sensörler**: Analog, Digital, I2C, SPI
- **Ağ**: WiFi, Ethernet, GSM

### 3. ESP32
- **Framework**: Arduino IDE veya ESP-IDF
- **C++**: Arduino C++ veya ESP-IDF C
- **Sensörler**: Built-in sensörler + harici sensörler
- **Ağ**: WiFi, Bluetooth

### 4. Generic Python
- **OS**: Windows, Linux, macOS
- **Python**: 3.7+
- **Sensörler**: USB, Serial, Network sensörleri
- **Ağ**: Ethernet, WiFi

## Veri Protokolü

### LXPCloud JSON Format

```json
{
  "lxp_version": "1.0",
  "device_info": {
    "device_id": "unique-device-id",
    "device_type": "raspberry_pi",
    "firmware_version": "1.0.0",
    "hardware_version": "1.0.0"
  },
  "timestamp": {
    "unix": 1234567890,
    "iso": "2023-12-07T10:30:00.000Z",
    "timezone": "UTC"
  },
  "data": {
    "sensors": {
      "temperature": {
        "value": 25.5,
        "unit": "°C",
        "status": "normal"
      },
      "humidity": {
        "value": 45.2,
        "unit": "%",
        "status": "normal"
      }
    },
    "metrics": {
      "cpu_usage": {
        "value": 15.3,
        "unit": "%",
        "status": "normal"
      },
      "memory_usage": {
        "value": 65.8,
        "unit": "%",
        "status": "normal"
      }
    },
    "alarms": [],
    "status": {
      "operational": true,
      "maintenance_required": false,
      "last_maintenance": null
    }
  },
  "metadata": {
    "location": {
      "latitude": 41.0082,
      "longitude": 28.9784,
      "altitude": 100
    },
    "environment": {
      "ambient_temperature": 22.0,
      "ambient_humidity": 45.0
    },
    "network": {
      "hostname": "device-hostname",
      "ip_address": "192.168.1.100",
      "connection_type": "wifi"
    }
  }
}
```

## Güvenlik

### Kimlik Doğrulama
- **API Key**: Her cihaz için benzersiz API anahtarı
- **HTTPS**: Tüm iletişim şifrelenmiş
- **Certificate Validation**: SSL sertifika doğrulaması

### Veri Güvenliği
- **Encryption**: Veri şifreleme (opsiyonel)
- **Access Control**: Erişim kontrolü
- **Audit Logging**: Denetim logları

## Performans

### Optimizasyon Stratejileri
- **Batch Processing**: Toplu veri işleme
- **Compression**: Veri sıkıştırma
- **Caching**: Önbellekleme
- **Connection Pooling**: Bağlantı havuzu

### Monitoring
- **Resource Usage**: Kaynak kullanımı izleme
- **Network Latency**: Ağ gecikmesi
- **Error Rates**: Hata oranları
- **Throughput**: Veri aktarım hızı

## Hata Yönetimi

### Hata Kategorileri
1. **Network Errors**: Ağ hataları
2. **Hardware Errors**: Donanım hataları
3. **Protocol Errors**: Protokol hataları
4. **System Errors**: Sistem hataları

### Hata İşleme Stratejileri
- **Retry Logic**: Yeniden deneme mantığı
- **Fallback Mechanisms**: Yedek mekanizmalar
- **Graceful Degradation**: Zarif düşüş
- **Error Reporting**: Hata raporlama

## Konfigürasyon

### Yapılandırma Dosyası
```json
{
  "device": {
    "name": "My Device",
    "type": "raspberry_pi",
    "location": {
      "latitude": 41.0082,
      "longitude": 28.9784,
      "altitude": 100
    }
  },
  "api": {
    "url": "https://app.lexpai.com/api/machine.php",
    "key": "your-api-key",
    "timeout": 30,
    "retry_attempts": 3
  },
  "sensors": {
    "temperature": {
      "enabled": true,
      "pin": 4,
      "interval": 60
    },
    "humidity": {
      "enabled": true,
      "pin": 17,
      "interval": 60
    }
  },
  "logging": {
    "level": "INFO",
    "file": "/var/log/lxpcloud-agent.log",
    "max_size": "10MB",
    "backup_count": 5
  }
}
```

## Geliştirme

### Kod Organizasyonu
```
src/
├── core/           # Ana bileşenler
├── protocols/      # Protokol implementasyonları
├── hardware/       # Donanım arayüzleri
├── platforms/      # Platform özel kodlar
├── utils/          # Yardımcı fonksiyonlar
└── cli.py          # Komut satırı arayüzü
```

### Test Stratejisi
- **Unit Tests**: Birim testler
- **Integration Tests**: Entegrasyon testleri
- **Hardware Tests**: Donanım testleri
- **Performance Tests**: Performans testleri

## Deployment

### Kurulum Yöntemleri
1. **Package Manager**: Sistem paket yöneticisi
2. **Docker Container**: Docker konteyner
3. **Manual Installation**: Manuel kurulum
4. **Script Installation**: Otomatik kurulum scripti

### Service Management
- **Systemd**: Linux servis yönetimi
- **Windows Service**: Windows servis yönetimi
- **Docker Compose**: Konteyner orkestrasyonu

## Monitoring ve Logging

### Log Seviyeleri
- **DEBUG**: Geliştirici bilgileri
- **INFO**: Genel bilgiler
- **WARNING**: Uyarılar
- **ERROR**: Hatalar
- **CRITICAL**: Kritik hatalar

### Metrics
- **System Metrics**: Sistem metrikleri
- **Application Metrics**: Uygulama metrikleri
- **Network Metrics**: Ağ metrikleri
- **Custom Metrics**: Özel metrikler

## Gelecek Geliştirmeler

### Planlanan Özellikler
- **MQTT Support**: MQTT protokol desteği
- **Edge Computing**: Kenar hesaplama
- **Machine Learning**: Makine öğrenmesi
- **Real-time Analytics**: Gerçek zamanlı analitik
- **Multi-cloud Support**: Çoklu bulut desteği

### Teknoloji Güncellemeleri
- **Python 3.11+**: Yeni Python sürümü desteği
- **Async/Await**: Asenkron programlama
- **Type Hints**: Tip ipuçları
- **Modern C++**: Modern C++ özellikleri 