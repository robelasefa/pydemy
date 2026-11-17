"""Mixins for model serialization."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, model_serializer


class DateTimeSerializer(BaseModel):
    """Mixin class for serializing datetime fields to ISO 8601 format."""

    @model_serializer()
    def serialize_datetimes(self) -> dict[str, Any]:
        """
        Serializes the model to a dictionary.

        Converts datetime fields to ISO 8601 format for JSON compatibility,
        recursing into nested models, lists, and dictionaries.
        """

        def _serialize(value: Any) -> Any:
            if isinstance(value, datetime):
                return value.isoformat()
            if isinstance(value, BaseModel):
                return {
                    name: _serialize(getattr(value, name)) for name in type(value).model_fields
                }
            if isinstance(value, list):
                return [_serialize(item) for item in value]
            if isinstance(value, tuple):
                return [_serialize(item) for item in value]
            if isinstance(value, dict):
                return {key: _serialize(item) for key, item in value.items()}
            return value

        return {name: _serialize(getattr(self, name)) for name in type(self).model_fields}
