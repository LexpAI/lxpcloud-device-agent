# LXPCloud PowerShell Integration

Bu doküman LXPCloud API'sine PowerShell scriptleri ile veri gönderme işlemlerini açıklar.

## Genel Bakış

PowerShell scriptleri Windows ortamında LXPCloud API'sine sistem metriklerini göndermek için kullanılır. Bu scriptler:

- Sistem metriklerini toplar (CPU, Memory, Disk)
- Ağ bilgilerini alır
- LXPCloud JSON protokolüne uygun veri formatlar
- HTTPS üzerinden API'ye gönderir

## Dosya Yapısı

```
lxpcloud-device-agent/
└── PowerShell/
    ├── README.md                    # PowerShell scriptleri genel bilgi
    ├── test_single_send.ps1         # Tek seferlik test gönderimi
    ├── send_data_powershell_final.ps1 # Sürekli veri gönderimi
    └── debug_powershell_fixed.ps1   # Debug ve test scripti
```

## API Konfigürasyonu

### API Key
```powershell
$API_KEY = "fce1ef45b2f31c8d8180cacbeaa593ad"
```

### API Endpoint
```powershell
$API_URL = "https://app.lexpai.com/api/machine.php"
```

## Kullanım Senaryoları

### 1. Tek Seferlik Test
```powershell
.\test_single_send.ps1
```

**Özellikler:**
- Sistem metriklerini bir kez toplar
- Veriyi API'ye gönderir
- Sonucu gösterir ve çıkar

### 2. Sürekli Veri Gönderimi
```powershell
# Varsayılan ayarlarla (60 saniye aralık)
.\send_data_powershell_final.ps1

# Özel ayarlarla
.\send_data_powershell_final.ps1 -DeviceName "Production Server" -Interval 30
```

**Özellikler:**
- Belirtilen aralıklarla sürekli veri toplar
- İstatistikleri gösterir
- Hata durumlarını yönetir
- Ctrl+C ile durdurulabilir

### 3. Debug ve Test
```powershell
.\debug_powershell_fixed.ps1
```

**Test Edilen Öğeler:**
- PowerShell versiyonu
- Execution policy
- Ağ bağlantısı
- API bağlantısı
- Sistem metrikleri
- Ağ bilgileri
- JSON dönüşümü
- Tek seferlik veri gönderimi

## Veri Formatı

### LXPCloud JSON Protokolü
```json
{
  "api_key": "fce1ef45b2f31c8d8180cacbeaa593ad",
  "payload": {
    "lxp_version": "1.0",
    "device_info": {
      "device_id": "uuid",
      "device_type": "windows_pc",
      "firmware_version": "1.0.0",
      "hardware_version": "1.0.0"
    },
    "timestamp": {
      "unix": 1234567890,
      "iso": "2023-12-07T10:30:00.000Z",
      "timezone": "UTC"
    },
    "data": {
      "sensors": {},
      "metrics": {
        "cpu_usage": {
          "value": 25.5,
          "unit": "%",
          "status": "normal"
        },
        "memory_usage": {
          "value": 45.2,
          "unit": "%",
          "status": "normal"
        },
        "disk_usage": {
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
        "hostname": "COMPUTERNAME",
        "ip_address": "192.168.1.100",
        "connection_type": "ethernet"
      }
    }
  },
  "recorded_at": 1234567890
}
```

## Sistem Gereksinimleri

### Minimum Gereksinimler
- Windows 7/Server 2008 R2 veya üzeri
- PowerShell 5.1 veya üzeri
- İnternet bağlantısı
- Execution Policy: RemoteSigned veya Unrestricted

### Önerilen Gereksinimler
- Windows 10/Server 2016 veya üzeri
- PowerShell 7.0 veya üzeri
- Yönetici hakları (bazı sistem metrikleri için)

## Kurulum ve Yapılandırma

### 1. Execution Policy Ayarlama
```powershell
# Mevcut policy'yi kontrol et
Get-ExecutionPolicy

# Policy'yi ayarla (gerekirse)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Scriptleri İndirme
Scriptleri `lxpcloud-device-agent/PowerShell/` klasörüne kopyalayın.

### 3. API Key Güncelleme
Gerekirse scriptlerdeki API key'i güncelleyin:
```powershell
$API_KEY = "your_new_api_key_here"
```

## Sorun Giderme

### Yaygın Sorunlar

#### 1. Execution Policy Hatası
```
File cannot be loaded because running scripts is disabled on this system.
```

**Çözüm:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 2. Ağ Bağlantısı Sorunu
```
The remote server returned an error: (400) Bad Request.
```

**Çözüm:**
- İnternet bağlantısını kontrol edin
- Firewall ayarlarını kontrol edin
- API endpoint'inin doğru olduğundan emin olun

#### 3. Sistem Metrikleri Hatası
```
Get-Counter : The specified object was not found on the computer.
```

**Çözüm:**
- Yönetici haklarıyla çalıştırın
- Performance Counter servisinin çalıştığından emin olun

### Debug Adımları

1. **Debug scriptini çalıştırın:**
   ```powershell
   .\debug_powershell_fixed.ps1
   ```

2. **Ağ bağlantısını test edin:**
   ```powershell
   Test-Connection -ComputerName "app.lexpai.com"
   ```

3. **PowerShell versiyonunu kontrol edin:**
   ```powershell
   $PSVersionTable.PSVersion
   ```

## Güvenlik

### API Key Güvenliği
- API key'i güvenli bir şekilde saklayın
- Scriptleri paylaşırken API key'i değiştirin
- Production ortamında environment variable kullanın

### Ağ Güvenliği
- HTTPS bağlantısı kullanılır
- Firewall kurallarını kontrol edin
- Proxy ayarlarını yapılandırın (gerekirse)

## Performans

### Optimizasyon Önerileri
- Veri gönderim aralığını ihtiyaca göre ayarlayın
- Sistem kaynaklarını izleyin
- Log dosyalarını düzenli olarak temizleyin

### Monitoring
- Script çalışma durumunu izleyin
- Başarısız gönderimleri takip edin
- Sistem performansını kontrol edin

## Geliştirme

### Yeni Metrikler Ekleme
1. `Get-SystemMetrics` fonksiyonunu güncelleyin
2. `Format-LXPData` fonksiyonunda yeni metrikleri ekleyin
3. Test edin ve doğrulayın

### Özel Sensörler
1. Yeni sensör fonksiyonları oluşturun
2. Veri formatını güncelleyin
3. API'ye uygun şekilde gönderin

## Destek

Sorunlar için:
1. Debug scriptini çalıştırın
2. Hata mesajlarını kaydedin
3. Sistem bilgilerini toplayın
4. LXPCloud destek ekibiyle iletişime geçin 