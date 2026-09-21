"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from pydemy.models import (
    Asset,
    Chapter,
    Course,
    CourseFilter,
    CourseReview,
    Instructor,
    Lecture,
    Locale,
    PriceDetail,
    Quiz,
    ReviewFilter,
    User,
)


class TestCourseFilter:
    """Test cases for CourseFilter model."""

    def test_course_filter_empty(self):
        """Test empty CourseFilter creation."""
        filter_obj = CourseFilter()
        assert filter_obj.model_dump(exclude_unset=True) == {}

    def test_course_filter_with_search(self):
        """Test CourseFilter with search term."""
        filter_obj = CourseFilter(search="python")
        assert filter_obj.search == "python"
        assert filter_obj.model_dump(exclude_unset=True) == {"search": "python"}

    def test_course_filter_with_multiple_fields(self):
        """Test CourseFilter with multiple fields."""
        filter_obj = CourseFilter(
            search="python", page=2, page_size=20, category="Development", price="paid"
        )
        data = filter_obj.model_dump(exclude_unset=True)
        assert data["search"] == "python"
        assert data["page"] == 2
        assert data["page_size"] == 20
        assert data["category"] == "Development"
        assert data["price"] == "paid"


class TestReviewFilter:
    """Test cases for ReviewFilter model."""

    def test_review_filter_empty(self):
        """Test empty ReviewFilter creation."""
        filter_obj = ReviewFilter()
        assert filter_obj.model_dump(exclude_unset=True) == {}

    def test_review_filter_with_rating(self):
        """Test ReviewFilter with rating."""
        filter_obj = ReviewFilter(rating=5)
        assert filter_obj.rating == 5
        assert filter_obj.model_dump(exclude_unset=True) == {"rating": 5}

    def test_review_filter_with_pagination(self):
        """Test ReviewFilter with pagination."""
        filter_obj = ReviewFilter(page=1, page_size=10)
        data = filter_obj.model_dump(exclude_unset=True)
        assert data["page"] == 1
        assert data["page_size"] == 10


class TestCourse:
    """Test cases for Course model."""

    def test_course_creation_minimal(self):
        """Test Course creation with minimal data."""
        course_data = {"_class": "course", "id": 12345, "title": "Test Course"}
        course = Course(**course_data)
        assert course.id == 12345
        assert course.title == "Test Course"

    def test_course_creation_full(self):
        """Test Course creation with full data."""
        course_data = {
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
        course = Course(**course_data)
        assert course.id == 12345
        assert course.title == "Test Python Course"
        assert course.is_paid is True
        assert course.price == "19.99"
        assert isinstance(course.price_detail, PriceDetail)
        assert course.price_detail.amount == 1999
        assert course.price_detail.currency == "USD"
        assert len(course.visible_instructors) == 1
        assert isinstance(course.visible_instructors[0], Instructor)
        assert course.visible_instructors[0].display_name == "John Doe"
        assert isinstance(course.locale, Locale)
        assert course.locale.locale == "en_US"

    def test_course_without_class_field(self):
        """Test Course creation without _class field."""
        course_data = {"id": 12345, "title": "Test Course"}
        course = Course(**course_data)
        assert course.id == 12345
        assert course.title == "Test Course"


class TestInstructor:
    """Test cases for Instructor model."""

    def test_instructor_creation_minimal(self):
        """Test Instructor creation with minimal data."""
        instructor_data = {"_class": "instructor", "id": 678, "display_name": "John Doe"}
        instructor = Instructor(**instructor_data)
        assert instructor.id == 678
        assert instructor.display_name == "John Doe"

    def test_instructor_creation_full(self):
        """Test Instructor creation with full data."""
        instructor_data = {
            "_class": "instructor",
            "id": 678,
            "title": "Test Instructor",
            "display_name": "John Doe",
            "job_title": "Python Developer",
            "url": "https://example.com/instructor",
        }
        instructor = Instructor(**instructor_data)
        assert instructor.id == 678
        assert instructor.title == "Test Instructor"
        assert instructor.display_name == "John Doe"
        assert instructor.job_title == "Python Developer"
        assert instructor.url == "https://example.com/instructor"


class TestPriceDetail:
    """Test cases for PriceDetail model."""

    def test_price_detail_creation(self):
        """Test PriceDetail creation."""
        price_data = {"_class": "price_detail", "amount": 1999, "currency": "USD"}
        price = PriceDetail(**price_data)
        assert price.amount == 1999
        assert price.currency == "USD"

    def test_price_detail_without_class(self):
        """Test PriceDetail creation without _class."""
        price_data = {"amount": 1999, "currency": "USD"}
        price = PriceDetail(**price_data)
        assert price.amount == 1999
        assert price.currency == "USD"


class TestLocale:
    """Test cases for Locale model."""

    def test_locale_creation(self):
        """Test Locale creation."""
        locale_data = {"_class": "locale", "locale": "en_US"}
        locale = Locale(**locale_data)
        assert locale.locale == "en_US"

    def test_locale_without_class(self):
        """Test Locale creation without _class."""
        locale_data = {"locale": "en_US"}
        locale = Locale(**locale_data)
        assert locale.locale == "en_US"


class TestCourseReview:
    """Test cases for CourseReview model."""

    def test_course_review_creation_minimal(self):
        """Test CourseReview creation with minimal data."""
        review_data = {
            "_class": "course_review",
            "id": 987,
            "content": "Great course!",
            "rating": 5,
        }
        review = CourseReview(**review_data)
        assert review.id == 987
        assert review.content == "Great course!"
        assert review.rating == 5

    def test_course_review_with_user(self):
        """Test CourseReview with user data."""
        review_data = {
            "_class": "course_review",
            "id": 987,
            "content": "Great course!",
            "rating": 5,
            "user": {"_class": "user", "id": 456, "display_name": "Jane Smith"},
        }
        review = CourseReview(**review_data)
        assert review.id == 987
        assert review.content == "Great course!"
        assert review.rating == 5
        assert isinstance(review.user, User)
        assert review.user.display_name == "Jane Smith"


class TestUser:
    """Test cases for User model."""

    def test_user_creation_minimal(self):
        """Test User creation with minimal data."""
        user_data = {"_class": "user", "id": 456, "display_name": "Jane Smith"}
        user = User(**user_data)
        assert user.id == 456
        assert user.display_name == "Jane Smith"

    def test_user_without_class(self):
        """Test User creation without _class."""
        user_data = {"id": 456, "display_name": "Jane Smith"}
        user = User(**user_data)
        assert user.id == 456
        assert user.display_name == "Jane Smith"


class TestChapter:
    """Test cases for Chapter model."""

    def test_chapter_creation(self):
        """Test Chapter creation."""
        chapter_data = {
            "_class": "chapter",
            "id": 1,
            "title": "Introduction",
            "description": "Course introduction",
        }
        chapter = Chapter(**chapter_data)
        assert chapter.id == 1
        assert chapter.title == "Introduction"
        assert chapter.description == "Course introduction"

    def test_chapter_without_class(self):
        """Test Chapter creation without _class."""
        chapter_data = {"id": 1, "title": "Introduction"}
        chapter = Chapter(**chapter_data)
        assert chapter.id == 1
        assert chapter.title == "Introduction"


class TestLecture:
    """Test cases for Lecture model."""

    def test_lecture_creation_minimal(self):
        """Test Lecture creation with minimal data."""
        lecture_data = {"_class": "lecture", "id": 2, "title": "Getting Started"}
        lecture = Lecture(**lecture_data)
        assert lecture.id == 2
        assert lecture.title == "Getting Started"

    def test_lecture_with_asset(self):
        """Test Lecture with asset data."""
        lecture_data = {
            "_class": "lecture",
            "id": 2,
            "title": "Getting Started",
            "asset": {"_class": "asset", "id": 123, "title": "Introduction Video"},
        }
        lecture = Lecture(**lecture_data)
        assert lecture.id == 2
        assert lecture.title == "Getting Started"
        assert isinstance(lecture.asset, Asset)
        assert lecture.asset.id == 123
        assert lecture.asset.title == "Introduction Video"


class TestAsset:
    """Test cases for Asset model."""

    def test_asset_creation(self):
        """Test Asset creation."""
        asset_data = {"_class": "asset", "id": 123, "title": "Introduction Video"}
        asset = Asset(**asset_data)
        assert asset.id == 123
        assert asset.title == "Introduction Video"

    def test_asset_without_class(self):
        """Test Asset creation without _class."""
        asset_data = {"id": 123, "title": "Introduction Video"}
        asset = Asset(**asset_data)
        assert asset.id == 123
        assert asset.title == "Introduction Video"


class TestQuiz:
    """Test cases for Quiz model."""

    def test_quiz_creation(self):
        """Test Quiz creation."""
        quiz_data = {
            "_class": "quiz",
            "id": 3,
            "title": "Knowledge Check",
            "duration": 300,
            "pass_percent": 80.0,
        }
        quiz = Quiz(**quiz_data)
        assert quiz.id == 3
        assert quiz.title == "Knowledge Check"
        assert quiz.duration == 300
        assert quiz.pass_percent == 80.0

    def test_quiz_without_class(self):
        """Test Quiz creation without _class."""
        quiz_data = {"id": 3, "title": "Knowledge Check"}
        quiz = Quiz(**quiz_data)
        assert quiz.id == 3
        assert quiz.title == "Knowledge Check"


class TestModelValidation:
    """Test cases for model validation."""

    def test_course_filter_invalid_type(self):
        """Test CourseFilter with invalid data type."""
        with pytest.raises(ValidationError):
            CourseFilter(page="invalid_page")

    def test_review_filter_invalid_rating(self):
        """Test ReviewFilter with invalid rating."""
        with pytest.raises(ValidationError):
            ReviewFilter(rating=6)  # Rating should be 1-5

    def test_course_missing_required_field(self):
        """Test Course missing required field."""
        with pytest.raises(ValidationError):
            Course(title="Test Course")  # Missing required id field

    def test_instructor_missing_required_field(self):
        """Test Instructor missing required field."""
        with pytest.raises(ValidationError):
            Instructor(id=678)  # Missing required display_name field
