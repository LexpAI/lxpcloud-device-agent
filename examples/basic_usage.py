#!/usr/bin/env python3
"""
Basic Usage Example for LXPCloud Device Agent
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lxpcloud_device_agent import LXPCloudAgent

async def main():
    """Basic usage example"""
    print("🚀 LXPCloud Device Agent - Basic Usage Example")
    print("=" * 50)
    
    # Initialize agent with custom config path
    config_path = "../config/device_config.json"
    agent = LXPCloudAgent(config_path)
    
    try:
        print("Starting LXPCloud Device Agent...")
        await agent.start()
        
        # Keep running for a while to see data collection
        print("Agent is running. Press Ctrl+C to stop...")
        await asyncio.sleep(30)  # Run for 30 seconds
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await agent.stop()
        print("Agent stopped.")

if __name__ == "__main__":
    asyncio.run(main()) 