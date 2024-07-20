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

from .chapter import Chapter
from .course import Course, Instructor, Locale, PriceDetail
from .course_category import CourseCategory
from .course_review import CourseReview
from .course_subcategory import CourseSubcategory
from .filters.course_filters import CourseFilter, Duration, InstructionalLevel, Ordering, Price
from .filters.review_filters import ReviewFilter
from .lecture import Asset, Lecture
from .quiz import Quiz
from .user import User
