# LXPCloud Data Sender - PowerShell Script (Final Fixed Version)
# API Key: fce1ef45b2f31c8d8180cacbeaa593ad

param(
    [string]$DeviceName = "Windows Device",
    [string]$DeviceType = "windows_pc",
    [int]$Interval = 60
)

# Configuration
$API_KEY = "fce1ef45b2f31c8d8180cacbeaa593ad"
$API_URL = "https://app.lexpai.com/api/machine.php"

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"
$White = "White"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = $White
    )
    Write-Host $Message -ForegroundColor $Color
}

function Get-SystemMetrics {
    try {
        # Get CPU usage with error handling
        $cpu = 0
        try {
            $cpuCounter = Get-Counter "\Processor(_Total)\% Processor Time" -ErrorAction Stop
            $cpu = $cpuCounter.CounterSamples.CookedValue
        }
        catch {
            Write-ColorOutput "Warning: Could not get CPU usage, using default value" $Yellow
            $cpu = 25.0
        }
        
        # Get memory usage with error handling
        $memory = 0
        try {
            $memoryCounter = Get-Counter "\Memory\% Committed Bytes In Use" -ErrorAction Stop
            $memory = $memoryCounter.CounterSamples.CookedValue
        }
        catch {
            Write-ColorOutput "Warning: Could not get memory usage, using default value" $Yellow
            $memory = 50.0
        }
        
        # Get disk usage with error handling
        $disk = 0
        try {
            $diskInfo = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'" -ErrorAction Stop
            if ($diskInfo) {
                $disk = [math]::Round((($diskInfo.Size - $diskInfo.FreeSpace) / $diskInfo.Size) * 100, 2)
            }
            else {
                $disk = 65.0
            }
        }
        catch {
            Write-ColorOutput "Warning: Could not get disk usage, using default value" $Yellow
            $disk = 65.0
        }
        
        return @{
            cpu_usage = [math]::Round($cpu, 2)
            memory_usage = [math]::Round($memory, 2)
            disk_usage = $disk
        }
    }
    catch {
        Write-ColorOutput "Error getting system metrics: $($_.Exception.Message)" $Red
        return @{
            cpu_usage = 25.0
            memory_usage = 50.0
            disk_usage = 65.0
        }
    }
}

function Get-NetworkInfo {
    try {
        $ip = "0.0.0.0"
        
        # Try to get IP address
        try {
            $networkInterfaces = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction Stop
            $ethernet = $networkInterfaces | Where-Object { $_.InterfaceAlias -like "*Ethernet*" } | Select-Object -First 1
            if ($ethernet) {
                $ip = $ethernet.IPAddress
            }
            else {
                $wifi = $networkInterfaces | Where-Object { $_.InterfaceAlias -like "*Wi-Fi*" } | Select-Object -First 1
                if ($wifi) {
                    $ip = $wifi.IPAddress
                }
            }
        }
        catch {
            Write-ColorOutput "Warning: Could not get network info, using default" $Yellow
        }
        
        return @{
            hostname = $env:COMPUTERNAME
            ip_address = $ip
            connection_type = "ethernet"
        }
    }
    catch {
        Write-ColorOutput "Error getting network info: $($_.Exception.Message)" $Red
        return @{
            hostname = $env:COMPUTERNAME
            ip_address = "0.0.0.0"
            connection_type = "ethernet"
        }
    }
}

function Get-LocationInfo {
    # Default to Istanbul coordinates
    return @{
        latitude = 41.0082
        longitude = 28.9784
        altitude = 100
    }
}

function Format-LXPData {
    param(
        [hashtable]$SystemMetrics,
        [hashtable]$NetworkInfo,
        [hashtable]$LocationInfo
    )
    
    try {
        $timestamp = [DateTimeOffset]::UtcNow
        
        $data = @{
            lxp_version = "1.0"
            device_info = @{
                device_id = [System.Guid]::NewGuid().ToString()
                device_type = $DeviceType
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
                        value = $SystemMetrics.cpu_usage
                        unit = "%"
                        status = if ($SystemMetrics.cpu_usage -gt 80) { "warning" } else { "normal" }
                    }
                    memory_usage = @{
                        value = $SystemMetrics.memory_usage
                        unit = "%"
                        status = if ($SystemMetrics.memory_usage -gt 85) { "warning" } else { "normal" }
                    }
                    disk_usage = @{
                        value = $SystemMetrics.disk_usage
                        unit = "%"
                        status = if ($SystemMetrics.disk_usage -gt 90) { "warning" } else { "normal" }
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
                location = $LocationInfo
                environment = @{
                    ambient_temperature = 22.0
                    ambient_humidity = 45.0
                }
                network = $NetworkInfo
            }
        }
        
        return $data
    }
    catch {
        Write-ColorOutput "Error formatting data: $($_.Exception.Message)" $Red
        return $null
    }
}

function Send-LXPData {
    param(
        [hashtable]$Data
    )
    
    if (-not $Data) {
        Write-ColorOutput "❌ No data to send" $Red
        return $false
    }
    
    try {
        $payload = @{
            api_key = $API_KEY
            payload = $Data
            recorded_at = $Data.timestamp.unix
        }
        
        $jsonPayload = $payload | ConvertTo-Json -Depth 10 -Compress
        
        Write-ColorOutput "Sending data to LXPCloud..." $Blue
        Write-ColorOutput "Payload size: $($jsonPayload.Length) bytes" $Yellow
        
        $headers = @{
            "Content-Type" = "application/json"
            "User-Agent" = "LXPCloud-PowerShell-Agent/1.0"
        }
        
        $response = Invoke-RestMethod -Uri $API_URL -Method POST -Body $jsonPayload -Headers $headers -TimeoutSec 30
        
        if ($response.status -eq "ok") {
            Write-ColorOutput "✅ Data sent successfully!" $Green
            return $true
        }
        else {
            Write-ColorOutput "❌ API returned error: $($response.error)" $Red
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Error sending data: $($_.Exception.Message)" $Red
        return $false
    }
}

function Test-LXPConnection {
    try {
        Write-ColorOutput "Testing connection to LXPCloud..." $Yellow
        
        $headers = @{
            "Content-Type" = "application/json"
            "User-Agent" = "LXPCloud-PowerShell-Agent/1.0"
        }
        
        # Test with a simple GET request to check if API is reachable
        # The API doesn't support test parameter, so we'll just check if it responds
        $response = Invoke-RestMethod -Uri $API_URL -Method GET -Headers $headers -TimeoutSec 10
        
        # If we get here, the API is reachable
        Write-ColorOutput "✅ Connection test successful!" $Green
        return $true
    }
    catch {
        if ($_.Exception.Response.StatusCode -eq 405) {
            Write-ColorOutput "✅ Connection test successful! (Method not allowed is expected for GET without parameters)" $Green
            return $true
        }
        else {
            Write-ColorOutput "❌ Connection test failed: $($_.Exception.Message)" $Red
            return $false
        }
    }
}

# Main execution
Write-ColorOutput "🚀 LXPCloud PowerShell Data Sender (Final Fixed)" $Blue
Write-ColorOutput "===============================================" $Blue
Write-ColorOutput "Device: $DeviceName" $White
Write-ColorOutput "Type: $DeviceType" $White
Write-ColorOutput "Interval: $Interval seconds" $White
Write-ColorOutput "API URL: $API_URL" $White
Write-ColorOutput ""

# Test connection first
if (-not (Test-LXPConnection)) {
    Write-ColorOutput "Connection test failed. Exiting..." $Red
    exit 1
}

Write-ColorOutput "Starting data collection loop..." $Green
Write-ColorOutput "Press Ctrl+C to stop" $Yellow
Write-ColorOutput ""

$successCount = 0
$errorCount = 0

try {
    while ($true) {
        $startTime = Get-Date
        
        try {
            # Collect system data
            $systemMetrics = Get-SystemMetrics
            $networkInfo = Get-NetworkInfo
            $locationInfo = Get-LocationInfo
            
            # Format data
            $lxpData = Format-LXPData -SystemMetrics $systemMetrics -NetworkInfo $networkInfo -LocationInfo $locationInfo
            
            if ($lxpData) {
                # Send data
                if (Send-LXPData -Data $lxpData) {
                    $successCount++
                }
                else {
                    $errorCount++
                }
            }
            else {
                $errorCount++
                Write-ColorOutput "❌ Failed to format data" $Red
            }
        }
        catch {
            $errorCount++
            Write-ColorOutput "❌ Error in main loop: $($_.Exception.Message)" $Red
        }
        
        # Display statistics
        Write-ColorOutput "--- Statistics ---" $Blue
        Write-ColorOutput "Successful sends: $successCount" $Green
        Write-ColorOutput "Failed sends: $errorCount" $Red
        Write-ColorOutput "CPU: $($systemMetrics.cpu_usage)% | Memory: $($systemMetrics.memory_usage)% | Disk: $($systemMetrics.disk_usage)%" $White
        Write-ColorOutput ""
        
        # Wait for next interval
        $endTime = Get-Date
        $elapsed = ($endTime - $startTime).TotalSeconds
        $waitTime = [math]::Max(0, $Interval - $elapsed)
        
        if ($waitTime -gt 0) {
            Write-ColorOutput "Waiting $waitTime seconds until next send..." $Yellow
            Start-Sleep -Seconds $waitTime
        }
    }
}
catch {
    Write-ColorOutput "Script interrupted: $($_.Exception.Message)" $Red
}
finally {
    Write-ColorOutput ""
    Write-ColorOutput "=== Final Statistics ===" $Blue
    Write-ColorOutput "Total successful sends: $successCount" $Green
    Write-ColorOutput "Total failed sends: $errorCount" $Red
    Write-ColorOutput "Script finished." $White
} 