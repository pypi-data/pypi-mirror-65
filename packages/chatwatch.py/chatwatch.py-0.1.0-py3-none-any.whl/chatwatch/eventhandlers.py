"""
Module for all the event handlers
"""
from asyncio import AbstractEventLoop, sleep, Event
from logging import Logger, getLogger
from typing import Coroutine, Dict

from .errors import MaxListenersExceeded
from .messageresponse import MessageResponse
from .settings import base_logger


# TODO: Splice MessageEventHandler and EventHandler???
class MessageEventHandler:
    """
    Event handler
    """

    def __init__(self, loop: AbstractEventLoop):
        """
        :param loop: The asyncio loop to use
        """
        self.hooks: Dict[int, Event] = {}
        self.handlers: list = []
        self.response_cache: dict = {}
        self.logger: Logger = getLogger(base_logger + "eventhandlers")
        self.loop: AbstractEventLoop = loop

    async def dispatch(self, data: dict):
        """
        Dispatch a message
        :param data: The data to send
        """
        message = MessageResponse(data)
        self.logger.debug(f"Received response for {message.message_id}")
        if message.message_id not in self.hooks.keys() and len(self.handlers) == 0:
            return
        self.response_cache[message.message_id] = message
        self.hooks[message.message_id].set()
        for handler in self.handlers:
            self.loop.create_task(handler(message))
        await sleep(10)
        del self.hooks[message.message_id]

    async def wait_for(self, message_id: int):
        """
        Waits for a message
        :param message_id: The message id to wait for
        :return: The message response
        """
        if message_id not in self.hooks.keys():
            self.hooks[message_id] = Event(loop=self.loop)
            self.logger.debug(f"Creating hook point for message: {message_id}")
        else:
            self.logger.debug(f"Hook already exists for message: {message_id}")
        await self.hooks[message_id].wait()
        return await self.get_response(message_id)

    async def get_response(self, message_id: int):
        """
        Gets the message response. Can only be accessed 10 seconds after the response
        :param message_id: The message to look for
        :return: The message or none
        """
        try:
            return self.response_cache[message_id]
        except KeyError:
            self.logger.error("Found no response.")
            return None

    def register_event_handler(self, func: Coroutine):
        """
        Adds a message handler
        :param func: The function to add
        """
        self.handlers.append(func)


class EventHandler:
    """
    Generic event handler
    """

    def __init__(self, loop: AbstractEventLoop):
        """
        :param loop: The asyncio loop to use
        """
        self.loop: AbstractEventLoop = loop

        self.max_listeners = 6

        self.hooks: dict = {}
        self.logger: Logger = getLogger(base_logger + "eventhandlers")

    async def dispatch(self, event_type: str, event_data: dict):
        """
        Dispatch a general event
        :param event_type: The event type
        :param event_data: The event data
        """
        event_type = "on_" + event_type
        if event_type not in self.hooks.keys():
            self.logger.debug("No handlers registered for event {}".format(event_type))
            return
        self.logger.debug("Dispatching event: {}".format(event_type))
        for hook in self.hooks[event_type]:
            self.loop.create_task(hook(event_data))

    def register_event_handler(self, func, event_type: str = None):
        """
        Adds a event handler
        :param func: The function to add
        :param event_type: What event to subscribe to
        """
        if event_type is None:
            event_type = func.__name__
        if event_type not in self.hooks.keys():
            self.hooks[event_type] = []
        if len(self.hooks[event_type]) > self.max_listeners:
            raise MaxListenersExceeded(self.max_listeners, event_type)
        self.logger.debug("Registred new event handler for {}".format(event_type))
        self.hooks[event_type].append(func)
