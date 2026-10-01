from __future__ import annotations

from collections.abc import Iterable


class ValidationError(Exception):
    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}


def validate_required(value: object, field_name: str) -> None:
    if value is None or value == "":
        raise ValidationError(f"{field_name} is required")


def validate_list_not_empty(value: Iterable[object], field_name: str) -> None:
    if value is None or len(list(value)) == 0:
        raise ValidationError(f"{field_name} cannot be empty")
