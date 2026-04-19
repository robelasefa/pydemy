"""Tests for the synchronous UdemyClient."""

import pytest
from unittest.mock import Mock, patch
import httpx

from pydemy import UdemyClient
from pydemy._exceptions import UdemyAPIError
from pydemy.models import CourseFilter, ReviewFilter


class TestUdemyClient:
    """Test cases for UdemyClient."""

    def test_client_initialization(self, client_credentials):
        """Test client initialization with valid credentials."""
        client = UdemyClient(**client_credentials)
        assert client.client_id == client_credentials["client_id"]
        assert client.client_secret == client_credentials["client_secret"]
        assert client.base_url == "https://www.udemy.com/api-2.0/"

    def test_client_initialization_missing_client_id(self, client_credentials):
        """Test client initialization fails with missing client_id."""
        credentials = client_credentials.copy()
        credentials.pop("client_id")
        with pytest.raises(UdemyAPIError, match="client_id is required"):
            UdemyClient(**credentials)

    def test_client_initialization_missing_client_secret(self, client_credentials):
        """Test client initialization fails with missing client_secret."""
        credentials = client_credentials.copy()
        credentials.pop("client_secret")
        with pytest.raises(UdemyAPIError, match="client_secret is required"):
            UdemyClient(**credentials)

    def test_base_url_readonly(self, sync_client):
        """Test that base_url is read-only."""
        with pytest.raises(ValueError, match="Base URL cannot be changed"):
            sync_client.base_url = "https://example.com"

    def test_set_client_id(self, sync_client):
        """Test setting client_id updates authentication."""
        new_id = "new_client_id"
        sync_client.client_id = new_id
        assert sync_client.client_id == new_id
        assert sync_client.auth.username == new_id

    def test_set_client_secret(self, sync_client):
        """Test setting client_secret updates authentication."""
        new_secret = "new_client_secret"
        sync_client.client_secret = new_secret
        assert sync_client.client_secret == new_secret
        assert sync_client.auth.password == new_secret

    def test_set_timeout_valid(self, sync_client):
        """Test setting valid timeout."""
        sync_client.timeout = 10
        assert sync_client.timeout.timeout == 10

    def test_set_timeout_invalid(self, sync_client):
        """Test setting invalid timeout raises ValueError."""
        with pytest.raises(ValueError, match="Timeout value must be non-negative"):
            sync_client.timeout = -1

    @patch('httpx.get')
    def test_get_courses_success(self, mock_get, sync_client, mock_course_response):
        """Test successful course retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = mock_course_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        courses = sync_client.get_courses()
        
        assert len(courses) == 1
        assert courses[0].id == 12345
        assert courses[0].title == "Test Python Course"
        mock_get.assert_called_once()

    @patch('httpx.get')
    def test_get_courses_with_filters(self, mock_get, sync_client, mock_course_response, sample_course_filter_data):
        """Test course retrieval with filters."""
        mock_response = Mock()
        mock_response.json.return_value = mock_course_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        filters = CourseFilter(**sample_course_filter_data)
        courses = sync_client.get_courses(filters)
        
        assert len(courses) == 1
        mock_get.assert_called_once()
        
        # Check that query parameters were passed
        call_args = mock_get.call_args
        assert 'params' in call_args.kwargs

    @patch('httpx.get')
    def test_get_courses_http_error(self, mock_get, sync_client):
        """Test HTTP error handling in get_courses."""
        mock_get.side_effect = httpx.HTTPStatusError("404 Not Found", request=Mock(), response=Mock(status_code=404))
        
        with pytest.raises(UdemyAPIError, match="HTTP error 404"):
            sync_client.get_courses()

    @patch('httpx.get')
    def test_get_courses_request_error(self, mock_get, sync_client):
        """Test request error handling in get_courses."""
        mock_get.side_effect = httpx.RequestError("Connection error")
        
        with pytest.raises(UdemyAPIError, match="Request error"):
            sync_client.get_courses()

    @patch('httpx.get')
    def test_get_courses_json_error(self, mock_get, sync_client):
        """Test JSON parsing error handling in get_courses."""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with pytest.raises(UdemyAPIError, match="JSON parsing error"):
            sync_client.get_courses()

    @patch('httpx.get')
    def test_get_course_details_success(self, mock_get, sync_client, mock_course_detail_response):
        """Test successful course details retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = mock_course_detail_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        course = sync_client.get_course_details(12345)
        
        assert course.id == 12345
        assert course.title == "Test Python Course"
        mock_get.assert_called_once()

    @patch('httpx.get')
    def test_get_course_reviews_success(self, mock_get, sync_client, mock_review_response):
        """Test successful course reviews retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = mock_review_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        reviews = sync_client.get_course_reviews(12345)
        
        assert len(reviews) == 1
        assert reviews[0].id == 987
        assert reviews[0].content == "Great course!"
        mock_get.assert_called_once()

    @patch('httpx.get')
    def test_get_course_reviews_with_filters(self, mock_get, sync_client, mock_review_response, sample_review_filter_data):
        """Test course reviews retrieval with filters."""
        mock_response = Mock()
        mock_response.json.return_value = mock_review_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        filters = ReviewFilter(**sample_review_filter_data)
        reviews = sync_client.get_course_reviews(12345, filters)
        
        assert len(reviews) == 1
        mock_get.assert_called_once()
        
        # Check that query parameters were passed
        call_args = mock_get.call_args
        assert 'params' in call_args.kwargs

    @patch('httpx.get')
    def test_get_course_public_curriculum_success(self, mock_get, sync_client, mock_curriculum_response):
        """Test successful curriculum retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = mock_curriculum_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        curriculum = sync_client.get_course_public_curriculum(12345)
        
        assert len(curriculum) == 3
        mock_get.assert_called_once()

    @patch('httpx.get')
    def test_get_course_public_curriculum_with_pagination(self, mock_get, sync_client, mock_curriculum_response):
        """Test curriculum retrieval with pagination parameters."""
        mock_response = Mock()
        mock_response.json.return_value = mock_curriculum_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        curriculum = sync_client.get_course_public_curriculum(12345, page=2, page_size=20)
        
        assert len(curriculum) == 3
        mock_get.assert_called_once()
        
        # Check that pagination parameters were passed
        call_args = mock_get.call_args
        assert 'params' in call_args.kwargs
        assert call_args.kwargs['params']['page'] == 2
        assert call_args.kwargs['params']['page_size'] == 20

    @patch('httpx.get')
    def test_get_course_public_curriculum_parsing_chapter(self, mock_get, sync_client):
        """Test curriculum parsing for chapter entries."""
        response_data = {
            "results": [
                {
                    "_class": "chapter",
                    "id": 1,
                    "title": "Introduction",
                    "description": "Course introduction"
                }
            ]
        }
        mock_response = Mock()
        mock_response.json.return_value = response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        curriculum = sync_client.get_course_public_curriculum(12345)
        
        assert len(curriculum) == 1
        assert curriculum[0]["_class"] == "chapter"
        assert curriculum[0]["title"] == "Introduction"

    @patch('httpx.get')
    def test_get_course_public_curriculum_parsing_lecture(self, mock_get, sync_client):
        """Test curriculum parsing for lecture entries."""
        response_data = {
            "results": [
                {
                    "_class": "lecture",
                    "id": 2,
                    "title": "Getting Started",
                    "asset": {
                        "_class": "asset",
                        "id": 123,
                        "title": "Introduction Video"
                    }
                }
            ]
        }
        mock_response = Mock()
        mock_response.json.return_value = response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        curriculum = sync_client.get_course_public_curriculum(12345)
        
        assert len(curriculum) == 1
        assert curriculum[0]._class == "lecture"
        assert curriculum[0].title == "Getting Started"

    @patch('httpx.get')
    def test_get_course_public_curriculum_parsing_quiz(self, mock_get, sync_client):
        """Test curriculum parsing for quiz entries."""
        response_data = {
            "results": [
                {
                    "_class": "quiz",
                    "id": 3,
                    "title": "Knowledge Check",
                    "duration": 300,
                    "pass_percent": 80.0
                }
            ]
        }
        mock_response = Mock()
        mock_response.json.return_value = response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        curriculum = sync_client.get_course_public_curriculum(12345)
        
        assert len(curriculum) == 1
        assert curriculum[0]["_class"] == "quiz"
        assert curriculum[0]["title"] == "Knowledge Check"

    @patch('httpx.get')
    def test_get_course_public_curriculum_unexpected_class(self, mock_get, sync_client):
        """Test curriculum parsing with unexpected class type."""
        response_data = {
            "results": [
                {
                    "_class": "unknown_type",
                    "id": 4,
                    "title": "Unknown Item"
                }
            ]
        }
        mock_response = Mock()
        mock_response.json.return_value = response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        curriculum = sync_client.get_course_public_curriculum(12345)
        
        assert len(curriculum) == 0  # Unexpected types should be ignored

    @patch('httpx.get')
    def test_get_courses_invalid_response_format(self, mock_get, sync_client):
        """Test handling of invalid response format."""
        mock_response = Mock()
        mock_response.json.return_value = {"invalid": "format"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(UdemyAPIError, match="Unexpected response format"):
            sync_client.get_courses()

    def test_context_manager(self, client_credentials):
        """Test context manager functionality."""
        with UdemyClient(**client_credentials) as client:
            assert isinstance(client, UdemyClient)
            assert hasattr(client, '_http_client')
        
        # After exiting context, client should still exist but http_client might be closed
        assert isinstance(client, UdemyClient)
