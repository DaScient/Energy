from __future__ import annotations

from typing import Any, Set

from phiak.core.errors import PrivacyViolationError


FORBIDDEN_KEYS: Set[str] = {
    "name", "first_name", "last_name",
    "dob", "date_of_birth",
    "address", "street",
    "phone", "email",
    "mrn", "medical_record_number",
    "patient_id", "ssn",
    "latitude", "longitude", "lat", "lon",
    "notes", "free_text",
}


def assert_no_forbidden_fields(obj: Any, path: str = "") -> None:
    """Best effort scan for forbidden fields.

    This prevents accidental ingestion of obvious person-level fields.
    It is not a de-identification tool.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            k_low = str(k).lower()
            p = f"{path}.{k}" if path else str(k)
            if k_low in FORBIDDEN_KEYS:
                raise PrivacyViolationError(f"Forbidden field detected: {p}")
            assert_no_forbidden_fields(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            assert_no_forbidden_fields(v, f"{path}[{i}]")
    else:
        return
