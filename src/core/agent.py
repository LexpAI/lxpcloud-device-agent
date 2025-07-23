import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json
import signal
import sys

from .connection import LXPConnection
from .data_collector import DataCollector
from .data_sender import DataSender
from ..protocols.lxp_protocol import LXPProtocol
from ..utils.logger import setup_logger

class LXPCloudAgent:
    """
    Main LXPCloud Device Agent
    Handles data collection, processing, and transmission
    """
    
    def __init__(self, config_path: str = "config/device_config.json"):
        self.config = self._load_config(config_path)
        self.logger = setup_logger(self.config['logging'])
        
        # Initialize components
        self.connection = LXPConnection(self.config['api'])
        self.data_collector = DataCollector(self.config['sensors'])
        self.data_sender = DataSender(self.connection)
        self.protocol = LXPProtocol()
        
        self.running = False
        self.data_buffer = []
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(self.stop())
        
    async def start(self):
        """Start the agent"""
        self.logger.info("Starting LXPCloud Device Agent")
        self.running = True
        
        try:
            # Test connection
            await self.connection.test_connection()
            self.logger.info("Connection test successful")
            
            # Start data collection loop
            await self._data_collection_loop()
            
        except Exception as e:
            self.logger.error(f"Agent startup failed: {e}")
            raise
    
    async def stop(self):
        """Stop the agent"""
        self.logger.info("Stopping LXPCloud Device Agent")
        self.running = False
        
        # Send remaining data
        if self.data_buffer:
            await self._send_buffered_data()
        
        # Cleanup
        await self.connection.close()
    
    async def _data_collection_loop(self):
        """Main data collection and transmission loop"""
        interval = self.config['data_collection']['interval']
        
        while self.running:
            try:
                # Collect data
                raw_data = await self.data_collector.collect_all()
                
                # Format data using LXP protocol
                formatted_data = self.protocol.format_data(
                    raw_data, 
                    self.config['device']
                )
                
                # Add to buffer
                self.data_buffer.append(formatted_data)
                
                # Send if buffer is full or interval reached
                if len(self.data_buffer) >= self.config['data_collection']['batch_size']:
                    await self._send_buffered_data()
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                self.logger.error(f"Data collection error: {e}")
                await asyncio.sleep(interval)
    
    async def _send_buffered_data(self):
        """Send buffered data to LXPCloud"""
        if not self.data_buffer:
            return
            
        try:
            # Send data in batches
            for data in self.data_buffer:
                success = await self.data_sender.send_data(data)
                if success:
                    self.logger.debug(f"Data sent successfully: {data['timestamp']['unix']}")
                else:
                    self.logger.warning("Failed to send data, will retry")
                    
            # Clear buffer on successful send
            self.data_buffer.clear()
            
        except Exception as e:
            self.logger.error(f"Data transmission error: {e}")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {e}")

async def main():
    """Main entry point"""
    agent = LXPCloudAgent()
    
    try:
        await agent.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(main()) 