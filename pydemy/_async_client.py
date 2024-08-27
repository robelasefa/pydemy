"""Asynchronously interact with the Udemy API for courses, reviews, curriculum, and more."""

from typing import List, Self, Union, cast

import httpx

from ._base_client import BaseClient
from ._exceptions import UdemyAPIError
from .models._chapter import Chapter
from .models._course import Course
from .models._course_review import CourseReview
from .models._filters.course_filters import CourseFilter
from .models._filters.review_filters import ReviewFilter
from .models._lecture import Lecture
from .models._quiz import Quiz


class AsyncUdemyClient(BaseClient):
    """Asynchronous client for interacting with the Udemy API."""

    async def __aenter__(self) -> Self:
        """Initializes the client for use within an async with block."""
        # Perform any necessary setup tasks here
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleans up resources when exiting the async with block."""
        # Perform any necessary cleanup tasks here
        pass

    async def get_courses(self, filters: CourseFilter = CourseFilter()) -> List[Course]:
        """
        Retrieves a list of Udemy courses based on provided search parameters asynchronously.

        Args:
            filters (CourseFilter, optional): A namedtuple containing optional filters.

        Returns:
            A list of Course objects representing the retrieved courses.

        Raises:
            UdemyAPIError: If there's an error communicating with the API or the response status
                code indicates an error.
        """

        url = self.__base_url + "courses/"
        query_params = {
            key: str(value) for key, value in filters.model_dump(exclude_unset=True).items()
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=url, params=query_params, auth=self._auth, timeout=self._timeout
                )
                response.raise_for_status()  # Raise exception for non-2xx status codes
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

        except httpx.HTTPError as exc:
            raise UdemyAPIError(f"Error communicating with the API: {exc}") from exc
        except Exception as exc:
            raise UdemyAPIError(f"Unexpected error: {exc}") from exc

    async def get_course_details(self, course_id: int) -> Course:
        """
        Retrieves details of a specified course by its ID and returns a Course object
        asynchronously.

        Args:
            course_id (int): The ID of the course to retrieve details for.

        Returns:
            A Course object representing the retrieved course details.

        Raises:
            UdemyAPIError: If there's an error communicating with the API or the response
                status code indicates an error.
        """
        url = self.__base_url + f"courses/{course_id}/"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=url, auth=self._auth, timeout=self._timeout)
                response.raise_for_status()  # Raise exception for non-2xx status codes
                course_data = response.json()

            parsed_course_data = self._parse_entry(course_data)
            course = Course(**parsed_course_data)

            return course

        except httpx.HTTPError as exc:
            raise UdemyAPIError(f"Error communicating with the API: {exc}") from exc
        except Exception as exc:
            raise UdemyAPIError(f"Unexpected error: {exc}") from exc

    async def get_course_reviews(
        self, course_id: int, filters: ReviewFilter = ReviewFilter()
    ) -> List[CourseReview]:
        """
        Retrieves a list of reviews for a course using review filters asynchronously.

        Args:
            course_id (int): The ID of the course to retrieve reviews for.
            filters (ReviewFilter, optional): A namedtuple containing optional filters.

        Returns:
            A list of CourseReview objects representing the retrieved reviews.

        Raises:
            UdemyAPIError: If there's an error communicating with the API or the response
                status code indicates an error.
        """
        url = self.__base_url + f"courses/{course_id}/reviews/"
        query_params = {
            key: str(value) for key, value in filters.model_dump(exclude_unset=True).items()
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=url, params=query_params, auth=self._auth, timeout=self._timeout
                )
                response.raise_for_status()  # Raise exception for non-2xx status codes
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

        except httpx.HTTPError as exc:
            raise UdemyAPIError(f"Error communicating with the API: {exc}") from exc
        except Exception as exc:
            raise UdemyAPIError(f"Unexpected error: {exc}") from exc

    async def get_course_public_curriculum(
        self, course_id: int, page: int = 1, page_size: int = 10
    ) -> List[Union[Chapter, Quiz, Lecture]]:
        """
        Retrieves the public curriculum list of a specified course asynchronously.

        Parses the response data into Chapter, Quiz or Lecture objects based on the _class
        attribute.

        Args:
            course_id (int): The ID of the course to retrieve the public curriculum list for.
            page (int, optional): Pagination parameter for retrieving specific pages.
                Defaults to None.
            page_size (int, optional): Pagination parameter for specifying the number of items per
                page. Defaults to None.

        Returns:
            A list of Chapter, Quiz or Lecture objects parsed from the API response.

        Raises:
            UdemyAPIError: If there's an error communicating with the API or the response
                status code indicates an error.
        """
        url = self.__base_url + f"courses/{course_id}/public-curriculum-items/"
        query_params = {"page": page, "page_size": page_size}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=url, params=query_params, auth=self._auth, timeout=self._timeout
                )
                response.raise_for_status()  # Raise exception for non-2xx status codes
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

        except httpx.HTTPError as exc:
            raise UdemyAPIError(f"Error communicating with the API: {exc}") from exc
        except Exception as exc:
            raise UdemyAPIError(f"Unexpected error: {exc}") from exc
