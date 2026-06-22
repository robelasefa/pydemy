"""Tests for the asynchronous AsyncUdemyClient."""

from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

from pydemy import AsyncUdemyClient
from pydemy._exceptions import UdemyAPIError
from pydemy.models import CourseFilter, ReviewFilter


class TestAsyncUdemyClient:
    """Test cases for AsyncUdemyClient."""

    def test_async_client_initialization(self, client_credentials):
        """Test async client initialization with valid credentials."""
        client = AsyncUdemyClient(**client_credentials)
        assert client.client_id == client_credentials["client_id"]
        assert client.client_secret == client_credentials["client_secret"]
        assert client.base_url == "https://www.udemy.com/api-2.0/"

    def test_async_client_initialization_missing_client_id(self, client_credentials):
        """Test async client initialization fails with missing client_id."""
        credentials = client_credentials.copy()
        credentials.pop("client_id")
        with pytest.raises(UdemyAPIError, match="client_id is required"):
            AsyncUdemyClient(**credentials)

    def test_async_client_initialization_missing_client_secret(self, client_credentials):
        """Test async client initialization fails with missing client_secret."""
        credentials = client_credentials.copy()
        credentials.pop("client_secret")
        with pytest.raises(UdemyAPIError, match="client_secret is required"):
            AsyncUdemyClient(**credentials)

    @pytest.mark.asyncio
    async def test_async_context_manager(self, client_credentials):
        """Test async context manager functionality."""
        async with AsyncUdemyClient(**client_credentials) as client:
            assert isinstance(client, AsyncUdemyClient)
            assert hasattr(client, "_http_client")

        # After exiting context, client should still exist
        assert isinstance(client, AsyncUdemyClient)

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_courses_success(
        self, mock_async_client_class, async_client, mock_course_response
    ):
        """Test successful async course retrieval."""
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_course_response
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        courses = await async_client.get_courses()

        assert len(courses) == 1
        assert courses[0].id == 12345
        assert courses[0].title == "Test Python Course"
        mock_client_instance.get.assert_called_once()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_courses_with_filters(
        self,
        mock_async_client_class,
        async_client,
        mock_course_response,
        sample_course_filter_data,
    ):
        """Test async course retrieval with filters."""
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_course_response
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        filters = CourseFilter(**sample_course_filter_data)
        courses = await async_client.get_courses(filters)

        assert len(courses) == 1
        mock_client_instance.get.assert_called_once()

        # Check that query parameters were passed
        call_args = mock_client_instance.get.call_args
        assert "params" in call_args.kwargs

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_courses_http_error(self, mock_async_client_class, async_client):
        """Test HTTP error handling in async get_courses."""
        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=Mock(), response=Mock(status_code=404)
        )
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        with pytest.raises(UdemyAPIError, match="HTTP error 404"):
            await async_client.get_courses()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_courses_request_error(self, mock_async_client_class, async_client):
        """Test request error handling in async get_courses."""
        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = httpx.RequestError("Connection error")
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        with pytest.raises(UdemyAPIError, match="Request error"):
            await async_client.get_courses()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_courses_json_error(self, mock_async_client_class, async_client):
        """Test JSON parsing error handling in async get_courses."""
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        with pytest.raises(UdemyAPIError, match="JSON parsing error"):
            await async_client.get_courses()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_course_details_success(
        self, mock_async_client_class, async_client, mock_course_detail_response
    ):
        """Test successful async course details retrieval."""
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_course_detail_response
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        course = await async_client.get_course_details(12345)

        assert course.id == 12345
        assert course.title == "Test Python Course"
        mock_client_instance.get.assert_called_once()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_course_reviews_success(
        self, mock_async_client_class, async_client, mock_review_response
    ):
        """Test successful async course reviews retrieval."""
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_review_response
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        reviews = await async_client.get_course_reviews(12345)

        assert len(reviews) == 1
        assert reviews[0].id == 987
        assert reviews[0].content == "Great course!"
        mock_client_instance.get.assert_called_once()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_course_reviews_with_filters(
        self,
        mock_async_client_class,
        async_client,
        mock_review_response,
        sample_review_filter_data,
    ):
        """Test async course reviews retrieval with filters."""
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_review_response
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        filters = ReviewFilter(**sample_review_filter_data)
        reviews = await async_client.get_course_reviews(12345, filters)

        assert len(reviews) == 1
        mock_client_instance.get.assert_called_once()

        # Check that query parameters were passed
        call_args = mock_client_instance.get.call_args
        assert "params" in call_args.kwargs

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_course_public_curriculum_success(
        self, mock_async_client_class, async_client, mock_curriculum_response
    ):
        """Test successful async curriculum retrieval."""
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_curriculum_response
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        curriculum = await async_client.get_course_public_curriculum(12345)

        assert len(curriculum) == 3
        mock_client_instance.get.assert_called_once()

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_course_public_curriculum_with_pagination(
        self, mock_async_client_class, async_client, mock_curriculum_response
    ):
        """Test async curriculum retrieval with pagination parameters."""
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_curriculum_response
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        curriculum = await async_client.get_course_public_curriculum(12345, page=2, page_size=20)

        assert len(curriculum) == 3
        mock_client_instance.get.assert_called_once()

        # Check that pagination parameters were passed
        call_args = mock_client_instance.get.call_args
        assert "params" in call_args.kwargs
        assert call_args.kwargs["params"]["page"] == 2
        assert call_args.kwargs["params"]["page_size"] == 20

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_course_public_curriculum_parsing_chapter(
        self, mock_async_client_class, async_client
    ):
        """Test async curriculum parsing for chapter entries."""
        response_data = {
            "results": [
                {
                    "_class": "chapter",
                    "id": 1,
                    "title": "Introduction",
                    "description": "Course introduction",
                }
            ]
        }
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = response_data
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        curriculum = await async_client.get_course_public_curriculum(12345)

        assert len(curriculum) == 1
        assert curriculum[0]["_class"] == "chapter"
        assert curriculum[0]["title"] == "Introduction"

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_course_public_curriculum_parsing_lecture(
        self, mock_async_client_class, async_client
    ):
        """Test async curriculum parsing for lecture entries."""
        response_data = {
            "results": [
                {
                    "_class": "lecture",
                    "id": 2,
                    "title": "Getting Started",
                    "asset": {"_class": "asset", "id": 123, "title": "Introduction Video"},
                }
            ]
        }
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = response_data
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        curriculum = await async_client.get_course_public_curriculum(12345)

        assert len(curriculum) == 1
        assert curriculum[0]._class == "lecture"
        assert curriculum[0].title == "Getting Started"

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_course_public_curriculum_parsing_quiz(
        self, mock_async_client_class, async_client
    ):
        """Test async curriculum parsing for quiz entries."""
        response_data = {
            "results": [
                {
                    "_class": "quiz",
                    "id": 3,
                    "title": "Knowledge Check",
                    "duration": 300,
                    "pass_percent": 80.0,
                }
            ]
        }
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = response_data
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        curriculum = await async_client.get_course_public_curriculum(12345)

        assert len(curriculum) == 1
        assert curriculum[0]["_class"] == "quiz"
        assert curriculum[0]["title"] == "Knowledge Check"

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_course_public_curriculum_unexpected_class(
        self, mock_async_client_class, async_client
    ):
        """Test async curriculum parsing with unexpected class type."""
        response_data = {"results": [{"_class": "unknown_type", "id": 4, "title": "Unknown Item"}]}
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = response_data
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        curriculum = await async_client.get_course_public_curriculum(12345)

        assert len(curriculum) == 0  # Unexpected types should be ignored

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient")
    async def test_get_courses_invalid_response_format(
        self, mock_async_client_class, async_client
    ):
        """Test handling of invalid response format in async client."""
        mock_client_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = {"invalid": "format"}
        mock_response.raise_for_status.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client_class.return_value.__aenter__.return_value = mock_client_instance

        with pytest.raises(UdemyAPIError, match="Unexpected response format"):
            await async_client.get_courses()

    @pytest.mark.asyncio
    async def test_async_context_manager_resource_cleanup(self, client_credentials):
        """Test that async context manager properly cleans up resources."""
        client = AsyncUdemyClient(**client_credentials)

        # Mock the aclose method to track if it's called
        with patch.object(httpx.AsyncClient, "aclose", new_callable=AsyncMock) as mock_aclose:
            async with client:
                assert hasattr(client, "_http_client")

            # Verify aclose was called
            mock_aclose.assert_called_once()
