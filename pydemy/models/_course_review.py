"""Pydantic model representing a Udemy Course Review with a nested User model."""

from datetime import datetime

from ._mixins.serializers import DateTimeSerializer
from ._user import User


class CourseReview(DateTimeSerializer):
    """Pydantic model for a Course Review on the Udemy API."""

    id: int
    content: str | None = None
    rating: float | None = None
    created: datetime | None = None
    modified: datetime | None = None
    user_modified: datetime | None = None
    user: User | None = None
