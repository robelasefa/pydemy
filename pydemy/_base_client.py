from typing import Any, Dict

import httpx

from ._exceptions import UdemyAPIError
from .models._course import Course, Instructor, Locale, PriceDetail
from .models._course_review import CourseReview
from .models._lecture import Asset, Lecture
from .models._user import User


class BaseClient:
    """Base class for Udemy API clients (sync and async)."""

    __base_url = "https://www.udemy.com/api-2.0/"

    def __init__(self, client_id: str, client_secret: str, timeout: int = 5) -> None:
        """
        Initializes the base Udemy client.

        Args:
            client_id (str): Your Udemy client ID.
            client_secret (str): Your Udemy client secret.
            timeout (int, optional): The timeout value in seconds for requests to the Udemy API.
                Defaults to 5.
        Raises:
            UdemyAPIError: If either client_id or client_secret is not provided.
        """
        if not client_id:
            raise UdemyAPIError("The argument client_id is required.")
        if not client_secret:
            raise UdemyAPIError("The argument client_secret is required.")

        self._client_id = client_id
        self._client_secret = client_secret
        self._auth = httpx.BasicAuth(self._client_id, self._client_secret)
        self._timeout = httpx.Timeout(timeout)

    @property
    def base_url(self) -> str:
        """Returns the base URL used when sending requests with relative URLs."""
        return self.__base_url

    @base_url.setter
    def base_url(self, _: str) -> None:
        """Raises a ValueError as the base URL cannot be modified after initialization."""
        raise ValueError("Base URL cannot be changed after initialization.")

    @property
    def client_id(self) -> str:
        """Returns the client ID used for authentication."""
        return self._client_id

    @client_id.setter
    def client_id(self, value: str) -> None:
        """Sets the client ID and redefines the authentication."""
        self._client_id = value
        self._auth = httpx.BasicAuth(self._client_id, self._client_secret)

    @property
    def client_secret(self) -> str:
        """Returns the client secret used for authentication."""
        return self._client_secret

    @client_secret.setter
    def client_secret(self, value: str) -> None:
        """Sets the client secret and redefines the authentication."""
        self._client_secret = value
        self._auth = httpx.BasicAuth(self._client_id, self._client_secret)

    @property
    def auth(self) -> httpx.BasicAuth:
        """Returns the httpx.BasicAuth object used for authentication."""
        return self._auth

    @property
    def timeout(self) -> httpx.Timeout:
        """Returns the httpx.Timeout object used for API requests."""
        return self._timeout

    @timeout.setter
    def timeout(self, value: int) -> None:
        """Sets the timeout value for API requests in seconds."""
        if value < 0:
            raise ValueError("Timeout value must be non-negative")
        self._timeout = httpx.Timeout(value)

    @staticmethod
    def _parse_entry(entry_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses an entry dictionary from the Udemy API response, removing the _class key
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
