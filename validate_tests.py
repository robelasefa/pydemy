#!/usr/bin/env python3
"""Validate all test files compile correctly."""

import py_compile

test_files = [
    "tests/__init__.py",
    "tests/conftest.py",
    "tests/test_client.py",
    "tests/test_async_client.py",
    "tests/test_models.py",
    "tests/test_error_handling.py",
    "tests/test_context_managers.py",
]

print("Validating test files...")

all_good = True
for test_file in test_files:
    try:
        py_compile.compile(test_file, doraise=True)
        print(f"✓ {test_file}")
    except py_compile.PyCompileError as e:
        print(f"✗ {test_file}: {e}")
        all_good = False
    except FileNotFoundError:
        print(f"✗ {test_file}: File not found")
        all_good = False

if all_good:
    print("\n✅ All test files compile successfully!")
else:
    print("\n❌ Some test files have compilation errors")
