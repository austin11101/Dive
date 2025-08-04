import redis.asyncio as redis
from app.core.config import settings

# Create Redis client
redis_client = redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)

# Cache configuration
CACHE_EXPIRE_TIME = 3600  # 1 hour in seconds


async def get_cache(key: str):
    """Get value from cache"""
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"Cache get error: {e}")
        return None


async def set_cache(key: str, value: str, expire: int = CACHE_EXPIRE_TIME):
    """Set value in cache with expiration"""
    try:
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"Cache set error: {e}")
        return False


async def delete_cache(key: str):
    """Delete value from cache"""
    try:
        await redis_client.delete(key)
        return True
    except Exception as e:
        print(f"Cache delete error: {e}")
        return False
