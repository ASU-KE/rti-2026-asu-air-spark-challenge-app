---
name: python-patterns
description: Pythonic idioms, type hints, error handling, and PEP 8 for writing or reviewing Python. Use when writing or reviewing Python and idiomatic structure, typing, error handling, or performance is in question.
metadata:
  origin: ECC
---

# Python Development Patterns

Idiomatic Python patterns for building robust, efficient, and maintainable applications.

## Core Principles

### Readability Counts

Write code that is obvious to the next reader.

```python
# Good: Clear and readable
def get_active_users(users: list[User]) -> list[User]:
    """Return only active users from the provided list."""
    return [user for user in users if user.is_active]


# Bad: Clever but confusing
def get_active_users(u):
    return [x for x in u if x.a]
```

### Explicit is Better Than Implicit

Be clear about what your code does; avoid hidden side effects.

```python
# Good: Explicit configuration
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Bad: Hidden side effects
import some_module
some_module.setup()  # What does this do?
```

### EAFP — Easier to Ask Forgiveness Than Permission

Prefer exception handling over pre-checking conditions (LBYL, Look Before You Leap).

```python
# Good: EAFP style
def get_value(dictionary: dict, key: str, default_value: Any = None) -> Any:
    try:
        return dictionary[key]
    except KeyError:
        return default_value

# Bad: LBYL style
def get_value(dictionary: dict, key: str, default_value: Any = None) -> Any:
    if key in dictionary:
        return dictionary[key]
    else:
        return default_value
```

## Type Hints

Annotate function signatures. On Python 3.9+ prefer built-in generics (`list[str]`, `dict[str, int]`); use the `typing` module equivalents on 3.8 and earlier.

```python
from typing import Any, Optional

def process_user(
    user_id: str,
    data: dict[str, Any],
    active: bool = True
) -> Optional[User]:
    """Process a user and return the updated User or None."""
    if not active:
        return None
    return User(user_id, data)

# Python 3.8 and earlier
from typing import Dict, Optional

def process_user_legacy(user_id: str, data: Dict[str, Any]) -> Optional[User]:
    ...
```

### Type Aliases and TypeVar

```python
from typing import TypeVar, Union

# Type alias for complex types
JSON = Union[dict[str, Any], list[Any], str, int, float, bool, None]

def parse_json(data: str) -> JSON:
    return json.loads(data)

# Generic types
T = TypeVar('T')

def first(items: list[T]) -> T | None:
    """Return the first item or None if list is empty."""
    return items[0] if items else None
```

### Protocol-Based Duck Typing

```python
from typing import Protocol

class Renderable(Protocol):
    def render(self) -> str:
        """Render the object to a string."""

def render_all(items: list[Renderable]) -> str:
    """Render all items that implement the Renderable protocol."""
    return "\n".join(item.render() for item in items)
```

## Error Handling

Catch specific exceptions, chain with `from` to preserve the traceback, and model application failures with a custom hierarchy.

```python
# Catch specific exceptions; never a bare except that swallows failures
def load_config(path: str) -> Config:
    try:
        with open(path) as f:
            return Config.from_json(f.read())
    except FileNotFoundError as e:
        raise ConfigError(f"Config file not found: {path}") from e
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in config: {path}") from e
```

### Exception Chaining

```python
def process_data(data: str) -> Result:
    try:
        parsed = json.loads(data)
    except json.JSONDecodeError as e:
        # Chain exceptions to preserve the traceback
        raise ValueError(f"Failed to parse data: {data}") from e
```

### Custom Exception Hierarchy

```python
class AppError(Exception):
    """Base exception for all application errors."""
    pass

class ValidationError(AppError):
    """Raised when input validation fails."""
    pass

class NotFoundError(AppError):
    """Raised when a requested resource is not found."""
    pass

# Usage
def get_user(user_id: str) -> User:
    user = db.find_user(user_id)
    if not user:
        raise NotFoundError(f"User not found: {user_id}")
    return user
```

## Context Managers

Use `with` for resource management so setup and teardown always pair, even on exceptions.

```python
def process_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()
```

### Custom Context Managers

```python
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    """Context manager to time a block of code."""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{name} took {elapsed:.4f} seconds")

# Usage
with timer("data processing"):
    process_large_dataset()
```

### Context Manager Classes

```python
class DatabaseTransaction:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        self.connection.begin_transaction()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        return False  # Don't suppress exceptions

# Usage
with DatabaseTransaction(conn):
    user = conn.create_user(user_data)
    conn.create_profile(user.id, profile_data)
```

## Comprehensions and Generators

Use a comprehension for a simple transformation; expand into a named function once it grows more than one condition.

```python
# Comprehension for simple transformations
names = [user.name for user in users if user.is_active]

# Once it grows complex, use a generator function instead of
# [x * 2 for x in items if x > 0 if x % 2 == 0]
def filter_and_transform(items: Iterable[int]) -> list[int]:
    result = []
    for x in items:
        if x > 0 and x % 2 == 0:
            result.append(x * 2)
    return result
```

### Generator Expressions

Use a generator expression for lazy evaluation; it avoids the large intermediate list a comprehension would build.

```python
# Lazy: no intermediate list
total = sum(x * x for x in range(1_000_000))
```

### Generator Functions

```python
def read_large_file(path: str) -> Iterator[str]:
    """Read a large file line by line."""
    with open(path) as f:
        for line in f:
            yield line.strip()

# Usage
for line in read_large_file("huge.txt"):
    process(line)
```

## Data Classes and Named Tuples

Use `@dataclass` for mutable data containers with auto-generated `__init__`, `__repr__`, and `__eq__`; use `NamedTuple` for immutable records.

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    """User entity with automatic __init__, __repr__, and __eq__."""
    id: str
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

user = User(id="123", name="Alice", email="alice@example.com")
```

### Data Classes with Validation

Validate in `__post_init__`.

```python
@dataclass
class User:
    email: str
    age: int

    def __post_init__(self):
        if "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email}")
        if self.age < 0 or self.age > 150:
            raise ValueError(f"Invalid age: {self.age}")
```

### Named Tuples

```python
from typing import NamedTuple

class Point(NamedTuple):
    """Immutable 2D point."""
    x: float
    y: float

    def distance(self, other: 'Point') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

# Usage
p1 = Point(0, 0)
p2 = Point(3, 4)
print(p1.distance(p2))  # 5.0
```

## Deep-Dive References

Reach for these when the task enters their branch:

- [Decorators](decorators.md) — function, parameterized, and class-based decorators.
- [Concurrency Patterns](concurrency.md) — threading (I/O-bound), multiprocessing (CPU-bound), and `async`/`await`.
- [Memory and Performance](performance.md) — `__slots__`, generators for large data, and string building.
- [Package Organization and Tooling](packaging-and-tooling.md) — project layout, imports, `pyproject.toml`, and the format/lint/type/test/security commands.

## Quick Reference: Python Idioms

| Idiom | Description |
|-------|-------------|
| EAFP | Easier to Ask Forgiveness than Permission |
| Context managers | Use `with` for resource management |
| List comprehensions | For simple transformations |
| Generators | For lazy evaluation and large datasets |
| Type hints | Annotate function signatures |
| Dataclasses | For data containers with auto-generated methods |
| `__slots__` | For memory optimization |
| f-strings | For string formatting (Python 3.6+) |
| `pathlib.Path` | For path operations (Python 3.4+) |
| `enumerate` | For index-element pairs in loops |

## Anti-Patterns to Avoid

Each pair shows the trap and its idiomatic replacement.

```python
# Bad: Mutable default arguments
def append_to(item, items=[]):
    items.append(item)
    return items

# Good: Use None and create new list
def append_to(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Bad: Checking type with type()
if type(obj) == list:
    process(obj)

# Good: Use isinstance
if isinstance(obj, list):
    process(obj)

# Bad: Comparing to None with ==
if value == None:
    process()

# Good: Use is
if value is None:
    process()

# Bad: from module import *
from os.path import *

# Good: Explicit imports
from os.path import join, exists

# Bad: Bare except
try:
    risky_operation()
except:
    pass

# Good: Specific exception
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
```

When in doubt, prioritize clarity over cleverness and follow the principle of least surprise.
