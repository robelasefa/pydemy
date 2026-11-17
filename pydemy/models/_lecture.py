"""Pydantic models representing a Lecture and nested Asset object."""

from datetime import datetime

from ._mixins.serializers import DateTimeSerializer


class Asset(DateTimeSerializer):
    """
    Pydantic model for an asset associated with a lecture (e.g., video) from the Udemy API
    response.

    **Note:** This object structure is inferred from the API response and might not be explicitly
    documented by Udemy.
    """

    id: int
    asset_type: str | None = None
    title: str | None = None
    created: datetime | None = None


class Lecture(DateTimeSerializer):
    """
    Pydantic model for a Lecture object from the Udemy API response.

    **Note:** All attributes except "title" are present in the API response but not
    explicitly documented by Udemy.
    """

    id: int
    title: str | None = None
    created: datetime | None = None
    description: str | None = None
    title_cleaned: str | None = None
    is_published: bool = False
    transcript: str | None = None
    is_downloadable: bool = False
    is_free: bool = False
    asset: Asset | None = None
    sort_order: int = 0
    can_be_previewed: bool = False
