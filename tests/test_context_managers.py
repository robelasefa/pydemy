"""Tests for context manager functionality."""

from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

from pydemy import AsyncUdemyClient, UdemyClient


class TestContextManagers:
    """Test cases for context manager functionality."""

    @pytest.fixture
    def client_credentials(self):
        """Fixture providing test client credentials."""
        return {"client_id": "test_client_id", "client_secret": "test_client_secret"}

    def test_sync_context_manager_basic(self, client_credentials):
        """Test basic sync context manager functionality."""
        with UdemyClient(**client_credentials) as client:
            assert isinstance(client, UdemyClient)
            assert hasattr(client, "_http_client")
            assert client.client_id == client_credentials["client_id"]
            assert client.client_secret == client_credentials["client_secret"]

    def test_sync_context_manager_resource_cleanup(self, client_credentials):
        """Test that sync context manager properly cleans up resources."""
        client = UdemyClient(**client_credentials)

        with patch.object(httpx.Client, "close") as mock_close:
            with client:
                assert hasattr(client, "_http_client")

            # Verify close was called
            mock_close.assert_called_once()

    def test_sync_context_manager_exception_handling(self, client_credentials):
        """Test sync context manager with exception."""
        client = UdemyClient(**client_credentials)

        with patch.object(httpx.Client, "close") as mock_close:
            with pytest.raises(ValueError):
                with client:
                    assert hasattr(client, "_http_client")
                    raise ValueError("Test exception")

            # Verify close was still called even with exception
            mock_close.assert_called_once()

    def test_sync_context_manager_reuse(self, client_credentials):
        """Test that client can be reused after context manager."""
        client = UdemyClient(**client_credentials)

        with client:
            assert hasattr(client, "_http_client")

        # Client should still be usable
        assert client.client_id == client_credentials["client_id"]
        assert isinstance(client, UdemyClient)

    @pytest.mark.asyncio
    async def test_async_context_manager_basic(self, client_credentials):
        """Test basic async context manager functionality."""
        async with AsyncUdemyClient(**client_credentials) as client:
            assert isinstance(client, AsyncUdemyClient)
            assert hasattr(client, "_http_client")
            assert client.client_id == client_credentials["client_id"]
            assert client.client_secret == client_credentials["client_secret"]

    @pytest.mark.asyncio
    async def test_async_context_manager_resource_cleanup(self, client_credentials):
        """Test that async context manager properly cleans up resources."""
        client = AsyncUdemyClient(**client_credentials)

        with patch.object(httpx.AsyncClient, "aclose", new_callable=AsyncMock) as mock_aclose:
            async with client:
                assert hasattr(client, "_http_client")

            # Verify aclose was called
            mock_aclose.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_context_manager_exception_handling(self, client_credentials):
        """Test async context manager with exception."""
        client = AsyncUdemyClient(**client_credentials)

        with patch.object(httpx.AsyncClient, "aclose", new_callable=AsyncMock) as mock_aclose:
            with pytest.raises(ValueError):
                async with client:
                    assert hasattr(client, "_http_client")
                    raise ValueError("Test exception")

            # Verify aclose was still called even with exception
            mock_aclose.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_context_manager_reuse(self, client_credentials):
        """Test that async client can be reused after context manager."""
        client = AsyncUdemyClient(**client_credentials)

        async with client:
            assert hasattr(client, "_http_client")

        # Client should still be usable
        assert client.client_id == client_credentials["client_id"]
        assert isinstance(client, AsyncUdemyClient)

    def test_sync_context_manager_without_httpx_client(self, client_credentials):
        """Test sync context manager when httpx.Client doesn't exist."""
        client = UdemyClient(**client_credentials)

        # Should not have _http_client before entering context
        assert not hasattr(client, "_http_client")

        with client:
            # Should have _http_client after entering context
            assert hasattr(client, "_http_client")

    @pytest.mark.asyncio
    async def test_async_context_manager_without_httpx_client(self, client_credentials):
        """Test async context manager when httpx.AsyncClient doesn't exist."""
        client = AsyncUdemyClient(**client_credentials)

        # Should not have _http_client before entering context
        assert not hasattr(client, "_http_client")

        async with client:
            # Should have _http_client after entering context
            assert hasattr(client, "_http_client")

    def test_sync_context_manager_nested(self, client_credentials):
        """Test nested sync context managers."""
        with UdemyClient(**client_credentials) as client1:
            assert hasattr(client1, "_http_client")

            with UdemyClient(**client_credentials) as client2:
                assert hasattr(client2, "_http_client")
                assert client1 is not client2  # Different instances

    @pytest.mark.asyncio
    async def test_async_context_manager_nested(self, client_credentials):
        """Test nested async context managers."""
        async with AsyncUdemyClient(**client_credentials) as client1:
            assert hasattr(client1, "_http_client")

            async with AsyncUdemyClient(**client_credentials) as client2:
                assert hasattr(client2, "_http_client")
                assert client1 is not client2  # Different instances

    def test_sync_context_manager_client_attributes_preserved(self, client_credentials):
        """Test that client attributes are preserved in sync context manager."""
        client = UdemyClient(**client_credentials)
        original_timeout = client.timeout

        with client:
            assert client.timeout == original_timeout
            # Modify timeout within context
            client.timeout = 20

        # Timeout should be preserved after context
        assert client.timeout == 20

    @pytest.mark.asyncio
    async def test_async_context_manager_client_attributes_preserved(self, client_credentials):
        """Test that client attributes are preserved in async context manager."""
        client = AsyncUdemyClient(**client_credentials)
        original_timeout = client.timeout

        async with client:
            assert client.timeout == original_timeout
            # Modify timeout within context
            client.timeout = 20

        # Timeout should be preserved after context
        assert client.timeout == 20

    def test_sync_context_manager_httpx_client_creation(self, client_credentials):
        """Test that httpx.Client is created properly in sync context manager."""
        with patch("httpx.Client") as mock_client_class:
            mock_client_instance = Mock()
            mock_client_class.return_value = mock_client_instance

            with UdemyClient(**client_credentials) as client:
                assert client._http_client is mock_client_instance
                mock_client_class.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_context_manager_httpx_client_creation(self, client_credentials):
        """Test that httpx.AsyncClient is created properly in async context manager."""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client_instance = AsyncMock()
            mock_client_class.return_value = mock_client_instance

            async with AsyncUdemyClient(**client_credentials) as client:
                assert client._http_client is mock_client_instance
                mock_client_class.assert_called_once()
