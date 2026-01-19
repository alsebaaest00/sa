"""Tests for caching system"""

import tempfile
import time
from pathlib import Path


from sa.utils.cache import CacheManager, cached, get_cache_manager


class TestCacheManager:
    """Tests for CacheManager class"""

    def test_cache_initialization(self):
        """Test cache manager initialization"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = CacheManager(cache_dir=tmpdir, ttl=3600)
            assert cache.cache_dir == Path(tmpdir)
            assert cache.ttl == 3600

    def test_set_and_get_value(self):
        """Test setting and getting a value"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = CacheManager(cache_dir=tmpdir)

            # Set value
            assert cache.set("test_key", {"data": "test_value"})

            # Get value
            result = cache.get("test_key")
            assert result == {"data": "test_value"}

    def test_get_nonexistent_key(self):
        """Test getting a nonexistent key returns None"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = CacheManager(cache_dir=tmpdir)
            result = cache.get("nonexistent")
            assert result is None

    def test_cache_expiration(self):
        """Test that cache expires after TTL"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = CacheManager(cache_dir=tmpdir, ttl=1)  # 1 second TTL

            # Set value
            cache.set("test_key", "test_value")

            # Should get value immediately
            assert cache.get("test_key") == "test_value"

            # Wait for expiration
            time.sleep(2)

            # Should return None after expiration
            assert cache.get("test_key") is None

    def test_delete_key(self):
        """Test deleting a key"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = CacheManager(cache_dir=tmpdir)

            # Set and verify
            cache.set("test_key", "test_value")
            assert cache.get("test_key") == "test_value"

            # Delete
            assert cache.delete("test_key")

            # Should be gone
            assert cache.get("test_key") is None

    def test_clear_all_cache(self):
        """Test clearing all cache"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = CacheManager(cache_dir=tmpdir)

            # Set multiple values
            cache.set("key1", "value1")
            cache.set("key2", "value2")
            cache.set("key3", "value3")

            # Clear all
            count = cache.clear()
            assert count == 3

            # All should be gone
            assert cache.get("key1") is None
            assert cache.get("key2") is None
            assert cache.get("key3") is None

    def test_clear_expired_only(self):
        """Test clearing only expired cache entries"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = CacheManager(cache_dir=tmpdir, ttl=2)  # 2 second TTL

            # Set first value
            cache.set("expired_key", "value1")

            # Wait 1 second
            time.sleep(1)

            # Set second value (not expired)
            cache.set("valid_key", "value2")

            # Wait for first to expire
            time.sleep(2)

            # Clear expired
            count = cache.clear_expired()
            assert count == 1

            # Valid key should still exist
            assert cache.get("valid_key") == "value2"

            # Expired key should be gone
            assert cache.get("expired_key") is None

    def test_cache_stats(self):
        """Test getting cache statistics"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = CacheManager(cache_dir=tmpdir, ttl=3600)

            # Add some cache entries
            cache.set("key1", "value1")
            cache.set("key2", "value2")

            # Get stats
            stats = cache.get_stats()

            assert stats["total_files"] == 2
            assert stats["total_size_mb"] >= 0
            assert stats["expired_files"] == 0
            assert stats["ttl_hours"] == 1.0

    def test_cache_with_complex_data(self):
        """Test caching complex data structures"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = CacheManager(cache_dir=tmpdir)

            complex_data = {
                "list": [1, 2, 3, 4, 5],
                "nested": {"a": 1, "b": {"c": 2}},
                "string": "test",
                "number": 42,
                "boolean": True,
            }

            cache.set("complex", complex_data)
            result = cache.get("complex")

            assert result == complex_data

    def test_cache_key_hashing(self):
        """Test that cache keys are hashed consistently"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = CacheManager(cache_dir=tmpdir)

            # Same key should produce same hash
            key1 = cache._get_cache_key("test_key")
            key2 = cache._get_cache_key("test_key")
            assert key1 == key2

            # Different keys should produce different hashes
            key3 = cache._get_cache_key("different_key")
            assert key1 != key3


class TestCachedDecorator:
    """Tests for @cached decorator"""

    def test_cached_decorator_basic(self):
        """Test basic caching with decorator"""
        call_count = 0

        @cached(ttl=3600)
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call should execute function
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count == 1

        # Second call should use cache
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count == 1  # Should not increase

    def test_cached_with_different_args(self):
        """Test that different arguments create different cache entries"""
        call_count = 0

        @cached(ttl=3600)
        def function_with_args(a, b):
            nonlocal call_count
            call_count += 1
            return a + b

        # Different arguments should not hit cache
        result1 = function_with_args(1, 2)
        result2 = function_with_args(3, 4)

        assert result1 == 3
        assert result2 == 7
        assert call_count == 2  # Both should execute

        # Same arguments should hit cache
        result3 = function_with_args(1, 2)
        assert result3 == 3
        assert call_count == 2  # Should not increase

    def test_cached_with_kwargs(self):
        """Test caching with keyword arguments"""
        call_count = 0

        @cached(ttl=3600)
        def function_with_kwargs(name, age=25):
            nonlocal call_count
            call_count += 1
            return f"{name}-{age}"

        result1 = function_with_kwargs("Alice", age=30)
        result2 = function_with_kwargs("Alice", age=30)

        assert result1 == "Alice-30"
        assert result2 == "Alice-30"
        assert call_count == 1  # Second call should use cache

    def test_cached_with_key_prefix(self):
        """Test caching with key prefix"""
        call_count = 0

        @cached(ttl=3600, key_prefix="test_prefix")
        def prefixed_function(x):
            nonlocal call_count
            call_count += 1
            return x * 3

        result = prefixed_function(4)
        assert result == 12
        assert call_count == 1


class TestGetCacheManager:
    """Tests for get_cache_manager function"""

    def test_get_cache_manager_returns_instance(self):
        """Test that get_cache_manager returns a CacheManager instance"""
        cache = get_cache_manager()
        assert isinstance(cache, CacheManager)

    def test_cache_manager_is_singleton(self):
        """Test that cache manager is a singleton"""
        cache1 = get_cache_manager()
        cache2 = get_cache_manager()
        assert cache1 is cache2


class TestCacheEdgeCases:
    """Tests for edge cases in caching"""

    def test_cache_with_none_value(self):
        """Test caching None value"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = CacheManager(cache_dir=tmpdir)

            cache.set("none_key", None)
            result = cache.get("none_key")

            # None is a valid cached value
            assert result is None

    def test_cache_with_empty_string(self):
        """Test caching empty string"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = CacheManager(cache_dir=tmpdir)

            cache.set("empty_key", "")
            result = cache.get("empty_key")

            assert result == ""

    def test_cache_survives_manager_recreation(self):
        """Test that cache persists across manager instances"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create first manager and set value
            cache1 = CacheManager(cache_dir=tmpdir)
            cache1.set("persistent_key", "persistent_value")

            # Create second manager with same directory
            cache2 = CacheManager(cache_dir=tmpdir)
            result = cache2.get("persistent_key")

            assert result == "persistent_value"
