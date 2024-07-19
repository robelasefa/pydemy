"""Interact with the Udemy API for courses, reviews, curriculum, and more."""

from typing import Any, Dict, List, Union, cast

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException

from pydemy.exceptions import UdemyAPIError
from pydemy.models.chapter import Chapter
from pydemy.models.course import Course, Instructor, Locale, PriceDetail
from pydemy.models.course_review import CourseReview
from pydemy.models.filters.course_filters import CourseFilter
from pydemy.models.filters.review_filters import ReviewFilter
from pydemy.models.lecture import Asset, Lecture
from pydemy.models.quiz import Quiz
from pydemy.models.user import User


class UdemyClient:
    """Udemy API client for interacting with courses, reviews, curriculum, and more."""

    __base_url = "https://www.udemy.com/api-2.0/"

    def __init__(self, client_id: str, client_secret: str, timeout: int = 5) -> None:
        """
        Initializes a UdemyClient object.

        Args:
            client_id (str): Your Udemy client ID.
            client_secret (str): Your Udemy client secret.
            timeout (int, optional): The timeout value in seconds for requests to the Udemy API.
                Defaults to 5.
        Raises:
            `UdemyAPIError`: If either client_id or client_secret is not provided.
        """
        if not client_id:
            raise UdemyAPIError("The argument client_id is required.")
        if not client_secret:
            raise UdemyAPIError("The argument client_secret is required.")

        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__auth = HTTPBasicAuth(self.__client_id, self.__client_secret)
        self.__timeout = timeout

    @property
    def client_id(self) -> str:
        """Returns the client ID used for authentication."""
        return self.__client_id

    @property
    def client_secret(self) -> str:
        """Returns the client secret used for authentication."""
        return self.__client_secret

    @property
    def auth(self) -> HTTPBasicAuth:
        """Returns the `HTTPBasicAuth` object used for authentication."""
        return self.__auth

    @property
    def timeout(self) -> int:
        """Returns the timeout value (in seconds) for API requests."""
        return self.__timeout

    @staticmethod
    def _parse_entry(entry_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses an entry dictionary from the Udemy API response, removing the `_class` key
        and transforming it for creating Pydantic objects.

        Args:
            entry_dict (Dict[str, Any]): A dictionary representing an entry from the Udemy API
                response.

        Returns:
            Dict[str, Any]: A modified dictionary suitable for creating a Pydantic object.
        """
        parsed_data = entry_dict.copy()  # Avoid modifying the original dict
        parsed_data.pop("_class", None)

        def parse_nested_model(field_name, model_class):
            if field_name in parsed_data and isinstance(parsed_data[field_name], dict):
                if model_class:
                    parsed_data[field_name] = model_class(**parsed_data[field_name])
                else:
                    pass

        if "_class" in entry_dict:
            # Handle top-level model selection
            model_class = {
                "course": Course,
                "course_review": CourseReview,
                "lecture": Lecture,
            }.get(entry_dict["_class"])

            if model_class:
                for field, value in entry_dict.items():
                    # Parse nested models based on defined classes
                    parse_nested_model(field, User if field == "user" else None)
                    parse_nested_model(field, PriceDetail if field == "price_detail" else None)
                    parse_nested_model(
                        field, Instructor if field == "visible_instructors" else None
                    )
                    parse_nested_model(field, Locale if field == "locale" else None)
                    parse_nested_model(field, Asset if field == "asset" else None)

                    # Handle lists of nested models
                    if isinstance(value, list) and any(isinstance(item, dict) for item in value):
                        model_class_list = {
                            "visible_instructors": Instructor,
                        }.get(field)
                        if model_class_list:
                            parsed_data[field] = [
                                model_class_list(**item) if item else item for item in value
                            ]

        return parsed_data

    def get_courses(self, filters: CourseFilter = CourseFilter()) -> List[Course]:
        """
        Returns a list of Udemy courses based on provided search parameters.

        Args:
            filters (`CourseFilter`, optional): A namedtuple containing optional filters.

        Returns:
            A list of `Course` objects representing the retrieved courses.

        Raises:
            `UdemyAPIError`: If there's an error communicating with the API or the response status
                code indicates an error.
        """

        url = self.__base_url + "courses/"
        query_params = {
            key: str(value) for key, value in filters.model_dump(exclude_unset=True).items()
        }

        try:
            response = requests.get(
                url=url, auth=self.__auth, params=query_params, timeout=self.__timeout
            )
            response.raise_for_status()  # Raise exception for non-200 status codes
            data = response.json()

            # Extract course entries based on the response format
            course_entries = cast(dict, data).get("results", [data])
            if not isinstance(course_entries, list):
                raise UdemyAPIError(f"Unexpected response format: {data}")

            courses = []
            for course_entry in course_entries:
                parsed_entry = self._parse_entry(course_entry)
                course = Course(**parsed_entry)
                courses.append(course)

            return courses

        except RequestException as exc:
            raise UdemyAPIError(f"Error communicating with the API: {exc}") from exc
        except Exception as exc:
            raise UdemyAPIError(f"Unexpected error: {exc}") from exc

    def get_course_details(self, course_id: int) -> Course:
        """
        Retrieves details of a specified course by its ID and returns a `Course` object.

        Args:
            course_id (int): The ID of the course to retrieve details for.

        Returns:
            A `Course` object representing the retrieved course details.

        Raises:
            `UdemyAPIError`: If there's an error communicating with the API or the response
                status code indicates an error.
        """
        url = self.__base_url + f"courses/{course_id}/"

        try:
            response = requests.get(url=url, auth=self.__auth, timeout=self.__timeout)
            response.raise_for_status()  # Raise exception for non-200 status codes
            course_data = response.json()
            parsed_course_data = self._parse_entry(course_data)
            course = Course(**parsed_course_data)

            return course

        except RequestException as exc:
            raise UdemyAPIError(f"Error communicating with the API: {exc}") from exc
        except Exception as exc:
            raise UdemyAPIError(f"Unexpected error: {exc}") from exc

    def get_course_reviews(
        self, course_id: int, filters: ReviewFilter = ReviewFilter()
    ) -> List[CourseReview]:
        """
        Retrieves a list of reviews for a course, with optional filters.

        Args:
            course_id (int): The ID of the course to retrieve reviews for.
            filters (ReviewFilter, optional): A namedtuple containing optional filters.

        Returns:
            A list of `CourseReview` objects representing the retrieved reviews.

        Raises:
            `UdemyAPIError`: If there's an error communicating with the API or the response
                status code indicates an error.
        """
        url = self.__base_url + f"courses/{course_id}/reviews/"
        query_params = {
            key: str(value) for key, value in filters.model_dump(exclude_unset=True).items()
        }

        try:
            response = requests.get(
                url=url, auth=self.__auth, params=query_params, timeout=self.__timeout
            )
            response.raise_for_status()  # Raise exception for non-200 status codes
            data = response.json()

            # Extract course entries based on the response format
            review_entries = cast(dict, data).get("results", [data])
            if not isinstance(review_entries, list):
                raise UdemyAPIError(f"Unexpected response format: {data}")

            reviews = []
            for review_entry in review_entries:
                parsed_entry = self._parse_entry(review_entry)
                review = CourseReview(**parsed_entry)
                reviews.append(review)

            return reviews

        except RequestException as exc:
            raise UdemyAPIError(f"Error communicating with the API: {exc}") from exc
        except Exception as exc:
            raise UdemyAPIError(f"Unexpected error: {exc}") from exc

    def get_course_public_curriculum(
        self, course_id: int, page: int = 1, page_size: int = 10
    ) -> List[Union[Chapter, Quiz, Lecture]]:
        """
        Retrieves the public curriculum list of a specified course.

        Parses the response data into `Chapter`, `Quiz` or `Lecture` objects based on the `_class`
        attribute.

        Args:
            course_id (int): The ID of the course to retrieve the public curriculum list for.
            page (int, optional): Pagination parameter for retrieving specific pages.
                Defaults to None.
            page_size (int, optional): Pagination parameter for specifying the number of items per
                page. Defaults to None.

        Returns:
            A list of `Chapter`, `Quiz` or `Lecture` objects parsed from the API response.

        Raises:
            `UdemyAPIError`: If there's an error communicating with the API or the response
                status code indicates an error.
        """
        url = self.__base_url + f"courses/{course_id}/public-curriculum-items/"
        query_params = {"page": page, "page_size": page_size}

        try:
            response = requests.get(
                url=url, auth=self.__auth, params=query_params, timeout=self.__timeout
            )
            response.raise_for_status()  # Raise exception for non-200 status codes
            data = response.json()

            # Extract course entries based on the response format
            curriculum_entries = cast(dict, data).get("results", [data])
            if not isinstance(curriculum_entries, list):
                raise UdemyAPIError(f"Unexpected response format: {data}")

            curriculums = []
            for entry in curriculum_entries:
                if entry["_class"] == ["chapter", "quiz"]:
                    curriculums.append(entry)  # Chapters and Quizs can be directly added
                elif entry["_class"] == "lecture":
                    parsed_entry = self._parse_entry(entry)
                    curriculums.append(parsed_entry)
                else:
                    # Don't handle unexpected item types
                    pass

        except RequestException as exc:
            raise UdemyAPIError(f"Error communicating with the API: {exc}") from exc
        except Exception as exc:
            raise UdemyAPIError(f"Unexpected error: {exc}") from exc
