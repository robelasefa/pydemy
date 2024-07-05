"""Pydantic model representing a Udemy Course Review with a nested User model."""

from datetime import datetime

from .mixins.serializers import DateTimeSerializer
from .user import User


class CourseReview(DateTimeSerializer):
    """Pydantic model for a Course Review on the Udemy API."""

    id: int
    content: str
    rating: float
    created: datetime
    modified: datetime
    user_modified: datetime
    user: User
