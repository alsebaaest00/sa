"""Caching utilities for SA platform"""

import hashlib
import json
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, Optional


class CacheManager:
    """Simple file-based cache manager"""

    def __init__(self, cache_dir: str = "data/cache", ttl: int = 86400):
        """
        Initialize cache manager

        Args:
            cache_dir: Directory to store cache files
            ttl: Time to live in seconds (default 24 hours)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl

    def _get_cache_key(self, key: str) -> str:
        """Generate cache file path from key"""
        # Hash the key to create a filename
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return str(self.cache_dir / f"{key_hash}.json")

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        cache_file = self._get_cache_key(key)
        cache_path = Path(cache_file)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, "r") as f:
                data = json.load(f)

            # Check if cache is expired
            if time.time() - data.get("timestamp", 0) > self.ttl:
                cache_path.unlink()  # Delete expired cache
                return None

            return data.get("value")
        except Exception:
            return None

    def set(self, key: str, value: Any) -> bool:
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache

        Returns:
            True if successful
        """
        cache_file = self._get_cache_key(key)

        try:
            data = {"timestamp": time.time(), "value": value}

            with open(cache_file, "w") as f:
                json.dump(data, f)

            return True
        except Exception:
            return False

    def delete(self, key: str) -> bool:
        """
        Delete value from cache

        Args:
            key: Cache key

        Returns:
            True if successful
        """
        cache_file = self._get_cache_key(key)
        cache_path = Path(cache_file)

        try:
            if cache_path.exists():
                cache_path.unlink()
            return True
        except Exception:
            return False

    def clear(self) -> int:
        """
        Clear all cache files

        Returns:
            Number of files deleted
        """
        count = 0
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
                count += 1
        except Exception:
            pass

        return count

    def clear_expired(self) -> int:
        """
        Clear only expired cache files

        Returns:
            Number of expired files deleted
        """
        count = 0
        try:
            current_time = time.time()
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    with open(cache_file, "r") as f:
                        data = json.load(f)

                    if current_time - data.get("timestamp", 0) > self.ttl:
                        cache_file.unlink()
                        count += 1
                except Exception:
                    continue
        except Exception:
            pass

        return count

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics

        Returns:
            Dictionary with cache stats
        """
        try:
            files = list(self.cache_dir.glob("*.json"))
            total_size = sum(f.stat().st_size for f in files)
            expired = 0

            current_time = time.time()
            for cache_file in files:
                try:
                    with open(cache_file, "r") as f:
                        data = json.load(f)

                    if current_time - data.get("timestamp", 0) > self.ttl:
                        expired += 1
                except Exception:
                    continue

            return {
                "total_files": len(files),
                "total_size_mb": total_size / (1024 * 1024),
                "expired_files": expired,
                "cache_dir": str(self.cache_dir),
                "ttl_hours": self.ttl / 3600,
            }
        except Exception:
            return {
                "total_files": 0,
                "total_size_mb": 0,
                "expired_files": 0,
                "cache_dir": str(self.cache_dir),
                "ttl_hours": self.ttl / 3600,
            }


# Global cache instance
_cache = CacheManager()


def cached(ttl: int = 86400, key_prefix: str = ""):
    """
    Decorator for caching function results

    Args:
        ttl: Time to live in seconds (default 24 hours)
        key_prefix: Prefix for cache keys

    Example:
        @cached(ttl=3600, key_prefix="image_gen")
        def generate_image(prompt):
            # expensive operation
            return result
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key_parts = [key_prefix, func.__name__]

            # Add args to key
            for arg in args:
                key_parts.append(str(arg))

            # Add kwargs to key
            for k, v in sorted(kwargs.items()):
                key_parts.append(f"{k}={v}")

            cache_key = ":".join(key_parts)

            # Try to get from cache
            cached_value = _cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Call function and cache result
            result = func(*args, **kwargs)
            _cache.set(cache_key, result)

            return result

        return wrapper

    return decorator


def get_cache_manager() -> CacheManager:
    """Get global cache manager instance"""
    return _cache
