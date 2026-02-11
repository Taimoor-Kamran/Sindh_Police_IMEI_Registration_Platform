# Pytest Patterns Reference

## Fixtures

### Basic Fixture
```python
@pytest.fixture
def client():
    return TestClient(app)
```

### Fixture with Teardown
```python
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()
```

### Scoped Fixtures
```python
@pytest.fixture(scope="session")  # once per test session
@pytest.fixture(scope="module")   # once per module
@pytest.fixture(scope="class")    # once per class
@pytest.fixture(scope="function") # default, once per test
```

### Parametrized Fixture
```python
@pytest.fixture(params=["mysql", "postgres", "sqlite"])
def database(request):
    return create_db(request.param)
```

## Parametrize

### Basic
```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected
```

### Multiple Parameters
```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):  # runs 4 combinations
    assert x * y > 0
```

### IDs for Clarity
```python
@pytest.mark.parametrize("input,expected", [
    pytest.param(1, 1, id="identity"),
    pytest.param(2, 4, id="square"),
])
def test_power(input, expected):
    assert input ** 2 == expected
```

## Markers

### Custom Markers (pyproject.toml)
```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "integration: integration tests",
    "unit: unit tests",
]
```

### Using Markers
```python
@pytest.mark.slow
def test_slow_operation():
    pass

@pytest.mark.skip(reason="Not implemented")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_feature():
    pass

@pytest.mark.xfail(reason="Known bug")
def test_known_issue():
    pass
```

## Mocking

### patch decorator
```python
from unittest.mock import patch

@patch("mymodule.external_api")
def test_with_mock(mock_api):
    mock_api.return_value = {"status": "ok"}
    result = my_function()
    assert result["status"] == "ok"
```

### patch context manager
```python
def test_with_context():
    with patch("mymodule.get_data") as mock:
        mock.return_value = [1, 2, 3]
        assert len(get_data()) == 3
```

### pytest-mock (mocker fixture)
```python
def test_with_mocker(mocker):
    mock = mocker.patch("mymodule.api_call")
    mock.return_value = "mocked"
    assert api_call() == "mocked"
```

## Async Tests

### pytest-asyncio
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result == "expected"
```

### Async Fixture
```python
@pytest.fixture
async def async_client():
    async with AsyncClient(app) as client:
        yield client

@pytest.mark.asyncio
async def test_endpoint(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
```

## Exception Testing

```python
def test_raises():
    with pytest.raises(ValueError) as exc_info:
        raise ValueError("invalid value")
    assert "invalid" in str(exc_info.value)

def test_raises_match():
    with pytest.raises(ValueError, match=r"invalid.*"):
        raise ValueError("invalid input")
```

## Temporary Files

```python
def test_with_tmp(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")
    assert file.read_text() == "hello"

def test_with_tmpdir(tmpdir):  # older API
    file = tmpdir.join("test.txt")
    file.write("hello")
```

## Capsys (Capture Output)

```python
def test_output(capsys):
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"
```

## Monkeypatch

```python
def test_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    assert os.environ["API_KEY"] == "test-key"

def test_attribute(monkeypatch):
    monkeypatch.setattr("mymodule.CONFIG", {"debug": True})
```
