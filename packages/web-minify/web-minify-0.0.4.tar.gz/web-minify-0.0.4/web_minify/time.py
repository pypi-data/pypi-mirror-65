import datetime

import logging

logger = logging.getLogger(__name__)


def human_delta(td_object: datetime.timedelta, max: int = 0):
    ms = int(td_object.total_seconds() * 1000)
    if ms < 1:
        return f"{ms} ms"
    # fmt: off
    periods = [
        ("year",  1000 * 60 * 60 * 24 * 365),
        ("month", 1000 * 60 * 60 * 24 * 30),
        ("day",   1000 * 60 * 60 * 24),
        ("hr",    1000 * 60 * 60),
        ("min",   1000 * 60),
        ("sec",   1000),
        ("ms", 1)
    ]
    # fmt: on

    strings = []
    ct: int = 0
    for period_name, period_ms in periods:
        if ms > period_ms:
            period_value, ms = divmod(ms, period_ms)
            # has_s = "s" if period_value > 1 else ""
            # strings.append("%s %s%s" % (period_value, period_name, has_s))
            strings.append(f"{period_value} {period_name}")
            ct += 1
            if max > 0 and ct > max:
                break
    return ", ".join(strings)  # + f"({td_object}, {ms})"
