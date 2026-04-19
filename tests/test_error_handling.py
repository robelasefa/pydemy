"""Tests for error handling scenarios."""

from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

from pydemy import AsyncUdemyClient, UdemyClient
from pydemy._exceptions import UdemyAPIError


class TestErrorHandling:
    """Test cases for comprehensive error handling."""

    @pytest.fixture
    def sync_client(self):
        """Create a sync client for testing."""
        return UdemyClient("test_id", "test_secret")

    @pytest.fixture
    def async_client(self):
        """Create an async client for testing."""
        return AsyncUdemyClient("test_id", "test_secret")

    def test_base_client_timeout_validation(self):
        """Test BaseClient timeout validation."""
        client = UdemyClient("test_id", "test_secret")

        # Valid timeout
        client.timeout = 10
        assert client.timeout.timeout == 10

        # Invalid timeout
        with pytest.raises(ValueError, match="Timeout value must be non-negative"):
            client.timeout = -1

    def test_udemy_api_error_creation(self):
        """Test UdemyAPIError exception creation."""
        error = UdemyAPIError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)

    @patch("httpx.get")
    def test_http_status_error_handling(self, mock_get, sync_client):
        """Test HTTP status error handling."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=Mock(), response=mock_response
        )

        with pytest.raises(UdemyAPIError, match="HTTP error 404"):
            sync_client.get_courses()

    @patch("httpx.get")
    def test_http_status_error_500(self, mock_get, sync_client):
        """Test HTTP 500 error handling."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.side_effect = httpx.HTTPStatusError(
            "500 Internal Server Error", request=Mock(), response=mock_response
        )

        with pytest.raises(UdemyAPIError, match="HTTP error 500"):
            sync_client.get_courses()

    @patch("httpx.get")
    def test_http_status_error_401(self, mock_get, sync_client):
        """Test HTTP 401 unauthorized error handling."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.side_effect = httpx.HTTPStatusError(
            "401 Unauthorized", request=Mock(), response=mock_response
        )

        with pytest.raises(UdemyAPIError, match="HTTP error 401"):
            sync_client.get_courses()

    @patch("httpx.get")
    def test_request_error_handling(self, mock_get, sync_client):
        """Test request error handling."""
        mock_get.side_effect = httpx.RequestError("Connection timeout")

        with pytest.raises(UdemyAPIError, match="Request error"):
            sync_client.get_courses()

    @patch("httpx.get")
    def test_request_error_handling_dns(self, mock_get, sync_client):
        """Test DNS resolution error handling."""
        mock_get.side_effect = httpx.RequestError("DNS resolution failed")

        with pytest.raises(UdemyAPIError, match="Request error"):
            sync_client.get_courses()

    @patch("httpx.get")
    def test_json_parsing_error_handling(self, mock_get, sync_client):
        """Test JSON parsing error handling."""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON format")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(UdemyAPIError, match="JSON parsing error"):
            sync_client.get_courses()

    @patch("httpx.get")
    def test_json_parsing_error_empty_response(self, mock_get, sync_client):
        """Test JSON parsing error with empty response."""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Expecting value: line 1 column 1")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(UdemyAPIError, match="JSON parsing error"):
            sync_client.get_courses()

    @patch("httpx.get")
    def test_unexpected_response_format_handling(self, mock_get, sync_client):
        """Test unexpected response format handling."""
        mock_response = Mock()
        mock_response.json.return_value = {"invalid": "format"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(UdemyAPIError, match="Unexpected response format"):
            sync_client.get_courses()

    @patch("httpx.get")
    def test_unexpected_response_format_no_results(self, mock_get, sync_client):
        """Test unexpected response format without results key."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(UdemyAPIError, match="Unexpected response format"):
            sync_client.get_courses()

    @patch("httpx.get")
    def test_unexpected_response_format_non_list_results(self, mock_get, sync_client):
        """Test unexpected response format with non-list results."""
        mock_response = Mock()
        mock_response.json.return_value = {"results": "not_a_list"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(UdemyAPIError, match="Unexpected response format"):
            sync_client.get_courses()

    @patch("httpx.get")
    def test_pydantic_validation_error_handling(self, mock_get, sync_client):
        """Test Pydantic validation error handling."""
        mock_response = Mock()
        # Return invalid data that will fail Pydantic validation
        mock_response.json.return_value = {
            "results": [
                {
                    "_class": "course",
                    "id": "invalid_id",  # Should be int
                    "title": "Test Course",
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(UdemyAPIError):  # Should catch and re-raise as UdemyAPIError
            sync_client.get_courses()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_async_http_status_error_handling(self, mock_async_client_class, async_client):
        """Test async HTTP status error handling."""
        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=Mock(), response=Mock(status_code=404)
        )
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        with pytest.raises(UdemyAPIError, match="HTTP error 404"):
            await async_client.get_courses()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_async_request_error_handling(self, mock_async_client_class, async_client):
        """Test async request error handling."""
        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = httpx.RequestError("Connection timeout")
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        with pytest.raises(UdemyAPIError, match="Request error"):
            await async_client.get_courses()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_async_json_parsing_error_handling(self, mock_async_client_class, async_client):
        """Test async JSON parsing error handling."""
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.side_effect = ValueError("Invalid JSON format")
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        with pytest.raises(UdemyAPIError, match="JSON parsing error"):
            await async_client.get_courses()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_async_unexpected_response_format_handling(
        self, mock_async_client_class, async_client
    ):
        """Test async unexpected response format handling."""
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = {"invalid": "format"}
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        with pytest.raises(UdemyAPIError, match="Unexpected response format"):
            await async_client.get_courses()

    def test_error_chaining_preservation(self):
        """Test that error chaining is preserved."""
        original_error = ValueError("Original error")

        try:
            raise UdemyAPIError("Wrapped error") from original_error
        except UdemyAPIError as e:
            assert e.__cause__ is original_error
            assert str(e.__cause__) == "Original error"

    @patch("httpx.get")
    def test_error_chaining_in_client_methods(self, mock_get, sync_client):
        """Test error chaining in client methods."""
        mock_get.side_effect = httpx.RequestError("Connection error")

        try:
            sync_client.get_courses()
        except UdemyAPIError as e:
            assert e.__cause__ is not None
            assert isinstance(e.__cause__, httpx.RequestError)

    @patch("httpx.get")
    def test_multiple_error_types_in_same_method(self, mock_get, sync_client):
        """Test multiple error types in the same method."""
        # Test HTTP error
        mock_get.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=Mock(), response=Mock(status_code=404)
        )
        with pytest.raises(UdemyAPIError, match="HTTP error 404"):
            sync_client.get_courses()

        # Test request error
        mock_get.side_effect = httpx.RequestError("Connection error")
        with pytest.raises(UdemyAPIError, match="Request error"):
            sync_client.get_courses()

        # Test JSON error
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        with pytest.raises(UdemyAPIError, match="JSON parsing error"):
            sync_client.get_courses()

    def test_base_client_auth_property(self, sync_client):
        """Test BaseClient auth property."""
        assert sync_client.auth.username == "test_id"
        assert sync_client.auth.password == "test_secret"

    def test_base_client_base_url_property(self, sync_client):
        """Test BaseClient base_url property."""
        assert sync_client.base_url == "https://www.udemy.com/api-2.0/"

    def test_base_client_base_url_readonly_enforcement(self, sync_client):
        """Test that base_url property is truly read-only."""
        with pytest.raises(ValueError, match="Base URL cannot be changed"):
            sync_client.base_url = "https://example.com"

    def test_error_message_formatting(self):
        """Test error message formatting."""
        # Test HTTP error message
        error = UdemyAPIError("HTTP error 404: Not Found")
        assert "404" in str(error)
        assert "Not Found" in str(error)

        # Test Request error message
        error = UdemyAPIError("Request error: Connection timeout")
        assert "Connection timeout" in str(error)

        # Test JSON parsing error message
        error = UdemyAPIError("JSON parsing error: Invalid JSON")
        assert "Invalid JSON" in str(error)
