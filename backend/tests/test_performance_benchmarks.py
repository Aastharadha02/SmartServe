import time
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.cache import get_cache

client = TestClient(app)


def test_catalog_caching_and_latency_benchmark():
    """
    Measurable benchmark comparing cold query latency vs warm cached response latency.
    """
    cache = get_cache()
    cache.clear()

    # 1. Cold Call (DB Query Execution)
    start_cold = time.perf_counter()
    res_cold = client.get("/api/v1/services/categories")
    cold_duration_ms = (time.perf_counter() - start_cold) * 1000

    assert res_cold.status_code == 200
    categories = res_cold.json()
    assert isinstance(categories, list)

    # 2. Warm Call 1 (In-Memory Cache Retrieval)
    start_warm1 = time.perf_counter()
    res_warm1 = client.get("/api/v1/services/categories")
    warm1_duration_ms = (time.perf_counter() - start_warm1) * 1000

    assert res_warm1.status_code == 200
    assert res_warm1.json() == categories

    # 3. Warm Call 2
    start_warm2 = time.perf_counter()
    res_warm2 = client.get("/api/v1/services/categories")
    warm2_duration_ms = (time.perf_counter() - start_warm2) * 1000

    assert res_warm2.status_code == 200

    # 4. Verify telemetry stats
    stats = cache.get_stats()
    assert stats["hits"] >= 2
    assert stats["misses"] >= 1
    assert stats["hit_ratio_percent"] >= 50.0

    print(f"\n[BENCHMARK] Cold DB Latency: {cold_duration_ms:.2f} ms | Warm Cache Latency: {warm1_duration_ms:.2f} ms & {warm2_duration_ms:.2f} ms")


def test_cache_invalidation_lifecycle():
    """Verify prefix invalidation forces cold cache reload."""
    cache = get_cache()
    cache.clear()

    # Seed cache
    res1 = client.get("/api/v1/services/categories")
    assert res1.status_code == 200
    assert cache.get("catalog:categories") is not None

    # Invalidate catalog
    deleted_count = cache.invalidate_prefix("catalog:")
    assert deleted_count >= 1
    assert cache.get("catalog:categories") is None

    # Next call repopulates cache
    res2 = client.get("/api/v1/services/categories")
    assert res2.status_code == 200
    assert cache.get("catalog:categories") is not None


def test_services_list_caching_and_telemetry_endpoint():
    """Verify services list endpoint caching and metrics endpoint."""
    res_list1 = client.get("/api/v1/services/?limit=10")
    assert res_list1.status_code == 200

    res_list2 = client.get("/api/v1/services/?limit=10")
    assert res_list2.status_code == 200

    res_metrics = client.get("/api/v1/services/metrics/cache")
    assert res_metrics.status_code == 200
    data = res_metrics.json()
    assert "hits" in data
    assert "misses" in data
    assert "hit_ratio_percent" in data
