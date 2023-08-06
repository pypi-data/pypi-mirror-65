"""
All the errors used by ChatWatch
"""


class ChatWatchError(BaseException):
    """
    Base ChatWatch error. All ChatWatch errors derive from this error.
    """


class RateLimiterError(BaseException):
    """
    Base RateLimiter error. All RateLimiter errors derive from this error
    """


# CW errors
class GatewayRejection(ChatWatchError):
    """
    The error raised when we get an unknown gateway error
    """

    def __init__(self):
        super().__init__("Something in the ChatWatch gateway broke.")


class InvalidTokenError(ChatWatchError):
    """
    The error raised when the user provided an incorrect token
    """
    def __init__(self):
        super().__init__("Invalid ChatWatch token provided")


class MaxListenersExceeded(ChatWatchError):
    """
    The error raised when the user registers more than the max_listeners per event. This is likely due to a memory leak
    """

    def __init__(self, max_listeners: int, event_name: str):
        self.max_listeners = max_listeners
        self.event = event_name
        super().__init__("Max listeners exceeded on event: {}. The current max is {}".format(event_name, max_listeners))


class NotConnectedError(ChatWatchError):
    """
    The error used when the user attempts to run a method that can only be ran after the client has connected,
    before it has connected
    """

    def __init__(self, method: str):
        super().__init__("{} can't be used until the client is connected!".format(method))


class ServiceOfflineError(ChatWatchError):
    """
    The error raised when ChatWatch is down
    """

    def __init__(self):
        super().__init__("ChatWatch seems to be down. Try again later.")


# Ratelimiting
class OutOfAttempts(RateLimiterError):
    """
    The error that is raised when the RateLimiter runs out of attempts
    """

    def __init__(self, attempts: int):
        super().__init__("The RateLimiter ran out of attempts! Attempts used: {}".format(attempts))
