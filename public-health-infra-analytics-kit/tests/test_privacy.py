import pytest
from phiak.core.privacy import assert_no_forbidden_fields
from phiak.core.errors import PrivacyViolationError


def test_privacy_rejects_forbidden_key():
    with pytest.raises(PrivacyViolationError):
        assert_no_forbidden_fields({"name": "bad"})


def test_privacy_allows_aggregate():
    assert_no_forbidden_fields({"cases": 12, "geo_id": "X"})
