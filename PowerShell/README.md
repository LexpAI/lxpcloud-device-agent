# LXPCloud PowerShell Scripts

Bu klasör LXPCloud API'sine veri göndermek için PowerShell scriptlerini içerir.

## Dosyalar

- `test_single_send.ps1` - Tek seferlik test veri gönderimi
- `send_data_powershell_final.ps1` - Sürekli veri gönderimi scripti
- `debug_powershell_fixed.ps1` - Debug ve test scripti

## Kullanım

### Tek Seferlik Test
```powershell
.\test_single_send.ps1
```

### Sürekli Veri Gönderimi
```powershell
# Varsayılan ayarlarla (60 saniye)
.\send_data_powershell_final.ps1

# Özel ayarlarla
.\send_data_powershell_final.ps1 -DeviceName "My PC" -Interval 30
```

### Debug Testi
```powershell
.\debug_powershell_fixed.ps1
```

## API Key

Scriptlerde kullanılan API Key: `fce1ef45b2f31c8d8180cacbeaa593ad`

## Gereksinimler

- PowerShell 5.1 veya üzeri
- Windows işletim sistemi
- İnternet bağlantısı
- Execution Policy: RemoteSigned veya Unrestricted

## Sorun Giderme

1. **Execution Policy Hatası**: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
2. **Ağ Bağlantısı**: `Test-Connection -ComputerName "app.lexpai.com"`
3. **API Bağlantısı**: Debug scriptini çalıştırın 