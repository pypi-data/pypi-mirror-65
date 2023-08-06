"""
The module for ChatWatch clients
"""
from asyncio import wait_for
from logging import Logger, getLogger

from discord import Message
from discord.ext.commands import Bot as DiscordBot

from .errors import NotConnectedError
from .http import HttpClient
from .messageresponse import MessageResponse
from .settings import library_stamp, base_logger, __version__
from .statistics import Statistics


class ManualChatWatchClient:
    """
    Bare bones ChatWatch client. You have to initialize all listeners yourself. Not recommended
    """

    def __init__(self, token: str, client: DiscordBot, *, reconnect: bool = True, silent_connection: bool = False,
                 auto_silence_connection: bool = True):
        """
        :param token: Your ksoft.si token with ChatWatch enabled
        :param client: Your discord bot
        :param reconnect: Whether to automatically reconnect
        :param silent_connection: Silence all connection errors/information
        :param auto_silence_connection: whether to silence all connection errors/information after 3 connection attempts
        :type token: str
        :type client: discord.ext.commands.Bot
        :type reconnect: bool
        :type silent_connection: bool
        :type auto_silence_connection: bool
        """
        self.token: str = token
        self.client: DiscordBot = client

        self.logger: Logger = getLogger(base_logger + "client")
        self.http: HttpClient = HttpClient(token, self.client.loop, reconnect=reconnect,
                                           silent_connection=silent_connection,
                                           auto_silence_connection=auto_silence_connection)
        self.default_events: DefaultEvents = DefaultEvents(self)
        self.statistics = Statistics()
        self.statistics.check_for_updates(__version__)

    async def connect(self):
        """
        Connects to ChatWatch
        :return: None
        """
        await self.http.connect()

    def start_listener(self):
        """
        Starts the listener task
        :return: None
        """
        self.client.loop.create_task(self.http.listener_task())

    async def send(self, data: dict):
        """
        Sends data to ChatWatch via the WebSocket. The same as chatwatch.http.send
        :param data: the data to send
        :type data: dict
        :return: None
        :raises NotConnectedError:
        """
        if not self.http.connected:
            raise NotConnectedError("send")
        # TODO: Implement this
        await self.http.send(data)

    def enable_default_events(self):
        """
        Enabled all default events
        :return: None
        """
        self.event(self.default_events.on_ping)
        self.event(self.default_events.on_resume)
        self.event(self.default_events.on_error)
        self.event(self.default_events.on_message_response)
        self.logger.info("Default events loaded")

    def event(self, func, *, name=None):
        """
        Decorator to add a event listener
        :param func: the function to add
        :param name: optional event name. If not supplied will use function.__name__
        """

        def wrapper(*args, **kwargs):
            self.logger.warning("Events should not be called manually!")
            func(*args, **kwargs)

        if name is None:
            name = func.__name__
        if name == "message":
            self.http.message_event_handler.register_event_handler(func)
        else:
            self.http.event_handler.register_event_handler(func, name)
        return wrapper

    async def register_message(self, message: Message):
        """
        Sends a message to ChatWatch
        :param message: the message to send
        """
        if not isinstance(message, Message):
            raise TypeError("message needs to be of type discord.Message")
        await self.http.send_message(message)

    async def wait_for_message(self, message_id: int, *, timeout: int = None) -> MessageResponse:
        """
        Waits for a message to enter
        :param message_id: the message id to wait for
        :param timeout: How long to wait for before
        :return:
        """
        if not (isinstance(timeout, int) or timeout is None):
            raise TypeError("Timeout has to be of type int")
        return await wait_for(self.http.message_event_handler.wait_for(message_id), timeout, loop=self.client.loop)


class ChatWatchClient(ManualChatWatchClient):
    """
    Automated version of the ManualChatWatchClient
    """

    def __init__(self, token: str, client: DiscordBot, *, reconnect: bool = True, silent_connection: bool = False,
                 auto_silence_connection: bool = True):
        super().__init__(token=token, client=client, reconnect=reconnect, silent_connection=silent_connection,
                         auto_silence_connection=auto_silence_connection)
        self.enable_default_events()
        self.start_listener()
        self.client.loop.create_task(self.connect())
        self.client.add_listener(self.on_message_listener, "on_message")

    async def on_message_listener(self, message: Message):
        """
        Default client listener to submit messages to ChatWatch
        :param message: the message to send
        """
        if message.guild is not None:
            await self.client.wait_until_ready()
            await self.register_message(message)


class DefaultEvents:
    """
    The default event handlers used by ChatWatch.py
    """

    def __init__(self, cw_client: ManualChatWatchClient):
        self.cw_client = cw_client
        self.logger: Logger = getLogger(base_logger + "defaultevents")

    async def on_ping(self, data: dict):  # pylint: disable= unused-argument
        """
        Default event for the ping event
        :param data: event data
        :return: None
        """
        await self.cw_client.send({"event": "pong", "data": library_stamp})

    async def on_resume(self, data: dict):  # pylint: disable= unused-argument
        """
        Default event for the resume event
        :param data: event data
        :return:
        """
        self.logger.info("Resumed cw.py")

    async def on_error(self, data: dict):
        """
        Default event for the error event
        :param data: event data
        :return:
        """
        self.logger.error("Received error from gateway: {}".format(data["message"]))

    async def on_message_response(self, data):
        """
        Default message dispatching
        :param data:
        :return:
        """
        data = data["data"]  # Don't need anything else here
        await self.cw_client.http.message_event_handler.dispatch(data)
