# Memory and Performance

Reach for these when memory footprint or throughput is the concern.

## `__slots__` for Memory Efficiency

Declare `__slots__` to drop the per-instance `__dict__` on classes with a fixed set of attributes and many instances.

```python
# Regular class uses __dict__ (more memory)
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# __slots__ reduces memory usage
class Point:
    __slots__ = ['x', 'y']

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
```

## Generators for Large Data

Yield items one at a time instead of materialising a full list in memory.

```python
# Returns full list in memory
def read_lines(path: str) -> list[str]:
    with open(path) as f:
        return [line.strip() for line in f]

# Yields lines one at a time
def read_lines(path: str) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()
```

## Building Strings with `join`

Accumulate with `"".join(...)` (O(n)); repeated `+=` in a loop is O(n²) because strings are immutable.

```python
# O(n²) due to string immutability
result = ""
for item in items:
    result += str(item)

# O(n) using join
result = "".join(str(item) for item in items)

# Using StringIO for building
from io import StringIO

buffer = StringIO()
for item in items:
    buffer.write(str(item))
result = buffer.getvalue()
```
