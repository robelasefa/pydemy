#!/usr/bin/env python3
"""Simple test runner to verify test suite functionality."""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import pytest
    print(f"✓ pytest version: {pytest.__version__}")
except ImportError:
    print("✗ pytest not installed")
    sys.exit(1)

try:
    import pytest_asyncio
    print(f"✓ pytest-asyncio version: {pytest_asyncio.__version__}")
except ImportError:
    print("✗ pytest-asyncio not installed")

try:
    from pydemy import UdemyClient, AsyncUdemyClient
    print("✓ Pydemy imports successful")
except ImportError as e:
    print(f"✗ Pydemy import failed: {e}")
    sys.exit(1)

# Test basic functionality
def test_basic_imports():
    """Test that all test modules can be imported."""
    try:
        from tests.conftest import client_credentials
        from tests.test_client import TestUdemyClient
        from tests.test_async_client import TestAsyncUdemyClient
        from tests.test_models import TestCourseFilter
        from tests.test_error_handling import TestErrorHandling
        from tests.test_context_managers import TestContextManagers
        print("✓ All test modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Test module import failed: {e}")
        return False

def test_client_creation():
    """Test basic client creation."""
    try:
        sync_client = UdemyClient("test_id", "test_secret")
        async_client = AsyncUdemyClient("test_id", "test_secret")
        print("✓ Client creation successful")
        return True
    except Exception as e:
        print(f"✗ Client creation failed: {e}")
        return False

if __name__ == "__main__":
    print("Running basic test suite validation...\n")
    
    success = True
    success &= test_basic_imports()
    success &= test_client_creation()
    
    if success:
        print("\n✓ All basic tests passed!")
        print("\nTo run the full test suite:")
        print("  python -m pytest tests/ -v")
        print("  python -m pytest tests/ --cov=pydemy")
        sys.exit(0)
    else:
        print("\n✗ Some basic tests failed!")
        sys.exit(1)
