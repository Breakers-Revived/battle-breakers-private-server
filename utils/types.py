"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Contains typing information for the server
"""
import sanic
from typing_extensions import Any, Type

import motor.motor_asyncio
from cryptography.hazmat.primitives.asymmetric.dh import DHPublicKey
from cryptography.hazmat.primitives.asymmetric.dsa import DSAPublicKey
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
from cryptography.hazmat.primitives.asymmetric.x448 import X448PublicKey

from utils.enums import ProfileType
from utils.friend_system import PlayerFriends
from utils.profile_system import PlayerProfile
from utils.services.calendar.calendar import ScheduledEvents
from utils.services.lightswitch.lightswitch import LightswitchService
from utils.services.storefront.catalog import StoreCatalogue
from utils.toml_config import TomlConfig


class Context:
    """
    The context for the server
    """
    public_key: (DHPublicKey | DSAPublicKey | RSAPublicKey | EllipticCurvePublicKey | Ed25519PublicKey | Ed448PublicKey
                 | X25519PublicKey | X448PublicKey)
    db: motor.motor_asyncio.AsyncIOMotorClient
    calendar: ScheduledEvents
    storefronts: StoreCatalogue
    lightswitch: LightswitchService
    accounts: dict[str, Any]
    friends: dict[str, PlayerFriends]
    profiles: dict[str, PlayerProfile]
    invalid_tokens: list[str]
    config: TomlConfig


class BBRequest(sanic.request.Request[sanic.app.Sanic[TomlConfig, Type[Context]], Type[Context]]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def make_context() -> "BBRequestContext":
        return BBRequestContext()


class BBRequestContext:
    """
    The context type hints for a regular request
    """
    ctx: Context
    is_owner: bool
    owner: str
    dvid: str


class BBProfileRequest(sanic.request.Request[sanic.app.Sanic[TomlConfig, Type[Context]], Type[Context]]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def make_context() -> "BBProfileRequestContext":
        return BBProfileRequestContext()


class BBProfileRequestContext:
    """
    The context type hints for a profile request
    """
    ctx: Context
    is_owner: bool
    owner: str
    dvid: str
    account_id: str
    profile: PlayerProfile
    rvn: int
    profile_id: ProfileType
    profile_revisions: list[
        dict[str, str | int], dict[str, str | int], dict[str, str | int], dict[str, str | int], dict[
            str, str | int]]


class BBFriendRequest(sanic.request.Request[sanic.app.Sanic[TomlConfig, Type[Context]], Type[Context]]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def make_context() -> "BBFriendRequestContext":
        return BBFriendRequestContext()


class BBFriendRequestContext:
    """
    The context type hints for a friend request
    """
    ctx: Context
    is_owner: bool
    owner: str
    dvid: str
    friends: PlayerFriends
