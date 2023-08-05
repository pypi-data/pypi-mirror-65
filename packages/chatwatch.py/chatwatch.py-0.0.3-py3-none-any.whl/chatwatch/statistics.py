"""
Internal utility module used for sending statistics
"""
from asyncio import AbstractEventLoop
from logging import Logger, getLogger
from typing import Tuple, Optional

from aiohttp import ClientSession, ClientResponse, ClientConnectionError
from requests import post, Response
from requests.exceptions import ConnectionError as RequestsConnectionError

from .settings import usage_stat_url, base_logger


# WARNING: This is only for statistics, don't bother faking it
class Statistics:
    """
    Utility class for sending statistics about the library
    """
    def __init__(self):
        self.logger: Logger = getLogger(base_logger + "statistics")

    def post_sync_safe(self, *args, **kwargs) -> Optional[Response]:
        """
        Internal method to send a synchronous request, where if any connection error occurs it will return None
        :param args: request.post args
        :param kwargs: request.post kwargs
        :return: Response or None
        """
        try:
            return post(*args, **kwargs)
        except RequestsConnectionError:
            self.logger.debug("Could not connect to update servers")
            return None

    async def post_async_safe(self, *args, **kwargs) -> Optional[ClientResponse]:
        """
        asyncronous version of post_sync_safe
        :param args: ClientSession.post args
        :param kwargs: ClientSession.post kwargs and loop for ClientSession
        :return:
        """
        async with ClientSession(loop=kwargs.get("loop", None)) as session:
            try:
                kwargs.pop("loop")
                return await session.post(*args, **kwargs)
            except ClientConnectionError:
                self.logger.debug("Could not connect to update servers")
                return None

    def register_install(self):
        """
        Utility method for us to send statistics about when the user installs ChatWatch.py
        :return:
        """
        headers = {
            "type": "install"
        }
        self.post_sync_safe(usage_stat_url, headers=headers)
        self.logger.debug("Install statistic has been logged")

    async def register_start(self, loop: AbstractEventLoop):
        """
        Utility method for us to send statistics about when the user is connecting to ChatWatch
        :param loop: asyncio loop used for aiohttp
        :return: None
        """
        headers = {
            "type": "start"
        }
        request = await self.post_async_safe(usage_stat_url, headers=headers, loop=loop)
        if request is None:
            return  # We don't want to log that the statistics has been logged if we couldn't connect to the servers
        self.logger.debug("Start statistic has been logged")

    def check_for_updates(self, current_version: Tuple[int, int, int]):
        """
        Utility method to check for library updates
        :param current_version: version tuple to check against
        :return: None
        """
        major: int = current_version[0]
        minor: int = current_version[1]
        patch: int = current_version[2]

        headers = {
            "type": "check_for_updates",
            "major": str(major),
            "minor": str(minor),
            "patch": str(patch)
        }

        request = self.post_sync_safe(usage_stat_url, headers=headers)
        if request is None:
            return
        data = request.json()
        if not data["up_to_date"]:
            self.logger.warning("WARNING: chatwatch.py is not updated, this could lead to severe security risks. "
                                "Please update to the current version: {}".format(data["latest"]))
        else:
            self.logger.debug("Running on the latest version")
