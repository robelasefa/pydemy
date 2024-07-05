"""Mixins for model serialization."""

from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, model_serializer


class DateTimeSerializer(BaseModel):
    """Mixin class for serializing datetime fields to ISO 8601 format."""

    @model_serializer()
    def serialize_datetimes(self) -> Dict[str, Any]:
        """
        Serializes the model to a dictionary.

        Converts datetime fields to ISO 8601 format for JSON compatibility.
        """
        model_dict = {}
        for field_name, _ in self.model_fields.items():
            field_value = getattr(self, field_name)
            if isinstance(field_value, datetime):
                model_dict[field_name] = field_value.isoformat()
            else:
                model_dict[field_name] = field_value
        return model_dict
