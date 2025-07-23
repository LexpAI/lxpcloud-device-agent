# LXPCloud Single Test Send - PowerShell Script
# API Key: fce1ef45b2f31c8d8180cacbeaa593ad

Write-Host "🚀 LXPCloud Single Test Send" -ForegroundColor Blue
Write-Host "============================" -ForegroundColor Blue
Write-Host ""

# Configuration
$API_KEY = "fce1ef45b2f31c8d8180cacbeaa593ad"
$API_URL = "https://app.lexpai.com/api/machine.php"

# Get system metrics
Write-Host "Collecting system metrics..." -ForegroundColor Yellow

try {
    # CPU Usage
    $cpu = Get-Counter "\Processor(_Total)\% Processor Time"
    $cpuUsage = [math]::Round($cpu.CounterSamples.CookedValue, 2)
    
    # Memory Usage
    $memory = Get-Counter "\Memory\% Committed Bytes In Use"
    $memoryUsage = [math]::Round($memory.CounterSamples.CookedValue, 2)
    
    # Disk Usage
    $disk = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'"
    $diskUsage = [math]::Round((($disk.Size - $disk.FreeSpace) / $disk.Size) * 100, 2)
    
    Write-Host "✅ System metrics collected successfully" -ForegroundColor Green
    Write-Host "CPU: $cpuUsage% | Memory: $memoryUsage% | Disk: $diskUsage%" -ForegroundColor White
}
catch {
    Write-Host "❌ Error collecting system metrics: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Get network info
Write-Host "Collecting network info..." -ForegroundColor Yellow

try {
    $hostname = $env:COMPUTERNAME
    $networkInterfaces = Get-NetIPAddress -AddressFamily IPv4
    $ethernet = $networkInterfaces | Where-Object { $_.InterfaceAlias -like "*Ethernet*" } | Select-Object -First 1
    $ipAddress = if ($ethernet) { $ethernet.IPAddress } else { "0.0.0.0" }
    
    Write-Host "✅ Network info collected successfully" -ForegroundColor Green
    Write-Host "Hostname: $hostname | IP: $ipAddress" -ForegroundColor White
}
catch {
    Write-Host "❌ Error collecting network info: $($_.Exception.Message)" -ForegroundColor Red
    $hostname = $env:COMPUTERNAME
    $ipAddress = "0.0.0.0"
}

# Create timestamp
$timestamp = [DateTimeOffset]::UtcNow

# Format data according to LXPCloud protocol
$lxpData = @{
    lxp_version = "1.0"
    device_info = @{
        device_id = [System.Guid]::NewGuid().ToString()
        device_type = "windows_pc"
        firmware_version = "1.0.0"
        hardware_version = "1.0.0"
    }
    timestamp = @{
        unix = [long]($timestamp.ToUnixTimeSeconds())
        iso = $timestamp.ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
        timezone = "UTC"
    }
    data = @{
        sensors = @{}
        metrics = @{
            cpu_usage = @{
                value = $cpuUsage
                unit = "%"
                status = if ($cpuUsage -gt 80) { "warning" } else { "normal" }
            }
            memory_usage = @{
                value = $memoryUsage
                unit = "%"
                status = if ($memoryUsage -gt 85) { "warning" } else { "normal" }
            }
            disk_usage = @{
                value = $diskUsage
                unit = "%"
                status = if ($diskUsage -gt 90) { "warning" } else { "normal" }
            }
        }
        alarms = @()
        status = @{
            operational = $true
            maintenance_required = $false
            last_maintenance = $null
        }
    }
    metadata = @{
        location = @{
            latitude = 41.0082
            longitude = 28.9784
            altitude = 100
        }
        environment = @{
            ambient_temperature = 22.0
            ambient_humidity = 45.0
        }
        network = @{
            hostname = $hostname
            ip_address = $ipAddress
            connection_type = "ethernet"
        }
    }
}

# Create payload
$payload = @{
    api_key = $API_KEY
    payload = $lxpData
    recorded_at = $lxpData.timestamp.unix
}

# Convert to JSON
$jsonPayload = $payload | ConvertTo-Json -Depth 10 -Compress

Write-Host "Preparing to send data..." -ForegroundColor Yellow
Write-Host "Payload size: $($jsonPayload.Length) bytes" -ForegroundColor White
Write-Host ""

# Send data
Write-Host "Sending data to LXPCloud..." -ForegroundColor Blue

try {
    $headers = @{
        "Content-Type" = "application/json"
        "User-Agent" = "LXPCloud-PowerShell-Test/1.0"
    }
    
    $response = Invoke-RestMethod -Uri $API_URL -Method POST -Body $jsonPayload -Headers $headers -TimeoutSec 30
    
    if ($response.status -eq "ok") {
        Write-Host "✅ Data sent successfully!" -ForegroundColor Green
        Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor White
    }
    else {
        Write-Host "❌ API returned error: $($response.error)" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ Error sending data: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode
        Write-Host "HTTP Status Code: $statusCode" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Test completed!" -ForegroundColor Blue 