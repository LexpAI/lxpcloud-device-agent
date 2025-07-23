# LXPCloud PowerShell Debug Script (Fixed)
# API Key: fce1ef45b2f31c8d8180cacbeaa593ad

Write-Host "🔍 LXPCloud PowerShell Debug Script (Fixed)" -ForegroundColor Blue
Write-Host "===========================================" -ForegroundColor Blue
Write-Host ""

# Configuration
$API_KEY = "fce1ef45b2f31c8d8180cacbeaa593ad"
$API_URL = "https://app.lexpai.com/api/machine.php"

# Test 1: PowerShell Version
Write-Host "1. Testing PowerShell Version..." -ForegroundColor Yellow
Write-Host "PowerShell Version: $($PSVersionTable.PSVersion)" -ForegroundColor White
Write-Host ""

# Test 2: Execution Policy
Write-Host "2. Testing Execution Policy..." -ForegroundColor Yellow
$executionPolicy = Get-ExecutionPolicy
Write-Host "Execution Policy: $executionPolicy" -ForegroundColor White
if ($executionPolicy -eq "Restricted") {
    Write-Host "⚠️  Warning: Execution policy is Restricted. Scripts may not run." -ForegroundColor Red
}
Write-Host ""

# Test 3: Network Connectivity
Write-Host "3. Testing Network Connectivity..." -ForegroundColor Yellow
try {
    $ping = Test-Connection -ComputerName "app.lexpai.com" -Count 1 -Quiet
    if ($ping) {
        Write-Host "✅ Network connectivity: OK" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Network connectivity: Failed" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ Network connectivity: Error - $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 4: API Connection Test
Write-Host "4. Testing API Connection..." -ForegroundColor Yellow
try {
    $headers = @{
        "Content-Type" = "application/json"
        "User-Agent" = "LXPCloud-PowerShell-Debug/1.0"
    }
    
    # Test with a simple GET request to check if API is reachable
    # The API doesn't support test parameter, so we'll just check if it responds
    Write-Host "Testing API endpoint: $API_URL" -ForegroundColor White
    
    $response = Invoke-RestMethod -Uri $API_URL -Method GET -Headers $headers -TimeoutSec 10
    
    # If we get here, the API is reachable
    Write-Host "✅ API connection: OK (Endpoint is reachable)" -ForegroundColor Green
    Write-Host "Response received from API" -ForegroundColor White
}
catch {
    if ($_.Exception.Response.StatusCode -eq 405) {
        Write-Host "✅ API connection: OK (Method not allowed is expected for GET without parameters)" -ForegroundColor Green
    }
    else {
        Write-Host "❌ API connection: Error - $($_.Exception.Message)" -ForegroundColor Red
    }
}
Write-Host ""

# Test 5: System Metrics
Write-Host "5. Testing System Metrics..." -ForegroundColor Yellow
try {
    # CPU
    try {
        $cpu = Get-Counter "\Processor(_Total)\% Processor Time" -ErrorAction Stop
        Write-Host "✅ CPU counter: OK - $($cpu.CounterSamples.CookedValue)%" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ CPU counter: Failed - $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Memory
    try {
        $memory = Get-Counter "\Memory\% Committed Bytes In Use" -ErrorAction Stop
        Write-Host "✅ Memory counter: OK - $($memory.CounterSamples.CookedValue)%" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Memory counter: Failed - $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Disk
    try {
        $disk = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'" -ErrorAction Stop
        if ($disk) {
            $diskUsage = [math]::Round((($disk.Size - $disk.FreeSpace) / $disk.Size) * 100, 2)
            Write-Host "✅ Disk counter: OK - $diskUsage%" -ForegroundColor Green
        }
        else {
            Write-Host "❌ Disk counter: No C: drive found" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "❌ Disk counter: Failed - $($_.Exception.Message)" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ System metrics: Error - $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 6: Network Info
Write-Host "6. Testing Network Info..." -ForegroundColor Yellow
try {
    $hostname = $env:COMPUTERNAME
    Write-Host "✅ Hostname: $hostname" -ForegroundColor Green
    
    try {
        $networkInterfaces = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction Stop
        $ethernet = $networkInterfaces | Where-Object { $_.InterfaceAlias -like "*Ethernet*" } | Select-Object -First 1
        if ($ethernet) {
            Write-Host "✅ IP Address: $($ethernet.IPAddress)" -ForegroundColor Green
        }
        else {
            $wifi = $networkInterfaces | Where-Object { $_.InterfaceAlias -like "*Wi-Fi*" } | Select-Object -First 1
            if ($wifi) {
                Write-Host "✅ IP Address: $($wifi.IPAddress)" -ForegroundColor Green
            }
            else {
                Write-Host "❌ No network interface found" -ForegroundColor Red
            }
        }
    }
    catch {
        Write-Host "❌ Network info: Failed - $($_.Exception.Message)" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ Network info: Error - $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 7: JSON Conversion
Write-Host "7. Testing JSON Conversion..." -ForegroundColor Yellow
try {
    $testData = @{
        test = "data"
        number = 123
        array = @(1, 2, 3)
    }
    
    $json = $testData | ConvertTo-Json -Depth 10 -Compress
    Write-Host "✅ JSON conversion: OK" -ForegroundColor Green
    Write-Host "JSON: $json" -ForegroundColor White
}
catch {
    Write-Host "❌ JSON conversion: Failed - $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 8: Single Data Send
Write-Host "8. Testing Single Data Send..." -ForegroundColor Yellow
try {
    $timestamp = [DateTimeOffset]::UtcNow
    
    $testData = @{
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
                    value = 25.5
                    unit = "%"
                    status = "normal"
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
                hostname = $env:COMPUTERNAME
                ip_address = "192.168.1.100"
                connection_type = "ethernet"
            }
        }
    }
    
    $payload = @{
        api_key = $API_KEY
        payload = $testData
        recorded_at = $testData.timestamp.unix
    }
    
    $jsonPayload = $payload | ConvertTo-Json -Depth 10 -Compress
    
    Write-Host "Sending test data..." -ForegroundColor Yellow
    Write-Host "Payload size: $($jsonPayload.Length) bytes" -ForegroundColor White
    
    $headers = @{
        "Content-Type" = "application/json"
        "User-Agent" = "LXPCloud-PowerShell-Debug/1.0"
    }
    
    $response = Invoke-RestMethod -Uri $API_URL -Method POST -Body $jsonPayload -Headers $headers -TimeoutSec 30
    
    if ($response.status -eq "ok") {
        Write-Host "✅ Single data send: OK" -ForegroundColor Green
        Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor White
    }
    else {
        Write-Host "❌ Single data send: Failed - $($response.error)" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ Single data send: Error - $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

Write-Host "🔍 Debug completed!" -ForegroundColor Blue 