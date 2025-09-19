"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Handles serialising custom objects into json for requests and other purposes
"""
from typing_extensions import Any


def custom_serialise(obj: Any) -> dict[str, Any]:
    """
    Custom serialiser for orjson to handle the custom objects
    :param obj: The object to serialize
    :return: The serialisable object
    """
    from utils.profile_system import MCPProfile, MCPItem
    if isinstance(obj, MCPProfile):
        return obj.profile
    elif isinstance(obj, MCPItem):
        return obj.item
    else:
        try:
            return obj.__dict__
        except AttributeError:
            try:
                return obj.__dict__()
            except AttributeError:
                pass
    raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serialisable")
