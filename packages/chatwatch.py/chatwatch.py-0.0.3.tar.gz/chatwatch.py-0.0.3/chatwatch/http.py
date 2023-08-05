"""
Http client for ChatWatch
"""

from asyncio import AbstractEventLoop
from asyncio import Event
from json import loads, dumps, JSONDecodeError
from logging import getLogger, Logger

from aiohttp import ClientSession, ClientConnectionError, WSServerHandshakeError, WSMsgType
from discord import Message

from .errors import GatewayRejection, ServiceOfflineError, InvalidTokenError
from .eventhandlers import EventHandler, MessageEventHandler
from .ratelimiters import Limiters
from .settings import library_stamp, base_logger
from .statistics import Statistics


class HttpClient:
    """
    Internal http client to interact with the ChatWatch api
    """

    def __init__(self, auth: str, loop: AbstractEventLoop, *, reconnect: bool = True, silent_connection: bool = False,
                 auto_silence_connection: bool = True):
        """
        :param auth: ksoft token
        :param loop: asyncio loop
        :param reconnect: whether to automatically reconnect or not
        :param silent_connection: whether to silently connect
        :param auto_silence_connection: automatically silence ourselves in the connection after 3 failed attempts
        """
        self.auth: str = auth
        self.loop: AbstractEventLoop = loop
        self.reconnect = reconnect
        self.silent_connection = silent_connection
        self.auto_silence_connection = auto_silence_connection

        self.logger: Logger = getLogger(base_logger + "http")
        self.message_event_handler: MessageEventHandler = MessageEventHandler(self.loop)
        self.event_handler: EventHandler = EventHandler(self.loop)
        self.statistics = Statistics()
        self.limiters = Limiters()
        self.message_queue: list = []
        self.started: bool = False
        self.started_event: Event = Event(loop=self.loop)

        self.auth_headers: dict = {"authorization": auth}
        self.library_headers: dict = {"User-Agent": library_stamp}
        self.ws_closers = [WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED]

        self.max_retries: int = 3
        self.connect_endpoint: str = "https://gateway.chatwatch.ksoft.si/acquire"

        self.websocket = None
        self.ws_uri: str = None
        self.http_session: ClientSession = None

    @property
    def connected(self) -> bool:
        """
        Whether we are connected to ChatWatch or not
        :return: if we are connected
        """
        return self.websocket is not None and not self.websocket.closed

    async def start_http_session(self):
        """
        Starts the http session
        :return: None
        """
        if not self.http_session:
            self.http_session = ClientSession()

    async def connect(self):
        """
        Connect to ChatWatch
        :return: None
        """
        await self.statistics.register_start(loop=self.loop)
        await self.start_http_session()
        silent = self.silent_connection
        gen = self.limiters.increasing_limiter()
        async for current_attempt in gen:
            if current_attempt == 2 and self.auto_silence_connection:
                self.logger.warning("Out of attempts. Connecting to chatwatch silently")
                silent = True
            try:
                self.ws_uri = await self.get_session(silent=silent)
            except GatewayRejection as error:
                if not silent:
                    self.logger.error("An error occurred while attempting to fetch gateway URL", error)
                continue
            except InvalidTokenError as error:
                raise error
            if not silent:
                self.logger.debug("Found WS URL: {}".format(self.ws_uri))
            try:
                self.websocket = await self.http_session.ws_connect(self.ws_uri, headers=self.auth_headers,
                                                                    autoping=True)
            except ClientConnectionError as error:
                if not silent:
                    self.logger.error("The server rejected our connection. Did you provide the correct credentials?",
                                      error)
                continue
            except WSServerHandshakeError as error:
                self.ws_uri = None
                if not silent:
                    self.logger.error("The server rejected our connection. Status code: {}".format(error.status))
                continue
            self.logger.info("Connected to ChatWatch")
            self.started_event.set()  # Event for client.wait_until_ready()
            if self.started:
                # TODO: Send everything in self.message_queue
                await self.event_handler.dispatch("resume", {})
            else:
                await self.event_handler.dispatch("connect", {})
            await self.send({"event": "hello", "data": library_stamp})  # TODO: Implement a default event on this?
            break
        self.logger.debug("Exiting connection loop")
        await gen.aclose()

    async def get_session(self, silent: bool = False):
        """
        Get a ChatWatch node from the gateway
        :param silent: Whether to be silent or not
        :return: The ChatWatch node URI
        """
        if not silent:
            self.logger.debug("Asking gateway for API server")
        try:
            request = await self.http_session.get(self.connect_endpoint, headers=self.auth_headers)
            if request.status != 200:
                data = await request.json()
                if data["message"] == "Unauthorized":
                    request.close()
                    raise InvalidTokenError()
                raise GatewayRejection()
            data = await request.json()
            if not silent:
                self.logger.debug("Found gateway URL")

            request.close()
            return data["url"]
        except ClientConnectionError:
            raise ServiceOfflineError()

    async def send(self, data: dict):
        """
        Sends a data to the websocket
        :param data: the data to be sent
        :return: None
        """
        if not self.connected:
            self.message_queue.append(data)
        self.logger.debug("> {}".format(dumps(data)))
        await self.websocket.send_json(data)

    async def handle_ws_message(self, data: str):
        """
        Handles a WebSocket message
        :param data: The data to be handled
        :return: None
        """
        try:
            json: dict = loads(data)
        except JSONDecodeError:
            self.logger.warning("Invalid response recieved")
            return

        if "event" not in json.keys():
            self.logger.warning("Random data received?")
        else:
            json_without_event = json.copy()
            json_without_event.pop("event")
            await self.event_handler.dispatch(json["event"], json)

    async def listener_task(self):
        """
        Task for reading websocket messages
        :return: None
        """
        while True:
            await self.started_event.wait()
            async for message in self.websocket:
                self.logger.debug("< {}".format(message.data))
                if message.type == WSMsgType.text:
                    await self.handle_ws_message(message.data)
                elif message.type in self.ws_closers:
                    if self.reconnect:
                        self.started_event.clear()
                        self.logger.warning("Connection to chatwatch disconnected. Reconnecting")
                        self.ws_uri = None
                        await self.connect()
                        break
                    else:
                        self.started_event.clear()
                        self.logger.warning("Connection to chatwatch disconnected.")
                        self.ws_uri = None
                else:
                    self.logger.error("Unknown message type: {}".format(message.type))

    async def send_message(self, message: Message):
        """
        Sends a message to ChatWatch
        :param message:
        :return:
        """
        await self.send(
            {
                "event": "message_ingest",
                "data": {
                    "guild": message.guild.id,
                    "channel": message.channel.id,
                    "message": message.content,
                    "message_id": message.id,
                    "user": message.author.id
                }
            })
