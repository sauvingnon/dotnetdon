from datetime import datetime, timezone

def datetime_from_ms_timestamp(ts_ms: int) -> datetime:
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
