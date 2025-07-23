#!/usr/bin/env python3
"""
LXPCloud Device Agent CLI
Command-line interface for agent management
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from .core.agent import LXPCloudAgent

def config_command(args):
    """Handle config command"""
    config_path = "/etc/lxpcloud-agent/device_config.json"
    
    if not Path(config_path).exists():
        print(f"❌ Configuration file not found: {config_path}")
        print("Run setup first: python3 -m lxpcloud_device_agent.setup")
        return 1
    
    if args.show:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(json.dumps(config, indent=2))
    
    if args.edit:
        import subprocess
        subprocess.run([os.environ.get('EDITOR', 'nano'), config_path])
    
    return 0

def status_command(args):
    """Handle status command"""
    import subprocess
    
    try:
        result = subprocess.run(['systemctl', 'status', 'lxpcloud-agent'], 
                              capture_output=True, text=True)
        print(result.stdout)
        return 0
    except FileNotFoundError:
        print("❌ systemctl not found. Are you on a systemd system?")
        return 1

def logs_command(args):
    """Handle logs command"""
    import subprocess
    
    try:
        cmd = ['journalctl', '-u', 'lxpcloud-agent']
        if args.follow:
            cmd.append('-f')
        if args.lines:
            cmd.extend(['-n', str(args.lines)])
        
        subprocess.run(cmd)
        return 0
    except FileNotFoundError:
        print("❌ journalctl not found. Are you on a systemd system?")
        return 1

def start_command(args):
    """Handle start command"""
    import subprocess
    
    try:
        subprocess.run(['systemctl', 'start', 'lxpcloud-agent'], check=True)
        print("✅ LXPCloud Agent started successfully")
        return 0
    except subprocess.CalledProcessError:
        print("❌ Failed to start LXPCloud Agent")
        return 1

def stop_command(args):
    """Handle stop command"""
    import subprocess
    
    try:
        subprocess.run(['systemctl', 'stop', 'lxpcloud-agent'], check=True)
        print("✅ LXPCloud Agent stopped successfully")
        return 0
    except subprocess.CalledProcessError:
        print("❌ Failed to stop LXPCloud Agent")
        return 1

def restart_command(args):
    """Handle restart command"""
    import subprocess
    
    try:
        subprocess.run(['systemctl', 'restart', 'lxpcloud-agent'], check=True)
        print("✅ LXPCloud Agent restarted successfully")
        return 0
    except subprocess.CalledProcessError:
        print("❌ Failed to restart LXPCloud Agent")
        return 1

def test_command(args):
    """Handle test command"""
    async def run_test():
        try:
            agent = LXPCloudAgent()
            await agent.connection.test_connection()
            print("✅ Connection test successful")
            return 0
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return 1
    
    return asyncio.run(run_test())

def main():
    parser = argparse.ArgumentParser(
        description="LXPCloud Device Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  lxpcloud-agent config --show          # Show current configuration
  lxpcloud-agent config --edit          # Edit configuration
  lxpcloud-agent status                 # Show service status
  lxpcloud-agent logs --follow          # Follow logs in real-time
  lxpcloud-agent start                  # Start the agent
  lxpcloud-agent stop                   # Stop the agent
  lxpcloud-agent restart                # Restart the agent
  lxpcloud-agent test                   # Test API connection
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configuration management')
    config_parser.add_argument('--show', action='store_true', help='Show current configuration')
    config_parser.add_argument('--edit', action='store_true', help='Edit configuration')
    config_parser.set_defaults(func=config_command)
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show service status')
    status_parser.set_defaults(func=status_command)
    
    # Logs command
    logs_parser = subparsers.add_parser('logs', help='Show service logs')
    logs_parser.add_argument('--follow', '-f', action='store_true', help='Follow logs')
    logs_parser.add_argument('--lines', '-n', type=int, help='Number of lines to show')
    logs_parser.set_defaults(func=logs_command)
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start the agent')
    start_parser.set_defaults(func=start_command)
    
    # Stop command
    stop_parser = subparsers.add_parser('stop', help='Stop the agent')
    stop_parser.set_defaults(func=stop_command)
    
    # Restart command
    restart_parser = subparsers.add_parser('restart', help='Restart the agent')
    restart_parser.set_defaults(func=restart_command)
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test API connection')
    test_parser.set_defaults(func=test_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main()) 