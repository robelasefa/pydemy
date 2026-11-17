"""Pydantic model representing a Chapter object as inferred from the Udemy API response."""

from datetime import datetime

from ._mixins.serializers import DateTimeSerializer


class Chapter(DateTimeSerializer):
    """
    Pydantic model for a Chapter object from the Udemy API response.

    **Note:** This object structure is inferred from the API response and might not be explicitly
    documented by Udemy.
    """

    id: int
    created: datetime | None = None
    sort_order: int = 0
    title: str | None = None
    description: str | None = None
    is_published: bool = False
