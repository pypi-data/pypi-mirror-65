"""
Internal module for ratelimiting
"""
from asyncio import sleep
from logging import Logger, getLogger

from .errors import OutOfAttempts
from .settings import base_logger


class Limiters:  # pylint: disable=too-few-public-methods
    """
    Internal ratelimiters
    """

    def __init__(self):
        self.logger: Logger = getLogger(base_logger + "ratelimiting")

    async def increasing_limiter(
            self, start_delay: int = 3, increase_delay: int = 3, max_delay: int = 60,
            max_attempts: int = -1):
        """
        Ratelimiter that increases in time for every attempt
        :param start_delay: the delay to start at after the first iteration
        :param increase_delay: the delay to add for every iteration
        :param max_delay: The delay will stop increasing when it hits this level
        :param max_attempts: max attempts the ratelimiter will try until it raises an error
        :type start_delay: int
        :type increase_delay: int
        :type max_delay: int
        :type max_attempts: int
        :raises OutOfAttempts:
        """
        current_attempts = 0
        use_attempts = max_attempts != -1
        next_delay = start_delay
        while True:
            self.logger.debug("Running loop")
            yield current_attempts
            current_attempts += 1
            self.logger.debug("Attempt nr.%s. Waiting %ss", current_attempts, next_delay)
            await sleep(next_delay)
            if use_attempts and current_attempts >= max_attempts:
                raise OutOfAttempts(current_attempts)
            if next_delay + increase_delay < max_delay:
                next_delay += increase_delay
            elif next_delay != max_delay:
                next_delay = max_delay
