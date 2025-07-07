#!/usr/bin/env python3
"""
Redis connection test script for debugging Render deployment issues.
Usage: python test_redis.py
"""

import os
import sys

def test_redis_connection():
    """Test Redis connection with the provided REDIS_URL"""
    
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        print("❌ REDIS_URL environment variable not set")
        return False
    
    print(f"🔍 Testing Redis connection...")
    print(f"📍 REDIS_URL: {redis_url[:20]}...{redis_url[-10:]}")  # Hide sensitive parts
    
    try:
        import redis
        
        # Test basic connection
        client = redis.from_url(redis_url)
        
        # Test ping
        result = client.ping()
        if result:
            print("✅ Redis PING successful")
        
        # Test basic operations
        client.set("test_key", "test_value", ex=60)
        value = client.get("test_key")
        if value == b"test_value":
            print("✅ Redis SET/GET operations successful")
        
        # Clean up
        client.delete("test_key")
        
        print("🎉 Redis connection test PASSED")
        return True
        
    except redis.ConnectionError as e:
        print(f"❌ Redis connection error: {e}")
        return False
    except redis.AuthenticationError as e:
        print(f"❌ Redis authentication error: {e}")
        return False
    except Exception as e:
        print(f"❌ Redis error: {e}")
        return False

def diagnose_redis_url():
    """Diagnose common Redis URL format issues"""
    
    redis_url = os.getenv("REDIS_URL", "")
    
    print("\n🔍 Redis URL Diagnosis:")
    print(f"📍 URL Length: {len(redis_url)} characters")
    
    if not redis_url:
        print("❌ REDIS_URL is empty")
        return
    
    if not redis_url.startswith(("redis://", "rediss://")):
        print("⚠️ URL should start with 'redis://' or 'rediss://'")
    
    if "@" not in redis_url:
        print("⚠️ URL might be missing authentication info")
    
    if "upstash.io" in redis_url:
        print("✅ Detected Upstash Redis service")
        if not redis_url.startswith("rediss://"):
            print("⚠️ Upstash usually requires SSL (rediss://)")
    
    # Parse URL components
    try:
        from urllib.parse import urlparse
        parsed = urlparse(redis_url)
        print(f"📍 Host: {parsed.hostname}")
        print(f"📍 Port: {parsed.port}")
        print(f"📍 Username: {parsed.username}")
        print(f"📍 Has Password: {'Yes' if parsed.password else 'No'}")
        print(f"📍 SSL: {'Yes' if parsed.scheme == 'rediss' else 'No'}")
    except Exception as e:
        print(f"❌ Failed to parse URL: {e}")

if __name__ == "__main__":
    print("🚀 Redis Connection Test")
    print("=" * 50)
    
    diagnose_redis_url()
    print("\n" + "=" * 50)
    
    success = test_redis_connection()
    
    if success:
        print("\n✅ All tests passed! Redis is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Redis connection failed. Check the diagnosis above.")
        sys.exit(1) 