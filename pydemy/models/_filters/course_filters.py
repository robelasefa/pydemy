"""Pydantic models and enums for filtering course search results on Udemy API."""

from enum import Enum
from typing import Optional, Self

from pydantic import BaseModel, Field, field_validator, model_validator

from .._course_category import CourseCategory
from .._course_subcategory import CourseSubcategory


class Price(Enum):
    """Enumeration representing the possible price options for courses."""

    PRICE_PAID = "price-paid"
    PRICE_FREE = "price-free"


class InstructionalLevel(Enum):
    """Enumeration representing the available instructional levels for courses."""

    ALL = "all"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class Ordering(Enum):
    """Enumeration representing the sorting options for course search results."""

    RELEVANCE = "relevance"
    MOST_REVIEWED = "most-reviewed"
    HIGHEST_RATED = "highest-rated"
    NEWEST = "newest"
    PRICE_LOW_TO_HIGH = "price-low-to-high"
    PRICE_HIGH_TO_LOW = "price-high-to-low"


class Duration(Enum):
    """Enumeration representing the estimated duration categories for courses."""

    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
    EXTRA_LONG = "extraLong"


_PRICE_ALIASES = {
    "paid": Price.PRICE_PAID,
    "free": Price.PRICE_FREE,
    "price-paid": Price.PRICE_PAID,
    "price-free": Price.PRICE_FREE,
}


class CourseFilter(BaseModel):
    """Pydantic model for filtering course search results on the Udemy API."""

    page: Optional[int] = 1
    page_size: Optional[int] = 10
    search: str = ""
    category: Optional[str] = None
    subcategory: Optional[str] = None
    price: Optional[Price] = None
    is_affiliate_agreed: bool = False
    is_fixed_priced_deals_agreed: bool = False
    is_percentage_deals_agreed: bool = False
    language: Optional[str] = Field(default="en", pattern=r"^[a-z]{2}$")
    has_closed_caption: bool = False
    has_coding_exercises: bool = False
    has_simple_quiz: bool = False
    instructional_level: Optional[InstructionalLevel] = None
    ordering: Optional[Ordering] = None
    ratings: Optional[str] = None
    duration: Optional[Duration] = None

    @model_validator(mode="after")
    def validate_page_and_size(self) -> Self:
        if (self.page or 0) * (self.page_size or 0) > 10000:
            raise ValueError("page * page_size cannot be greater than 10000")
        return self

    @field_validator("price", mode="before")
    @classmethod
    def _coerce_price(cls, value):
        if value is None:
            return None
        if isinstance(value, Price):
            return value
        if isinstance(value, str):
            key = value.strip().lower()
            if key in _PRICE_ALIASES:
                return _PRICE_ALIASES[key]
            try:
                return Price(value)
            except ValueError:
                pass
        raise ValueError("Invalid price filter value")

    @field_validator("category", mode="before")
    @classmethod
    def _validate_category(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            if value not in CourseCategory.POSSIBLE_CATEGORIES:
                raise ValueError("Invalid course category")
            return value
        raise ValueError("Invalid course category")

    @field_validator("subcategory", mode="before")
    @classmethod
    def _validate_subcategory(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            if value not in CourseSubcategory.POSSIBLE_SUBCATEGORIES:
                raise ValueError("Invalid course subcategory")
            return value
        raise ValueError("Invalid course subcategory")

    @field_validator("instructional_level", "ordering", "duration", mode="before")
    @classmethod
    def _coerce_enum(cls, value, info):
        if value is None:
            return None
        field = info.field_name
        enum_map = {
            "instructional_level": InstructionalLevel,
            "ordering": Ordering,
            "duration": Duration,
        }[field]
        if isinstance(value, enum_map):
            return value
        if isinstance(value, str):
            try:
                return enum_map(value)
            except ValueError:
                pass
        raise ValueError(f"Invalid {field} value")
