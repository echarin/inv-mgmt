from datetime import datetime
from decimal import Decimal

import pytz


def decimal_price_to_string(price: Decimal) -> str:
    return f"{price:.2f}"


def current_local_time() -> datetime:
    singapore_tz = pytz.timezone("Asia/Singapore")
    return datetime.now(singapore_tz)
