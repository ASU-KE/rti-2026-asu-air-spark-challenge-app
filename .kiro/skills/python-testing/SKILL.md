---
name: python-testing
description: pytest patterns — TDD, fixtures, parametrization, mocking, async, and coverage. Use when writing or reviewing pytest tests, or setting up test infrastructure.
metadata:
  origin: ECC
---

# Python Testing Patterns

pytest strategies for Python applications: TDD, fixtures, parametrization, and coverage in this file; deep-dive branches disclosed to siblings.

- [mocking.md](mocking.md) — `unittest.mock`: patching, autospec, mock properties
- [async-testing.md](async-testing.md) — `pytest-asyncio`, async fixtures, async mocks
- [recipes.md](recipes.md) — API endpoints, database sessions, class methods, file/side-effect tests
- [configuration.md](configuration.md) — full `pytest.ini` and `pyproject.toml` templates

## Test-Driven Development (TDD)

Drive every change through the cycle:

1. **RED**: write a failing test for the desired behavior.
2. **GREEN**: write minimal code to make it pass.
3. **REFACTOR**: improve the code while tests stay green.

```python
# Step 1: Write failing test (RED)
def test_add_numbers():
    result = add(2, 3)
    assert result == 5

# Step 2: Write minimal implementation (GREEN)
def add(a, b):
    return a + b

# Step 3: Refactor if needed (REFACTOR)
```

## Coverage

Target 80%+ overall and 100% on critical paths. Measure with `pytest --cov`:

```bash
pytest --cov=mypackage --cov-report=term-missing --cov-report=html
```

## pytest Fundamentals

### Test Structure

```python
import pytest

def test_addition():
    """Test basic addition."""
    assert 2 + 2 == 4

def test_string_uppercase():
    """Test string uppercasing."""
    text = "hello"
    assert text.upper() == "HELLO"

def test_list_append():
    """Test list append."""
    items = [1, 2, 3]
    items.append(4)
    assert 4 in items
    assert len(items) == 4
```

### Assertions

```python
# Equality / inequality
assert result == expected
assert result != unexpected

# Truthiness / identity
assert result           # Truthy
assert not result       # Falsy
assert result is True    # Exactly True
assert result is None    # Exactly None

# Membership
assert item in collection
assert item not in collection

# Comparisons
assert result > 0
assert 0 <= result <= 100

# Type checking
assert isinstance(result, str)
```

## Fixtures

### Basic Usage

```python
import pytest

@pytest.fixture
def sample_data():
    """Fixture providing sample data."""
    return {"name": "Alice", "age": 30}

def test_sample_data(sample_data):
    """Test using the fixture."""
    assert sample_data["name"] == "Alice"
    assert sample_data["age"] == 30
```

### Setup and Teardown

`yield` splits setup from teardown — code before it runs first, code after runs once the test finishes.

```python
@pytest.fixture
def database():
    """Fixture with setup and teardown."""
    db = Database(":memory:")           # Setup
    db.create_tables()
    db.insert_test_data()

    yield db                             # Provide to test

    db.close()                           # Teardown

def test_database_query(database):
    result = database.query("SELECT * FROM users")
    assert len(result) > 0
```

### Scopes

Scope controls how often a fixture rebuilds: `function` (default, per test), `module` (once per file), `session` (once per run). Widen scope for expensive resources.

```python
@pytest.fixture                          # function scope: per test
def temp_file():
    with open("temp.txt", "w") as f:
        yield f
    os.remove("temp.txt")

@pytest.fixture(scope="module")          # once per module
def module_db():
    db = Database(":memory:")
    db.create_tables()
    yield db
    db.close()

@pytest.fixture(scope="session")         # once per session
def shared_resource():
    resource = ExpensiveResource()
    yield resource
    resource.cleanup()
```

### Parameterized Fixtures

A fixture with `params` reruns every dependent test once per value.

```python
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def db(request):
    """Test against multiple database backends."""
    if request.param == "sqlite":
        return Database(":memory:")
    elif request.param == "postgresql":
        return Database("postgresql://localhost/test")
    elif request.param == "mysql":
        return Database("mysql://localhost/test")

def test_database_operations(db):
    """Runs once per backend."""
    result = db.query("SELECT 1")
    assert result is not None
```

### Multiple Fixtures

```python
@pytest.fixture
def user():
    return User(id=1, name="Alice")

@pytest.fixture
def admin():
    return User(id=2, name="Admin", role="admin")

def test_user_admin_interaction(user, admin):
    assert admin.can_manage(user)
```

### Autouse Fixtures

An `autouse=True` fixture runs for every test in scope without being named.

```python
@pytest.fixture(autouse=True)
def reset_config():
    Config.reset()
    yield
    Config.cleanup()

def test_without_fixture_call():
    # reset_config ran automatically
    assert Config.get_setting("debug") is False
```

### Shared Fixtures in conftest.py

Fixtures in `tests/conftest.py` are available to every test without import.

```python
# tests/conftest.py
import pytest

@pytest.fixture
def client():
    """Shared fixture for all tests."""
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers(client):
    """Generate auth headers for API testing."""
    response = client.post("/api/login", json={
        "username": "test",
        "password": "test"
    })
    token = response.json["token"]
    return {"Authorization": f"Bearer {token}"}
```

## Parametrization

`@pytest.mark.parametrize` runs one test across many inputs. Add `ids` for readable case names.

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("PyThOn", "PYTHON"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add(a, b, expected):
    assert add(a, b) == expected

@pytest.mark.parametrize("input,expected", [
    ("valid@email.com", True),
    ("invalid", False),
    ("@no-domain.com", False),
], ids=["valid-email", "missing-at", "missing-domain"])
def test_email_validation(input, expected):
    assert is_valid_email(input) is expected
```

## Markers and Test Selection

Mark tests to group and filter them, then select with `-m`. Declare every marker in [configuration.md](configuration.md) so `--strict-markers` rejects typos.

```python
@pytest.mark.slow
def test_slow_operation():
    time.sleep(5)

@pytest.mark.integration
def test_api_integration():
    response = requests.get("https://api.example.com")
    assert response.status_code == 200

@pytest.mark.unit
def test_unit_logic():
    assert calculate(2, 3) == 5
```

```bash
pytest -m "not slow"            # skip slow tests
pytest -m integration           # only integration
pytest -m "integration or slow" # either marker
pytest -m "unit and not slow"   # unit, excluding slow
```

## Exceptions

Assert that code raises with `pytest.raises`. Add `match` for the message, or capture `exc_info` for attributes.

```python
def test_divide_by_zero():
    """Raises on divide by zero."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_custom_exception():
    """Match the exception message (regex)."""
    with pytest.raises(ValueError, match="invalid input"):
        validate_input("invalid")

def test_exception_with_details():
    """Inspect exception attributes via exc_info."""
    with pytest.raises(CustomError) as exc_info:
        raise CustomError("error", code=400)

    assert exc_info.value.code == 400
    assert "error" in str(exc_info.value)
```

## Test Organization

### Directory Structure

Separate tests by type so markers and CI can target each tier.

```
tests/
├── conftest.py                 # Shared fixtures
├── __init__.py
├── unit/                       # Unit tests
│   ├── test_models.py
│   ├── test_utils.py
│   └── test_services.py
├── integration/                # Integration tests
│   ├── test_api.py
│   └── test_database.py
└── e2e/                        # End-to-end tests
    └── test_user_flow.py
```

### Test Classes

Group related tests in a `Test*` class; an `autouse` setup fixture runs before each method.

```python
class TestUserService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.service = UserService()

    def test_create_user(self):
        user = self.service.create_user("Alice")
        assert user.name == "Alice"

    def test_delete_user(self):
        user = User(id=1, name="Bob")
        self.service.delete_user(user)
        assert not self.service.user_exists(1)
```

## Best Practices

Every test should satisfy all of these before you consider it done:

- **Test behavior, not internals** — assert on outputs and effects, so refactors don't break tests.
- **One behavior per test** — a single clear reason to fail.
- **Descriptive names** — `test_user_login_with_invalid_credentials_fails`.
- **Fixtures over duplication** — share setup through fixtures.
- **Mock external dependencies** — keep tests off real networks and services (see [mocking.md](mocking.md)).
- **Cover edge cases** — empty inputs, `None`, boundary conditions.
- **Keep tests independent** — no shared state; any order passes.
- **Keep tests fast** — mark slow ones and exclude them from the default run.
- **Assert exceptions with `pytest.raises`** — never wrap the call in `try`/`except`.
- **Trust third-party code** — test your code, not the libraries.
- **80%+ coverage on critical paths** — measured, not assumed.

## Running Tests

```bash
pytest                          # all tests
pytest tests/test_utils.py      # one file
pytest tests/test_utils.py::test_function  # one test
pytest -v                       # verbose output
pytest --cov=mypackage --cov-report=html   # with coverage
pytest -m "not slow"            # skip slow tests
pytest -x                       # stop on first failure
pytest --maxfail=3              # stop after 3 failures
pytest --lf                     # rerun last failed
pytest -k "test_user"           # match by name pattern
pytest --pdb                    # drop into debugger on failure
```

## Quick Reference

| Pattern | Usage |
|---------|-------|
| `pytest.raises()` | Test expected exceptions |
| `@pytest.fixture()` | Create reusable test fixtures |
| `@pytest.mark.parametrize()` | Run tests with multiple inputs |
| `@pytest.mark.slow` | Mark slow tests |
| `pytest -m "not slow"` | Skip slow tests |
| `@patch()` | Mock functions and classes ([mocking.md](mocking.md)) |
| `tmp_path` fixture | Automatic temp directory ([recipes.md](recipes.md)) |
| `pytest --cov` | Generate coverage report |
| `assert` | Simple and readable assertions |

Tests are code: keep them clean, readable, and maintainable.
