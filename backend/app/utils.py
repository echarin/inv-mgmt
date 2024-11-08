from datetime import datetime

import pytz


def float_price_to_string(price: float) -> str:
    return f"{price:.2f}"

def local_time() -> datetime:
    singapore_tz = pytz.timezone('Asia/Singapore')
    return datetime.now(singapore_tz)