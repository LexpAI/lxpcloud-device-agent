import hashlib
import hmac
import base64
from typing import Dict, Any

class CryptoUtils:
    """Cryptographic utilities for LXPCloud protocol"""
    
    @staticmethod
    def hash_data(data: str) -> str:
        """Create SHA-256 hash of data"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def create_hmac(data: str, secret: str) -> str:
        """Create HMAC signature"""
        return hmac.new(
            secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def encode_base64(data: bytes) -> str:
        """Encode data to base64"""
        return base64.b64encode(data).decode()
    
    @staticmethod
    def decode_base64(data: str) -> bytes:
        """Decode base64 data"""
        return base64.b64decode(data)
    
    @staticmethod
    def sign_payload(payload: Dict[str, Any], secret: str) -> str:
        """Sign payload with HMAC"""
        # Convert payload to sorted JSON string
        import json
        payload_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        return CryptoUtils.create_hmac(payload_str, secret) 