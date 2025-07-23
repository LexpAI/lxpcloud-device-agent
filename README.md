# LXPCloud Device Agent

LXPCloud Device Agent, IoT cihazlarından LXPCloud platformuna veri göndermek için tasarlanmış çok platformlu bir yazılım çözümüdür.

## 🚀 Özellikler

- **Çok Platformlu Destek**: Raspberry Pi, Arduino, ESP32, Windows, Linux, macOS
- **Çeşitli Sensör Desteği**: Sıcaklık, nem, basınç, hareket, ışık ve daha fazlası
- **Güvenli İletişim**: HTTPS üzerinden şifrelenmiş veri aktarımı
- **Hata Yönetimi**: Otomatik yeniden deneme ve hata raporlama
- **Esnek Konfigürasyon**: JSON tabanlı yapılandırma sistemi
- **PowerShell Entegrasyonu**: Windows ortamında PowerShell scriptleri ile veri gönderimi

## 📁 Proje Yapısı

```
lxpcloud-device-agent/
├── src/                    # Ana kaynak kod
│   ├── core/              # Core bileşenler
│   ├── protocols/         # Protokol implementasyonları
│   ├── hardware/          # Donanım arayüzleri
│   ├── platforms/         # Platform özel kodlar
│   ├── utils/             # Yardımcı fonksiyonlar
│   └── cli.py             # CLI arayüzü
├── PowerShell/            # PowerShell scriptleri
│   ├── README.md          # PowerShell kullanım kılavuzu
│   ├── test_single_send.ps1         # Tek seferlik test
│   ├── send_data_powershell_final.ps1 # Sürekli veri gönderimi
│   └── debug_powershell_fixed.ps1   # Debug scripti
├── config/                # Konfigürasyon dosyaları
├── docs/                  # Dokümantasyon
│   ├── DEVICE_AGENT_ARCHITECTURE.md
│   ├── DEVICE_AGENT_IMPLEMENTATION_GUIDE.md
│   └── PowerShell_Integration.md
├── examples/              # Örnek kodlar
├── tests/                 # Test dosyaları
├── scripts/               # Kurulum ve yardımcı scriptler
├── requirements.txt       # Python bağımlılıkları
├── setup.py              # Kurulum scripti
└── README.md             # Bu dosya
```

## 🛠️ Kurulum

### Python Agent

```bash
# Repository'yi klonla
git clone https://github.com/your-repo/lxpcloud-device-agent.git
cd lxpcloud-device-agent

# Virtual environment oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# Konfigürasyon dosyasını düzenle
cp config/device_config.json.example config/device_config.json
# device_config.json dosyasını düzenle
```

### PowerShell Scriptleri (Windows)

```powershell
# PowerShell klasörüne git
cd PowerShell

# Debug testini çalıştır
.\debug_powershell_fixed.ps1

# Tek seferlik test
.\test_single_send.ps1

# Sürekli veri gönderimi
.\send_data_powershell_final.ps1
```

## 📖 Kullanım

### Python Agent

```bash
# Agent'ı başlat
python -m src.cli start

# Konfigürasyon ile başlat
python -m src.cli start --config config/device_config.json

# Debug modunda başlat
python -m src.cli start --debug
```

### PowerShell Scriptleri

```powershell
# Tek seferlik test
.\test_single_send.ps1

# Sürekli veri gönderimi (60 saniye aralık)
.\send_data_powershell_final.ps1

# Özel ayarlarla
.\send_data_powershell_final.ps1 -DeviceName "Production Server" -Interval 30

# Debug testi
.\debug_powershell_fixed.ps1
```

## 🔧 Konfigürasyon

### Python Agent Konfigürasyonu

```json
{
  "device": {
    "name": "My IoT Device",
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
    "file": "/var/log/lxpcloud-agent.log"
  }
}
```

### PowerShell Konfigürasyonu

PowerShell scriptlerinde API key ve URL doğrudan script içinde tanımlanmıştır:

```powershell
$API_KEY = "fce1ef45b2f31c8d8180cacbeaa593ad"
$API_URL = "https://app.lexpai.com/api/machine.php"
```

## 📊 Desteklenen Platformlar

### Python Agent
- **Raspberry Pi**: GPIO, I2C, SPI sensörleri
- **Arduino**: Arduino IDE ile C++ geliştirme
- **ESP32**: WiFi ve Bluetooth desteği
- **Generic Python**: Windows, Linux, macOS

### PowerShell Scriptleri
- **Windows**: Windows 7/Server 2008 R2 ve üzeri
- **PowerShell**: 5.1 ve üzeri
- **Sistem Metrikleri**: CPU, Memory, Disk kullanımı

## 🔒 Güvenlik

- **API Key Authentication**: Her cihaz için benzersiz API anahtarı
- **HTTPS Communication**: Tüm iletişim şifrelenmiş
- **Certificate Validation**: SSL sertifika doğrulaması
- **Error Handling**: Güvenli hata yönetimi

## 📈 Monitoring

### Python Agent
- Sistem kaynakları izleme
- Sensör verileri takibi
- Ağ bağlantısı durumu
- Hata oranları

### PowerShell Scriptleri
- Windows sistem metrikleri
- Ağ bağlantısı durumu
- API yanıt süreleri
- Başarı/başarısızlık istatistikleri

## 🐛 Sorun Giderme

### Python Agent

```bash
# Logları kontrol et
tail -f /var/log/lxpcloud-agent.log

# Debug modunda çalıştır
python -m src.cli start --debug

# Konfigürasyonu test et
python -m src.cli validate-config
```

### PowerShell Scriptleri

```powershell
# Debug scriptini çalıştır
.\debug_powershell_fixed.ps1

# Execution policy'yi kontrol et
Get-ExecutionPolicy

# Ağ bağlantısını test et
Test-Connection -ComputerName "app.lexpai.com"
```

## 📚 Dokümantasyon

- [Device Agent Architecture](docs/DEVICE_AGENT_ARCHITECTURE.md)
- [Implementation Guide](docs/DEVICE_AGENT_IMPLEMENTATION_GUIDE.md)
- [PowerShell Integration](docs/PowerShell_Integration.md)
- [Installation Guide](docs/installation.md)

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 Destek

- **Dokümantasyon**: [docs/](docs/) klasörü
- **Issues**: GitHub Issues
- **Email**: support@lexpai.com

## 🔄 Güncellemeler

### v1.0.0
- İlk sürüm
- Python agent implementasyonu
- PowerShell scriptleri eklendi
- Çok platformlu destek
- Güvenli API iletişimi

---

**LXPCloud Device Agent** - IoT cihazlarınızı LXPCloud platformuna bağlayın! 🚀 