from datetime import datetime

from app.utils import current_local_time, decimal_price_to_string


def test_decimal_price_to_string():
    assert decimal_price_to_string(1000) == "1000.00"
    assert decimal_price_to_string(100) == "100.00"
    assert decimal_price_to_string(10) == "10.00"
    assert decimal_price_to_string(1) == "1.00"
    assert decimal_price_to_string(0) == "0.00"


def test_current_local_time():
    local_time_result = current_local_time()

    assert isinstance(local_time_result, datetime)
    assert local_time_result.tzinfo is not None

    # Singapore is GMT+8
    assert (
        local_time_result.utcoffset().total_seconds() == 8 * 3600
    )  # 8 hours in seconds
