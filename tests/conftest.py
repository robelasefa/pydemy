"""Pytest configuration and fixtures for Pydemy tests."""

from unittest.mock import Mock, patch

import pytest

from pydemy import AsyncUdemyClient, UdemyClient


@pytest.fixture
def client_credentials():
    """Fixture providing test client credentials."""
    return {"client_id": "test_client_id", "client_secret": "test_client_secret"}


@pytest.fixture
def mock_course_response():
    """Fixture providing mock course API response."""
    return {
        "results": [
            {
                "_class": "course",
                "id": 12345,
                "title": "Test Python Course",
                "url": "https://www.udemy.com/test-python-course/",
                "is_paid": True,
                "price": "19.99",
                "price_detail": {"_class": "price_detail", "amount": 1999, "currency": "USD"},
                "visible_instructors": [
                    {
                        "_class": "instructor",
                        "id": 678,
                        "title": "Test Instructor",
                        "display_name": "John Doe",
                    }
                ],
                "image_480x270": "https://example.com/image.jpg",
                "locale": {"_class": "locale", "locale": "en_US"},
            }
        ]
    }


@pytest.fixture
def mock_course_detail_response():
    """Fixture providing mock course detail API response."""
    return {
        "_class": "course",
        "id": 12345,
        "title": "Test Python Course",
        "url": "https://www.udemy.com/test-python-course/",
        "is_paid": True,
        "price": "19.99",
        "price_detail": {"_class": "price_detail", "amount": 1999, "currency": "USD"},
        "visible_instructors": [
            {
                "_class": "instructor",
                "id": 678,
                "title": "Test Instructor",
                "display_name": "John Doe",
            }
        ],
        "image_480x270": "https://example.com/image.jpg",
        "locale": {"_class": "locale", "locale": "en_US"},
    }


@pytest.fixture
def mock_review_response():
    """Fixture providing mock review API response."""
    return {
        "results": [
            {
                "_class": "course_review",
                "id": 987,
                "content": "Great course!",
                "rating": 5,
                "created": "2023-01-01T00:00:00Z",
                "modified": "2023-01-01T00:00:00Z",
                "user": {"_class": "user", "id": 456, "display_name": "Jane Smith"},
                "course": {"_class": "course", "id": 12345, "title": "Test Python Course"},
            }
        ]
    }


@pytest.fixture
def mock_curriculum_response():
    """Fixture providing mock curriculum API response."""
    return {
        "results": [
            {
                "_class": "chapter",
                "id": 1,
                "title": "Introduction",
                "description": "Course introduction",
            },
            {
                "_class": "lecture",
                "id": 2,
                "title": "Getting Started",
                "asset": {"_class": "asset", "id": 123, "title": "Introduction Video"},
            },
            {
                "_class": "quiz",
                "id": 3,
                "title": "Knowledge Check",
                "duration": 300,
                "pass_percent": 80.0,
            },
        ]
    }


@pytest.fixture
def mock_http_error_response():
    """Fixture providing mock HTTP error response."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    return mock_response


@pytest.fixture
def sync_client(client_credentials):
    """Fixture providing a sync UdemyClient instance."""
    return UdemyClient(**client_credentials)


@pytest.fixture
def async_client(client_credentials):
    """Fixture providing an async UdemyClient instance."""
    return AsyncUdemyClient(**client_credentials)


@pytest.fixture
def mock_httpx_get():
    """Fixture for mocking httpx.get."""
    with patch("httpx.get") as mock_get:
        yield mock_get


@pytest.fixture
def mock_httpx_async_client():
    """Fixture for mocking httpx.AsyncClient."""
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = Mock()
        mock_client.return_value.__aenter__.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def sample_course_filter_data():
    """Sample data for testing CourseFilter."""
    return {
        "search": "python",
        "page": 1,
        "page_size": 10,
        "category": "Development",
        "price": "paid",
    }


@pytest.fixture
def sample_review_filter_data():
    """Sample data for testing ReviewFilter."""
    return {"page": 1, "page_size": 20, "rating": 5}
