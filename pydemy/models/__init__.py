"""Pydantic models for API interactions."""

__all__ = [
    # Course-related models
    "Course",
    "CourseCategory",
    "CourseSubcategory",
    "CourseReview",
    "CourseFilter",  # Filter for courses
    "ReviewFilter",  # Filter for reviews
    "Instructor",
    "Locale",
    "PriceDetail",
    # Chapter and Lecture models
    "Chapter",
    "Asset",
    "Lecture",
    # Quiz model
    "Quiz",
    # User model
    "User",
    # Additional filter classes
    "Price",
    "InstructionalLevel",
    "Ordering",
    "Duration",
]

from ._chapter import Chapter
from ._course import Course, Instructor, Locale, PriceDetail
from ._course_category import CourseCategory
from ._course_review import CourseReview
from ._course_subcategory import CourseSubcategory
from ._filters.course_filters import (
    CourseFilter,
    Duration,
    InstructionalLevel,
    Ordering,
    Price,
)
from ._filters.review_filters import ReviewFilter
from ._lecture import Asset, Lecture
from ._quiz import Quiz
from ._user import User
