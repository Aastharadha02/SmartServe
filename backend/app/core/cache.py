import time
import threading
from typing import Any, Optional, Dict, Callable
from functools import wraps
import logging

logger = logging.getLogger("smartserve.cache")


class CacheEntry:
    __slots__ = ("value", "expires_at", "created_at")

    def __init__(self, value: Any, ttl_seconds: int):
        now = time.monotonic()
        self.value = value
        self.created_at = now
        self.expires_at = now + ttl_seconds if ttl_seconds > 0 else float("inf")

    def is_expired(self) -> bool:
        return time.monotonic() > self.expires_at


class SmartServeMemoryCache:
    """
    High-performance, thread-safe in-memory TTL cache with bounded eviction,
    hit/miss telemetry, and zero third-party dependencies.
    """

    def __init__(self, max_entries: int = 2000, default_ttl: int = 180):
        self._store: Dict[str, CacheEntry] = {}
        self._lock = threading.Lock()
        self._max_entries = max_entries
        self._default_ttl = default_ttl
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                self._misses += 1
                return None
            if entry.is_expired():
                del self._store[key]
                self._misses += 1
                return None
            self._hits += 1
            return entry.value

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        effective_ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
        with self._lock:
            # Simple eviction when over limit: remove expired or oldest
            if len(self._store) >= self._max_entries:
                self._cleanup_expired_locked()
                if len(self._store) >= self._max_entries:
                    # Remove first 100 entries (FIFO)
                    keys_to_remove = list(self._store.keys())[:100]
                    for k in keys_to_remove:
                        self._store.pop(k, None)

            self._store[key] = CacheEntry(value, effective_ttl)

    def delete(self, key: str) -> bool:
        with self._lock:
            return bool(self._store.pop(key, None))

    def invalidate_prefix(self, prefix: str) -> int:
        """Invalidate all keys starting with a given prefix."""
        with self._lock:
            to_delete = [k for k in self._store if k.startswith(prefix)]
            for k in to_delete:
                del self._store[k]
            return len(to_delete)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    def _cleanup_expired_locked(self) -> None:
        expired_keys = [k for k, entry in self._store.items() if entry.is_expired()]
        for k in expired_keys:
            del self._store[k]

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            total_requests = self._hits + self._misses
            hit_ratio = round((self._hits / total_requests) * 100, 2) if total_requests > 0 else 0.0
            return {
                "active_keys": len(self._store),
                "hits": self._hits,
                "misses": self._misses,
                "total_requests": total_requests,
                "hit_ratio_percent": hit_ratio,
            }


# Global singleton cache instance
_cache_instance = SmartServeMemoryCache(max_entries=2000, default_ttl=180)


def get_cache() -> SmartServeMemoryCache:
    return _cache_instance


def cached(prefix: str, ttl_seconds: int = 180):
    """
    Decorator for caching function or endpoint results by prefix and arguments.
    """
    def decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Exclude db Session or unhashable objects from key
            safe_args = [str(a) for a in args if not hasattr(a, "execute") and not hasattr(a, "query")]
            safe_kwargs = {k: str(v) for k, v in kwargs.items() if k != "db" and not hasattr(v, "execute")}
            cache_key = f"{prefix}:{fn.__name__}:{safe_args}:{sorted(safe_kwargs.items())}"

            cached_val = _cache_instance.get(cache_key)
            if cached_val is not None:
                return cached_val

            result = fn(*args, **kwargs)
            _cache_instance.set(cache_key, result, ttl_seconds=ttl_seconds)
            return result
        return wrapper
    return decorator
