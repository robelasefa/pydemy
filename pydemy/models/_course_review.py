"""Pydantic model representing a Udemy Course Review with a nested User model."""

from datetime import datetime
from typing import Optional

from ._mixins.serializers import DateTimeSerializer
from ._user import User


class CourseReview(DateTimeSerializer):
    """Pydantic model for a Course Review on the Udemy API."""

    id: int
    content: Optional[str] = None
    rating: Optional[float] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    user_modified: Optional[datetime] = None
    user: Optional[User] = None
