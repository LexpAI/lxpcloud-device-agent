#!/bin/bash

set -e

echo "🚀 LXPCloud Device Agent Installer"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Check Python version
print_status "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
required_version="3.7"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    print_error "Python 3.7 or higher is required. Current version: $python_version"
    exit 1
fi

print_success "Python version check passed: $python_version"

# Install system dependencies
print_status "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git curl wget

# Create virtual environment
print_status "Creating virtual environment..."
python3 -m venv ~/lxpcloud-agent-env
source ~/lxpcloud-agent-env/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install aiohttp asyncio-mqtt pyserial requests pydantic python-dotenv

# Create installation directory
INSTALL_DIR="/opt/lxpcloud-agent"
print_status "Creating installation directory: $INSTALL_DIR"
sudo mkdir -p $INSTALL_DIR

# Download agent (if not already present)
if [ ! -d "$INSTALL_DIR/.git" ]; then
    print_status "Downloading LXPCloud Device Agent..."
    sudo git clone https://github.com/lexpai/lxpcloud-device-agent.git $INSTALL_DIR
else
    print_status "Updating existing installation..."
    cd $INSTALL_DIR
    sudo git pull origin main
fi

# Install agent
print_status "Installing agent..."
cd $INSTALL_DIR
sudo python3 setup.py install

# Create systemd service
print_status "Creating system service..."
sudo tee /etc/systemd/system/lxpcloud-agent.service > /dev/null <<EOF
[Unit]
Description=LXPCloud Device Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 -m lxpcloud_device_agent
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
print_status "Enabling system service..."
sudo systemctl daemon-reload
sudo systemctl enable lxpcloud-agent

# Create configuration directory
print_status "Creating configuration directory..."
sudo mkdir -p /etc/lxpcloud-agent
sudo cp config/device_config.json /etc/lxpcloud-agent/device_config.json

print_success "Installation completed!"
echo ""
print_status "Next steps:"
echo "1. Configure your device: sudo python3 -m lxpcloud_device_agent.setup"
echo "2. Edit configuration: sudo nano /etc/lxpcloud-agent/device_config.json"
echo "3. Start the service: sudo systemctl start lxpcloud-agent"
echo "4. Check status: sudo systemctl status lxpcloud-agent"
echo "5. View logs: sudo journalctl -u lxpcloud-agent -f"
echo ""
print_status "For support: support@lexpai.com" 