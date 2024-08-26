import logging
import time

from app.config import config
from app.functions.exceptions import too_many_requests

logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(self, times: int = 5, seconds: int = 60):
        self.t = times
        self.s = seconds
        self.r: dict[str, list[float]] = {}

    def __call__(self, k: str):
        c = time.time()
        if k not in self.r:
            self.r[k] = []
        self.r[k] = [t for t in self.r[k] if t > c - self.s]
        l = len(self.r[k]) + 1
        if l > self.t:
            n = self.s - c + self.r[k][-1]
            raise too_many_requests(
                msg=f"Too many requests. Wait {round(n, 2)} seconds."
            )
        logger.info(
            f"Call is rate limited. {l}/{self.t} calls in the next {self.s} seconds."
        )
        self.r[k].append(c)


rate_limiter = RateLimiter(*config.RATE_LIMITS)
