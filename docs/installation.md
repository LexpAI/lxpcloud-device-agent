# LXPCloud Device Agent Installation Guide

## Quick Installation

### One-Command Installation

```bash
curl -sSL https://raw.githubusercontent.com/lexpai/lxpcloud-device-agent/main/scripts/install.sh | bash
```

This command will:
- Check Python version (requires 3.7+)
- Install system dependencies
- Create virtual environment
- Download and install the agent
- Create systemd service
- Set up configuration directory

### Manual Installation

If you prefer manual installation:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lexpai/lxpcloud-device-agent.git
   cd lxpcloud-device-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package**:
   ```bash
   python setup.py install
   ```

## Platform-Specific Installation

### Raspberry Pi

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv git

# Run installation
curl -sSL https://raw.githubusercontent.com/lexpai/lxpcloud-device-agent/main/scripts/install.sh | bash
```

### Ubuntu/Debian

```bash
# Install dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv git

# Run installation
curl -sSL https://raw.githubusercontent.com/lexpai/lxpcloud-device-agent/main/scripts/install.sh | bash
```

### CentOS/RHEL

```bash
# Install dependencies
sudo yum update -y
sudo yum install -y python3-pip git

# Run installation
curl -sSL https://raw.githubusercontent.com/lexpai/lxpcloud-device-agent/main/scripts/install.sh | bash
```

## Configuration

### Initial Setup

After installation, configure your device:

```bash
sudo python3 -m lxpcloud_device_agent.setup
```

This interactive wizard will:
- Ask for your LXPCloud API key
- Configure device information
- Set up sensor configuration
- Create the configuration file

### Manual Configuration

Edit the configuration file:

```bash
sudo nano /etc/lxpcloud-agent/device_config.json
```

Key configuration options:

```json
{
  "api": {
    "api_key": "your_api_key_here"
  },
  "device": {
    "name": "Your Device Name",
    "type": "device_type"
  },
  "sensors": {
    "temperature": {
      "enabled": true,
      "pin": 18
    }
  }
}
```

## Service Management

### Start the Service

```bash
sudo systemctl start lxpcloud-agent
```

### Check Status

```bash
sudo systemctl status lxpcloud-agent
```

### View Logs

```bash
sudo journalctl -u lxpcloud-agent -f
```

### Stop the Service

```bash
sudo systemctl stop lxpcloud-agent
```

### Enable Auto-Start

```bash
sudo systemctl enable lxpcloud-agent
```

## CLI Management

The agent includes a command-line interface:

```bash
# Show configuration
lxpcloud-agent config --show

# Edit configuration
lxpcloud-agent config --edit

# Check service status
lxpcloud-agent status

# View logs
lxpcloud-agent logs --follow

# Start/stop/restart
lxpcloud-agent start
lxpcloud-agent stop
lxpcloud-agent restart

# Test connection
lxpcloud-agent test
```

## Troubleshooting

### Common Issues

1. **Permission Denied**:
   ```bash
   sudo chown -R $USER:$USER /opt/lxpcloud-agent
   ```

2. **Python Version**:
   ```bash
   python3 --version  # Should be 3.7+
   ```

3. **Network Issues**:
   ```bash
   ping app.lexpai.com
   ```

4. **Service Won't Start**:
   ```bash
   sudo journalctl -u lxpcloud-agent -n 50
   ```

### Getting Help

- **Email**: support@lexpai.com
- **Documentation**: [docs.lexpai.com](https://docs.lexpai.com)
- **Platform**: [app.lexpai.com](https://app.lexpai.com) 