import aiohttp
import asyncio
from typing import Dict, Any, Optional
import json

class LXPConnection:
    """Manages connection to LXPCloud API"""
    
    def __init__(self, config: Dict[str, Any]):
        self.base_url = config['base_url']
        self.endpoint = config['endpoint']
        self.api_key = config['api_key']
        self.timeout = config.get('timeout', 30)
        self.retry_attempts = config.get('retry_attempts', 3)
        
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_connection(self) -> bool:
        """Test connection to LXPCloud API"""
        try:
            url = f"{self.base_url}{self.endpoint}"
            params = {'api_key': self.api_key, 'test': '1'}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('status') == 'ok'
                return False
        except Exception as e:
            raise ConnectionError(f"Connection test failed: {e}")
    
    async def send_data(self, data: Dict[str, Any]) -> bool:
        """Send data to LXPCloud API"""
        for attempt in range(self.retry_attempts):
            try:
                url = f"{self.base_url}{self.endpoint}"
                payload = {
                    'api_key': self.api_key,
                    'payload': data,
                    'recorded_at': data['timestamp']['unix']
                }
                
                async with self.session.post(url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get('status') == 'ok'
                    else:
                        error_data = await response.json()
                        raise Exception(f"API Error: {error_data.get('error', 'Unknown error')}")
                        
            except Exception as e:
                if attempt == self.retry_attempts - 1:
                    raise e
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        return False
    
    async def close(self):
        """Close the connection"""
        if self.session:
            await self.session.close() 