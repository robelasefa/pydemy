"""Pydantic models representing a Lecture and nested Asset object."""

from datetime import datetime
from typing import Optional

from ._mixins.serializers import DateTimeSerializer


class Asset(DateTimeSerializer):
    """
    Pydantic model for an asset associated with a lecture (e.g., video) from the Udemy API
    response.

    **Note:** This object structure is inferred from the API response and might not be explicitly
    documented by Udemy.
    """

    id: int
    asset_type: str
    title: str
    created: datetime


class Lecture(DateTimeSerializer):
    """
    Pydantic model for a Lecture object from the Udemy API response.

    **Note:** All attributes except "title" are present in the API response but not
    explicitly documented by Udemy.
    """

    id: int
    title: str
    created: datetime
    description: str
    title_cleaned: str
    is_published: bool
    transcript: Optional[str] = None
    is_downloadable: bool
    is_free: bool
    asset: Asset
    sort_order: int
    can_be_previewed: bool
