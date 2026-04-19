# Test Suite Documentation

This directory contains a comprehensive test suite for the Pydemy library using pytest.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                  # Pytest configuration and fixtures
├── test_client.py               # Synchronous client tests
├── test_async_client.py          # Asynchronous client tests
├── test_models.py               # Pydantic model tests
├── test_error_handling.py        # Error handling scenarios
├── test_context_managers.py     # Context manager functionality tests
└── README.md                   # This file
```

## Test Coverage

### 1. Client Tests (`test_client.py`, `test_async_client.py`)
- **Client initialization**: Test credential validation and setup
- **API methods**: Test all client methods with various scenarios
- **Error handling**: Test HTTP errors, request errors, JSON parsing errors
- **Filtering**: Test course and review filter functionality
- **Pagination**: Test pagination parameters
- **Response parsing**: Test parsing of different response types

### 2. Model Tests (`test_models.py`)
- **Filter models**: `CourseFilter`, `ReviewFilter`
- **Data models**: `Course`, `CourseReview`, `Instructor`, `User`
- **Content models**: `Chapter`, `Lecture`, `Quiz`, `Asset`
- **Validation**: Test Pydantic model validation and error cases

### 3. Error Handling Tests (`test_error_handling.py`)
- **HTTP errors**: 404, 401, 500 status codes
- **Request errors**: Connection timeouts, DNS failures
- **JSON parsing errors**: Invalid JSON responses
- **Response format errors**: Unexpected API response structures
- **Error chaining**: Proper exception chaining preservation

### 4. Context Manager Tests (`test_context_managers.py`)
- **Resource management**: Proper cleanup of HTTP clients
- **Exception handling**: Cleanup even when exceptions occur
- **Nested contexts**: Multiple context managers
- **Attribute preservation**: Client attributes maintained across contexts

## Running Tests

### Prerequisites
Install test dependencies:
```bash
pip install -r requirements-dev.txt
```

### Basic Test Run
```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=pydemy

# Run specific test file
python -m pytest tests/test_client.py -v

# Run specific test method
python -m pytest tests/test_client.py::TestUdemyClient::test_client_initialization -v
```

### Test Configuration
The `pytest.ini` file configures:
- Test discovery patterns
- Coverage reporting
- Markers for async/slow/integration tests
- Strict mode for better test quality

## Test Fixtures

### `conftest.py` provides:
- **Client credentials**: Test API credentials
- **Mock responses**: Sample API response data
- **HTTP clients**: Mocked HTTP clients for testing
- **Filter data**: Sample filter configurations

## Test Categories

### Markers
- `@pytest.mark.asyncio`: Marks async tests
- `@pytest.mark.slow`: Marks slow-running tests
- `@pytest.mark.integration`: Marks integration tests

### Test Types
1. **Unit tests**: Individual component testing
2. **Integration tests**: Component interaction testing
3. **Error scenario tests**: Exception handling validation
4. **Context manager tests**: Resource management validation

## Mock Strategy

The test suite uses comprehensive mocking to:
- Avoid actual HTTP requests to external APIs
- Test error scenarios without network dependencies
- Ensure consistent and repeatable test results
- Test edge cases and error conditions

## Coverage Goals

Target coverage: **80%** minimum
- Critical paths: 100% coverage
- Error handling: 100% coverage
- Model validation: 100% coverage
- Context managers: 100% coverage

## Continuous Integration

The test suite is designed to run in CI/CD pipelines:
- Fast execution with mocking
- No external dependencies
- Clear error reporting
- Coverage reporting integration

## Best Practices Followed

1. **Descriptive test names**: Clear indication of what's being tested
2. **AAA pattern**: Arrange, Act, Assert structure
3. **Independent tests**: No test dependencies
4. **Comprehensive coverage**: Happy path and error cases
5. **Clear assertions**: Specific and meaningful assertions
6. **Proper fixtures**: Reusable test setup
7. **Error testing**: Comprehensive exception handling validation

## Troubleshooting

### Common Issues
1. **Import errors**: Ensure test dependencies are installed
2. **Async test failures**: Ensure pytest-asyncio is installed
3. **Coverage issues**: Check pytest-cov installation
4. **Mock conflicts**: Verify mock patching is correct

### Debug Mode
Run tests with additional debugging:
```bash
python -m pytest tests/ -v -s --tb=long
```

## Future Enhancements

1. **Performance tests**: Add performance benchmarking
2. **Load tests**: Test concurrent request handling
3. **Integration tests**: Test with real (sandbox) API
4. **Property-based tests**: Use hypothesis for edge case testing
5. **Contract tests**: API contract validation
