---
name: redis-patterns
description: Redis patterns for production — caching, distributed locks, rate limiting, pub/sub and Streams, sessions, key/TTL design, connection and eviction config. Use when adding caching, a lock, rate limiting, sessions, or messaging with Redis, reviewing key or TTL design, or tuning Redis for production.
metadata:
  origin: ECC
---

# Redis Patterns

Production Redis best practices across common backend use cases. Single commands are atomic; multi-step workflows need a Lua script, `MULTI`/`EXEC`, or a pipeline with `transaction=True` to stay atomic — this drives the Lua and pipeline choices throughout.

## Data Structure Cheat Sheet

| Use Case | Structure | Example Key |
|----------|-----------|-------------|
| Simple cache | String | `product:123` |
| User session | Hash | `session:abc` |
| Leaderboard | Sorted Set | `scores:weekly` |
| Unique visitors | Set | `visitors:2024-01-01` |
| Activity feed | List | `feed:user:456` |
| Event stream | Stream | `events:orders` |
| Counters / rate limits | String (INCR) | `ratelimit:user:123` |
| Bloom filter / HLL | HyperLogLog | `hll:pageviews` |

## Core Patterns

### Cache-Aside (Lazy Loading)

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_product(product_id: int):
    cache_key = f"product:{product_id}"
    cached = r.get(cache_key)

    if cached:
        return json.loads(cached)

    product = db.query("SELECT * FROM products WHERE id = %s", product_id)
    r.setex(cache_key, 3600, json.dumps(product))  # TTL: 1 hour
    return product
```

### Write-Through Cache

```python
def update_product(product_id: int, data: dict):
    # Write to DB first
    db.execute("UPDATE products SET ... WHERE id = %s", product_id)

    # Immediately update cache
    cache_key = f"product:{product_id}"
    r.setex(cache_key, 3600, json.dumps(data))
```

### Cache Invalidation

```python
# Tag-based invalidation — group related keys under a set
def cache_product(product_id: int, category_id: int, data: dict):
    key = f"product:{product_id}"
    tag = f"tag:category:{category_id}"
    pipe = r.pipeline(transaction=True)
    pipe.setex(key, 3600, json.dumps(data))
    pipe.sadd(tag, key)
    pipe.expire(tag, 3600)
    pipe.execute()

def invalidate_category(category_id: int):
    tag = f"tag:category:{category_id}"
    keys = r.smembers(tag)
    if keys:
        r.delete(*keys)
    r.delete(tag)
```

### Session Storage

```python
import time
import uuid

def create_session(user_id: int, ttl: int = 86400) -> str:
    session_id = str(uuid.uuid4())
    key = f"session:{session_id}"
    pipe = r.pipeline(transaction=True)
    pipe.hset(key, mapping={
        "user_id": user_id,
        "created_at": int(time.time()),
    })
    pipe.expire(key, ttl)
    pipe.execute()
    return session_id

def get_session(session_id: str) -> dict | None:
    data = r.hgetall(f"session:{session_id}")
    return data if data else None

def delete_session(session_id: str):
    r.delete(f"session:{session_id}")
```

## Rate Limiting

Use fixed-window for low-traffic endpoints; use sliding-window Lua for accurate per-user throttling.

### Fixed Window (Simple)

```python
def is_rate_limited(user_id: int, limit: int = 100, window: int = 60) -> bool:
    key = f"ratelimit:{user_id}:{int(time.time()) // window}"
    pipe = r.pipeline(transaction=True)
    pipe.incr(key)
    pipe.expire(key, window)
    count, _ = pipe.execute()
    return count > limit
```

### Sliding Window (Lua — Atomic)

```lua
-- sliding_window.lua
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])

redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
local count = redis.call('ZCARD', key)

if count < limit then
    -- Use unique member (now + sequence) to avoid collisions within the same millisecond
    local seq_key = key .. ':seq'
    local seq = redis.call('INCR', seq_key)
    redis.call('EXPIRE', seq_key, math.ceil(window / 1000))
    redis.call('ZADD', key, now, now .. '-' .. seq)
    redis.call('EXPIRE', key, math.ceil(window / 1000))
    return 1
end
return 0
```

```python
sliding_window = r.register_script(open('sliding_window.lua').read())

def allow_request(user_id: int) -> bool:
    key = f"ratelimit:sliding:{user_id}"
    now = int(time.time() * 1000)
    return bool(sliding_window(keys=[key], args=[now, 60000, 100]))
```

## Distributed Locks

Single-node lock via `SET NX PX`. For multi-node setups use the `redlock-py` library, which implements the full Redlock algorithm.

```python
import uuid

def acquire_lock(resource: str, ttl_ms: int = 5000) -> str | None:
    lock_key = f"lock:{resource}"
    token = str(uuid.uuid4())
    acquired = r.set(lock_key, token, px=ttl_ms, nx=True)
    return token if acquired else None

def release_lock(resource: str, token: str) -> bool:
    release_script = """
    if redis.call('get', KEYS[1]) == ARGV[1] then
        return redis.call('del', KEYS[1])
    else
        return 0
    end
    """
    result = r.eval(release_script, 1, f"lock:{resource}", token)
    return bool(result)

# Usage
token = acquire_lock("order:payment:123")
if token:
    try:
        process_payment()
    finally:
        release_lock("order:payment:123", token)
```

## Pub/Sub & Streams

Prefer **Streams** over Pub/Sub when you need delivery guarantees, consumer groups, or replay; use Pub/Sub for fire-and-forget broadcast.

### Pub/Sub (Fire-and-Forget)

```python
# Publisher
def publish_event(channel: str, payload: dict):
    r.publish(channel, json.dumps(payload))

# Subscriber (blocking — run in separate thread/process)
def subscribe_events(channel: str):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        if message['type'] == 'message':
            handle(json.loads(message['data']))
```

### Redis Streams (Durable Queue)

```python
# Producer
def emit(stream: str, event: dict):
    r.xadd(stream, event, maxlen=10000)  # Cap stream length

# Consumer group — guarantees at-least-once delivery
try:
    r.xgroup_create('events:orders', 'processor', id='0', mkstream=True)
except Exception:
    pass  # Group already exists

def consume(stream: str, group: str, consumer: str):
    while True:
        messages = r.xreadgroup(group, consumer, {stream: '>'}, count=10, block=2000)
        for _, entries in (messages or []):
            for msg_id, data in entries:
                process(data)
                r.xack(stream, group, msg_id)
```

## Key Design

### Naming Conventions

```
# Pattern: resource:id:field
user:123:profile
order:456:status
cache:product:789

# Pattern: namespace:resource:id
myapp:session:abc123
myapp:ratelimit:user:123

# Pattern: resource:date (time-bound keys)
stats:pageviews:2024-01-01
```

### TTL Strategy

Always set a TTL. Keys without one accumulate indefinitely and cause memory pressure.

| Data Type | Suggested TTL |
|-----------|--------------|
| User session | 24h (`86400`) |
| API response cache | 5–15 min |
| Rate limit window | Match window size |
| Short-lived tokens | 5–10 min |
| Leaderboard | 1h–24h |
| Static/reference data | 1h–1 week |

## Anti-Patterns

When reviewing key design or a Redis integration, check every key and call site against every row below before sign-off.

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Keys with no TTL | Memory grows unbounded | Always set TTL |
| `KEYS *` in production | Blocks the server (O(N)) | Use `SCAN` cursor |
| Storing large blobs (>100KB) | Slow serialization, memory pressure | Store reference + fetch from object store |
| Single Redis for everything | No isolation between cache & queue | Use separate DBs or instances |
| Ignoring connection pool limits | Connection exhaustion under load | Size pool to workload |
| Not handling cache miss stampede | Thundering herd on cold start | Use locks or probabilistic early expiry |
| `FLUSHALL` without thought | Wipes entire instance | Scope deletes by key pattern |

### Cache Miss Stampede Prevention

```python
import threading

_locks: dict[str, threading.Lock] = {}
_locks_mutex = threading.Lock()

def get_with_lock(key: str, fetch_fn, ttl: int = 300):
    cached = r.get(key)
    if cached:
        return json.loads(cached)

    with _locks_mutex:
        if key not in _locks:
            _locks[key] = threading.Lock()
        lock = _locks[key]
    with lock:
        cached = r.get(key)  # Re-check after acquiring lock
        if cached:
            return json.loads(cached)
        value = fetch_fn()
        r.setex(key, ttl, json.dumps(value))
        return value
```

For multi-process deployments, replace the in-process lock with `acquire_lock`/`release_lock` from [Distributed Locks](#distributed-locks).

## Quick Reference

| Pattern | When to Use |
|---------|-------------|
| Cache-aside | Read-heavy, tolerate slight staleness |
| Write-through | Strong consistency required |
| Distributed lock | Prevent concurrent access to a resource |
| Sliding window rate limit | Accurate per-user throttling |
| Redis Streams | Durable event queue with consumer groups |
| Pub/Sub | Broadcast with no delivery guarantees needed |
| Sorted Set leaderboard | Ranked scoring, pagination |
| HyperLogLog | Approximate unique count at low memory |

## Production Configuration

Connection pooling, cluster mode, Sentinel HA, and eviction policies: [`production-config.md`](production-config.md).

## Related

- Skill: `postgres-patterns` — relational data patterns
- Skill: `backend-patterns` — API and service layer patterns
- Skill: `database-migrations` — schema versioning
- Skill: `django-patterns` — Django cache framework integration
- Agent: `database-reviewer` — full database review workflow
