from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from panda_spa.schema import BookingSchema

VALID_SERVICES = {"spa", "massage", "facial"}


@pytest.fixture
def mock_registry():
    with patch(
            "panda_spa.validation.ServiceRegistryMeta.get_registry",
            return_value={name: None for name in VALID_SERVICES},
    ):
        yield


def _valid_times():
    start = datetime.now()
    end = start + timedelta(hours=1)
    return start, end


def test_booking_schema_valid(mock_registry):
    start, end = _valid_times()

    booking = BookingSchema(
        user_id=1,
        service_name="spa",
        start_time=start,
        end_time=end,
    )

    assert booking.user_id == 1
    assert booking.service_name == "spa"
    assert booking.start_time == start
    assert booking.end_time == end


def test_booking_schema_invalid_service(mock_registry):
    start, end = _valid_times()

    with pytest.raises(ValidationError) as exc_info:
        BookingSchema(
            user_id=1,
            service_name="invalid",
            start_time=start,
            end_time=end,
        )

    errors = exc_info.value.errors()
    assert len(errors) == 1

    err = errors[0]
    assert err["type"] == "value_error"
    assert err["loc"] == ("service_name",)
    assert "does not exist" in err["msg"]


def test_booking_schema_end_before_start(mock_registry):
    start = datetime.now()
    end = start - timedelta(hours=1)

    with pytest.raises(ValidationError) as exc_info:
        BookingSchema(
            user_id=1,
            service_name="spa",
            start_time=start,
            end_time=end,
        )

    errors = exc_info.value.errors()
    assert len(errors) == 1

    err = errors[0]
    assert err["type"] == "value_error"
    assert err["loc"] == ("end_time",)
    assert "must be after" in err["msg"]


def test_booking_schema_end_equals_start(mock_registry):
    start = datetime.now()
    end = start

    with pytest.raises(ValidationError):
        BookingSchema(
            user_id=1,
            service_name="spa",
            start_time=start,
            end_time=end,
        )


def test_booking_schema_invalid_user_id(mock_registry):
    start, end = _valid_times()

    with pytest.raises(ValidationError):
        BookingSchema(
            user_id=0,  # invalid (gt=0)
            service_name="spa",
            start_time=start,
            end_time=end,
        )


def test_booking_schema_missing_fields(mock_registry):
    start, end = _valid_times()

    with pytest.raises(ValidationError) as exc_info:
        BookingSchema(
            user_id=1,
            service_name="spa",
            start_time=start,
        )

    errors = exc_info.value.errors()
    assert any(err["loc"] == ("end_time",) for err in errors)
