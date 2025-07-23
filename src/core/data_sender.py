import asyncio
from typing import Dict, Any
from .connection import LXPConnection

class DataSender:
    """Handles data transmission to LXPCloud API"""
    
    def __init__(self, connection: LXPConnection):
        self.connection = connection
        self.retry_count = 0
        self.max_retries = 3
    
    async def send_data(self, data: Dict[str, Any]) -> bool:
        """Send data to LXPCloud API with retry logic"""
        for attempt in range(self.max_retries):
            try:
                success = await self.connection.send_data(data)
                if success:
                    self.retry_count = 0  # Reset retry count on success
                    return True
                else:
                    raise Exception("API returned failure status")
                    
            except Exception as e:
                self.retry_count += 1
                if attempt == self.max_retries - 1:
                    # Last attempt failed
                    print(f"Failed to send data after {self.max_retries} attempts: {e}")
                    return False
                else:
                    # Wait before retry with exponential backoff
                    wait_time = 2 ** attempt
                    print(f"Attempt {attempt + 1} failed, retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
        
        return False
    
    async def send_batch(self, data_batch: list) -> Dict[str, int]:
        """Send a batch of data records"""
        results = {
            'successful': 0,
            'failed': 0,
            'total': len(data_batch)
        }
        
        for data in data_batch:
            success = await self.send_data(data)
            if success:
                results['successful'] += 1
            else:
                results['failed'] += 1
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get transmission statistics"""
        return {
            'retry_count': self.retry_count,
            'max_retries': self.max_retries
        } 