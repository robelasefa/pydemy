"""Pydantic models and enums for filtering course search results on Udemy API."""

from enum import Enum
from typing import Optional, Self

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

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


class CourseFilter(BaseModel):
    """Pydantic model for filtering course search results on the Udemy API."""

    page: Optional[int] = 1
    page_size: Optional[int] = 10
    search: str = ""
    category: Optional[CourseCategory] = None
    subcategory: Optional[CourseSubcategory] = None
    price: Price = None
    is_affiliate_agreed: bool = False
    is_fixed_priced_deals_agreed: bool = False
    is_percentage_deals_agreed: bool = False
    language: Optional[str] = Field(
        default="en", pattern=r"^[a-z]{2}$"
    )  # Filter courses by alpha-2 language code
    has_closed_caption: bool = False
    has_coding_exercises: bool = False
    has_simple_quiz: bool = False
    instructional_level: InstructionalLevel = None
    ordering: Ordering = None
    ratings: str = None
    duration: Duration = None

    @model_validator(mode="after")
    def validate_page_and_size(self) -> Self:
        """
        Validates that the combination of page and page_size does not exceed a limit.

        Raises:
            ValueError: If the product of page and page_size is greater than 10000.
        """
        if (self.page or 0) * (self.page_size or 0) > 10000:
            raise ValueError("page * page_size cannot be greater than 10000")
        return self

    @field_validator("category")
    @classmethod
    def validate_category(cls, category: Optional[CourseCategory]) -> Optional[CourseCategory]:
        """
        Validates if the selected category is present in the available options.

        Args:
            category (CourseCategory, optional): The selected course category.

        Raises:
            ValidationError: If the category is invalid.

        Returns:
            (CourseCategory, optional): The validated category.
        """
        if category and category.title not in CourseCategory.POSSIBLE_CATEGORIES:
            error_messgae = (
                "Invalid course category selected. Please refer to the Udemy documentation "
                "for available categories: https://www.udemy.com/developers/affiliate/models/course-category/"  # pylint: disable=line-too-long
            )
            raise ValidationError(error_messgae)
        return category

    @model_validator(mode="after")
    def validate_subcategory(self) -> Self:
        """
        Validates if the selected subcategory is present in the available options
        for the parent category.

        Raises:
            ValidationError: If the subcategory is invalid or the parent category is missing.
        """
        category = self.category
        subcategory = self.subcategory

        if subcategory:
            if not category:
                raise ValidationError("Please select a parent category for subcategory.")
            if category.title.capitalize() not in CourseSubcategory.POSSIBLE_SUBCATEGORIES:
                error_messgae = (
                    "Invalid course subcategory selected. Please refer to the Udemy documentation "
                    "for available categories: https://www.udemy.com/developers/affiliate/models/course-subcategory/"  # pylint: disable=line-too-long
                )
                raise ValidationError(error_messgae)
        return self
