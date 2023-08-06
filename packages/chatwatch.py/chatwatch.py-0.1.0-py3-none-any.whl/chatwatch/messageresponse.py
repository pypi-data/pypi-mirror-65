"""
Message responses from ChatWatch
"""
from typing import List

from discord import Guild


class Classification:
    """
    The classifications returned in a message
    """

    def __init__(self, name):
        """
        :param name: The classification name.
        """
        self.classifications = [
            "DOMAIN_NO_TRUST",
            "DOMAIN_LOW_TRUST",

            "DOMAIN_GLOBAL_SPAM_MODERATE",
            "DOMAIN_GLOBAL_SPAM_SEVERE",

            "DOMAIN_AUTO_BLACKLIST",
            "DOMAIN_BLACKLISTED",

            "DOMAIN_DISCORD_INVITE",
            "DOMAIN_HIGH_TRUST",

            "MESSAGE_SCORE_SEVERE",
            "MESSAGE_SCORE_HIGH",
            "MESSAGE_SCORE_WARN",

            "FOREIGN_LANGUAGE",
            "MESSAGE_SHORT",

            "MESSAGE_TOXICITY_SEVERE",
            "MESSAGE_TOXICITY_HIGH",
            "MESSAGE_TOXICITY_POSSIBLE",

            "MESSAGE_IDENTITY_ATTACK",
            "MESSAGE_SEXUALLY_EXPLICIT",

            "MESSAGE_WORD_REPETITION_MODERATE",
            "MESSAGE_WORD_REPETITION_SEVERE",
            "MESSAGE_CAPITALIZATION_MODERATE",
            "MESSAGE_CAPITALIZATION_SEVERE",
            "MESSAGE_MENTIONS_MODERATE",
            "MESSAGE_MENTIONS_HIGH",
            "MESSAGE_HIGH_SPAM_PROBABILITY",

            "MESSAGE_MENTIONS_SEVERE",

            "MESSAGE_SIMILARITY_GLOBAL",
            "MESSAGE_SIMILARITY_LOCAL_HIGH",
            "MESSAGE_SIMILARITY_LOCAL_SEVERE",

            "USER_SPAMBOT",
            "USER_BLACKLISTED",
            "USER_WHITELISTED"
        ]
        if name not in self.classifications:
            if name.startswith("LANGUAGE_"):
                pass
            else:
                raise TypeError("Invalid classification name: {}".format(name))
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<ChatWatchClassification {}>".format(self.name)

    def __eq__(self, other):
        if not isinstance(other, Classification):
            raise TypeError("Classification can only be compared with other Classifications")
        return self.name == other.name


class CWUser:
    """
    Internal user used by MessageResponse
    """

    def __init__(self, user_data: dict):
        """
        Internal usage only
        :param user_data: The user data from a MessageResponse
        """
        self.id: int = int(user_data["user"])  # pylint: disable = invalid-name
        self.guilds: List[int] = []
        for guild in user_data["guilds"]:
            self.guilds.append(guild)
        self.blacklisted: bool = user_data["blacklisted"]
        self.blacklisted_reason: str = user_data["blacklisted_reason"] if user_data["blacklisted_reason"] else None
        self.times_blacklisted: int = user_data["blacklisted_count"]
        self.whitelisted: bool = user_data["whitelisted"]
        self.spambot: bool = user_data["spambot"]
        self.score: float = user_data["score"]

    def is_in_guild(self, guild: Guild) -> bool:
        """
        Checks if the user is in a guild
        :param guild: The guild to check against.
        :return: If the user is in the guild or not
        """
        return guild.id in self.guilds


class MessageResponse:
    """
    ChatWatch response from a message
    """

    def __init__(self, data: dict):
        """
        Internal usage only
        :param data: The data to convert to a message response
        """
        self.message_score: float = data["scores"]["content"]
        self.user_score: float = data["scores"]["overall"]
        self.score: float = self.message_score

        self.message_id: int = int(data["message"]["id"])
        self.message_channel: int = int(data["message"]["channel"])
        self.message_guild: int = int(data["message"]["guild"])

        self.phonetic_id: str = data["metadata"]["phonetic_id"]

        self.user: CWUser = CWUser(data["user"])

        self.classifications = []
        for classification in data["classifications"]:
            self.classifications.append(Classification(classification))
